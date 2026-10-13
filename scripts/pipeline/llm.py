from __future__ import annotations

import json
import os
import re
from pathlib import Path

from openai import OpenAI, RateLimitError
from tenacity import retry, retry_not, stop_after_attempt, wait_exponential, retry_if_exception_type

PROMPTS_DIR = Path(__file__).parent.parent.parent / "prompts"

# LLM 调用容错：指数退避重试，覆盖服务端瞬时不可用（如 Connection reset by peer）。
# 5 次尝试、退避序列约 2/4/8/16s（封顶 60s），可跨过数十秒级的服务端抖动窗口。
# 限流（429 / quota）不在此重试：模型级降级已由 _chat 处理，重试只会白等配额窗口。
_RETRY = retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=2, max=60),
    retry=retry_if_exception_type(Exception) & retry_not(RateLimitError),
)


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(
            f"Missing required env var: {name}. "
            f"Set it in .env (local) or GitHub Secrets (CI)."
        )
    return value


def get_client() -> OpenAI:
    """构造 OpenAI 兼容 client（复用 llm_analyzer 的配置契约）。"""
    return OpenAI(
        api_key=_require_env("LLM_API_KEY"),
        base_url=_require_env("LLM_BASE_URL"),
        timeout=120.0,
        max_retries=0,  # 重试统一交给 tenacity（_RETRY），避免双层退避叠加
    )


def get_model() -> str:
    return _require_env("LLM_MODEL")


def get_models() -> list[str]:
    """主模型 + LLM_FALLBACK_MODELS（逗号分隔）构成的降级链。

    免费档常见「某模型当日请求数耗尽」（Gemini flash-lite 500 次/天），
    单个模型耗尽时按序换下一个，避免整条流水线因 429 直接失败。
    """
    chain = [get_model()]
    extra = os.environ.get("LLM_FALLBACK_MODELS", "")
    for name in extra.split(","):
        name = name.strip()
        if name and name not in chain:
            chain.append(name)
    return chain


def _chat(client: OpenAI, messages: list[dict], **kwargs) -> str:
    """按降级链尝试 Chat Completions，返回文本内容。"""
    last_err: Exception | None = None
    for model in get_models():
        try:
            response = client.chat.completions.create(model=model, messages=messages, **kwargs)
            if len(get_models()) > 1 and model != get_models()[0]:
                print(f"⚠ [{model}] used (primary model rate-limited)")
            return response.choices[0].message.content
        except RateLimitError as err:
            last_err = err
            print(f"⚠ rate limited on [{model}]; trying next model in chain")
    raise last_err if last_err else RuntimeError("no model available")


def load_prompt(name: str) -> str:
    """加载 prompts/{name} 文件（name 含扩展名，如 'classifier.md'）。"""
    path = PROMPTS_DIR / name
    return path.read_text(encoding="utf-8")


def _extract_json(text: str) -> str:
    """兼容 markdown code fence 包裹的 JSON。"""
    text = text.strip()
    match = re.search(r"```(?:json)?\s*([\{\[][\s\S]*[\}\]])\s*```", text)
    return match.group(1) if match else text


@_RETRY
def call_json(
    system: str,
    user: str,
    *,
    temperature: float = 0.4,
    model: str | None = None,
) -> dict | list:
    """调用 LLM 并解析 JSON 输出。限流走模型降级链，其余异常指数退避重试。"""
    client = get_client()
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]

    if model:  # 显式指定模型时不走降级链
        try:
            content = _chat_single(client, model, messages, temperature=temperature,
                                   response_format={"type": "json_object"})
        except Exception as err:
            if "response_format" in str(err).lower() or "json_object" in str(err).lower():
                content = _chat_single(client, model, messages, temperature=temperature)
            else:
                raise
    else:
        try:
            content = _chat(client, messages, temperature=temperature,
                            response_format={"type": "json_object"})
        except Exception as err:
            if "response_format" in str(err).lower() or "json_object" in str(err).lower():
                content = _chat(client, messages, temperature=temperature)
            else:
                raise

    return json.loads(_extract_json(content))


def _chat_single(client: OpenAI, model: str, messages: list[dict], **kwargs) -> str:
    response = client.chat.completions.create(model=model, messages=messages, **kwargs)
    return response.choices[0].message.content


@_RETRY
def call_text(
    system: str,
    user: str,
    *,
    temperature: float = 0.5,
    model: str | None = None,
) -> str:
    """调用 LLM 返回纯文本（主笔合成 markdown 用）。"""
    client = get_client()
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]
    if model:
        return _chat_single(client, model, messages, temperature=temperature).strip()
    return _chat(client, messages, temperature=temperature).strip()
