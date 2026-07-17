"""Генерация текстовок email-кампаний через Claude (Anthropic API).

Используется структурированный вывод (output_config.format) — на выходе всегда
валидный JSON с вариантами тем и последовательностью писем.
"""
from __future__ import annotations

import json

from anthropic import AsyncAnthropic

from .config import settings
from .models import CopyBrief, GeneratedCopy

_client: AsyncAnthropic | None = None


def _get_client() -> AsyncAnthropic:
    global _client
    if _client is None:
        if not settings.anthropic_ready:
            raise RuntimeError("Не задан ANTHROPIC_API_KEY (см. .env).")
        _client = AsyncAnthropic(api_key=settings.anthropic_api_key)
    return _client


_OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "subject_variants": {
            "type": "array",
            "items": {"type": "string"},
            "description": "3-5 вариантов темы письма для A/B-теста",
        },
        "steps": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "step": {"type": "integer"},
                    "subject": {"type": "string"},
                    "body": {"type": "string"},
                    "delay_days": {"type": "integer"},
                },
                "required": ["step", "subject", "body", "delay_days"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["subject_variants", "steps"],
    "additionalProperties": False,
}

_SYSTEM = (
    "Ты — старший B2B копирайтер по холодным email-рассылкам. "
    "Пишешь короткие, персонализированные, конкретные письма без спам-триггеров "
    "и воды. Первое письмо + follow-up'ы образуют логичную последовательность: "
    "каждый follow-up добавляет ценность, а не просто напоминает. "
    "Используй плейсхолдеры Snov.io для персонализации: {{first_name}}, "
    "{{company_name}}, {{position}}. Один чёткий призыв к действию на письмо."
)


def _build_prompt(brief: CopyBrief) -> str:
    return (
        f"Составь холодную email-кампанию на языке: {brief.language}.\n"
        f"Продукт/услуга: {brief.product}\n"
        f"Аудитория (ICP): {brief.audience}\n"
        f"Цель кампании: {brief.goal}\n"
        f"Тон: {brief.tone}\n"
        f"Имя отправителя для подписи: {brief.sender_name or '(без подписи)'}\n"
        f"Кол-во follow-up писем после первого: {brief.num_followups}\n"
        f"Доп. заметки: {brief.extra_notes or 'нет'}\n\n"
        f"Верни {brief.num_followups + 1} шаг(ов) писем: шаг 1 — первичное письмо "
        f"(delay_days=0), затем follow-up'ы с разумными задержками (обычно 2-4 дня). "
        f"И 3-5 вариантов темы для первого письма."
    )


async def generate_copy(brief: CopyBrief) -> GeneratedCopy:
    client = _get_client()
    resp = await client.messages.create(
        model=settings.claude_model,
        max_tokens=8000,
        thinking={"type": "adaptive"},
        system=_SYSTEM,
        messages=[{"role": "user", "content": _build_prompt(brief)}],
        output_config={"format": {"type": "json_schema", "schema": _OUTPUT_SCHEMA}},
    )
    text = next((b.text for b in resp.content if b.type == "text"), "")
    data = json.loads(text)
    return GeneratedCopy.model_validate(data)
