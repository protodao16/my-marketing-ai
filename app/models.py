"""Pydantic-модели запросов и ответов API."""
from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


# ---------- Копирайтинг ----------
class CopyBrief(BaseModel):
    """Бриф для генерации текстовок кампании."""

    product: str = Field(..., description="Что продвигаем (продукт/услуга)")
    audience: str = Field(..., description="Целевая аудитория / ICP")
    goal: str = Field("book_meeting", description="Цель: book_meeting, demo, reply, signup ...")
    tone: str = Field("профессиональный, дружелюбный", description="Тон письма")
    language: str = Field("ru", description="Язык писем (ru/en/...)")
    sender_name: str = Field("", description="Имя отправителя для подписи")
    num_followups: int = Field(2, ge=0, le=5, description="Сколько follow-up писем сгенерировать")
    extra_notes: str = Field("", description="Доп. пожелания / факты о продукте")


class EmailStep(BaseModel):
    step: int = Field(..., description="Номер шага (1 = первое письмо)")
    subject: str
    body: str
    delay_days: int = Field(0, description="Задержка в днях перед отправкой относительно предыдущего шага")


class GeneratedCopy(BaseModel):
    subject_variants: list[str] = Field(default_factory=list, description="Варианты тем для A/B")
    steps: list[EmailStep] = Field(default_factory=list)


# ---------- Проспекты ----------
class Prospect(BaseModel):
    email: EmailStr
    first_name: str = ""
    last_name: str = ""
    company: str = ""
    position: str = ""


class ProspectsRequest(BaseModel):
    list_name: str = Field(..., description="Имя списка проспектов в Snov.io")
    prospects: list[Prospect]


# ---------- Запуск кампании ----------
class LaunchRequest(BaseModel):
    campaign_id: int = Field(..., description="ID существующей drip-кампании в Snov.io")
    list_id: int | None = Field(None, description="ID списка проспектов (если добавляем весь список)")
    prospects: list[Prospect] = Field(default_factory=list, description="Или конкретные получатели")
