"""FastAPI-приложение: генерация текстовок (Claude) + работа с Snov.io.

Рабочий процесс (draft-for-approval):
  1. /api/generate-copy  — Claude пишет черновик кампании (темы + письма).
  2. Ты просматриваешь/правишь черновик в UI.
  3. /api/prospects      — создаётся список и добавляются получатели в Snov.io.
  4. /api/launch         — получатели добавляются в drip-кампанию (запуск).
  5. /api/analytics/{id} — метрики кампании (opens/clicks/replies).
"""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .config import settings
from .copywriter import generate_copy
from .models import CopyBrief, GeneratedCopy, LaunchRequest, ProspectsRequest
from .snov import SnovError, snov_client

app = FastAPI(title="Marketing AI — Claude × Snov.io")

STATIC_DIR = Path(__file__).parent / "static"


@app.get("/api/health")
async def health() -> dict:
    return {
        "status": "ok",
        "anthropic_configured": settings.anthropic_ready,
        "snov_configured": settings.snov_ready,
        "model": settings.claude_model,
    }


@app.post("/api/generate-copy", response_model=GeneratedCopy)
async def api_generate_copy(brief: CopyBrief) -> GeneratedCopy:
    try:
        return await generate_copy(brief)
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Ошибка генерации: {e}") from e


@app.get("/api/snov/lists")
async def api_snov_lists() -> dict:
    try:
        return {"lists": await snov_client.get_lists()}
    except SnovError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e


@app.post("/api/prospects")
async def api_prospects(req: ProspectsRequest) -> dict:
    """Создаёт список в Snov.io и добавляет в него получателей."""
    try:
        created = await snov_client.create_list(req.list_name)
        list_id = created.get("id") or created.get("listId")
        if not list_id:
            raise HTTPException(status_code=502, detail=f"Не получен id списка: {created}")
        results = []
        for p in req.prospects:
            res = await snov_client.add_prospect(int(list_id), p.model_dump())
            results.append({"email": p.email, "result": res})
        return {"list_id": list_id, "added": len(results), "details": results}
    except SnovError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e


@app.post("/api/launch")
async def api_launch(req: LaunchRequest) -> dict:
    """Добавляет получателей в существующую drip-кампанию Snov.io (= запуск)."""
    try:
        prospects = [p.model_dump() for p in req.prospects]
        if req.list_id and not prospects:
            data = await snov_client.request(
                "GET",
                f"/v1/prospect-list/{req.list_id}",
            )
            for item in data.get("prospects", data if isinstance(data, list) else []):
                emails = item.get("emails") or []
                email = emails[0].get("email") if emails else item.get("email")
                if email:
                    prospects.append(
                        {
                            "email": email,
                            "first_name": item.get("firstName", ""),
                            "last_name": item.get("lastName", ""),
                        }
                    )
        if not prospects:
            raise HTTPException(status_code=400, detail="Нет получателей для запуска.")
        results = []
        for p in prospects:
            res = await snov_client.add_prospect_to_campaign(req.campaign_id, p)
            results.append({"email": p["email"], "result": res})
        return {"campaign_id": req.campaign_id, "launched_for": len(results), "details": results}
    except SnovError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e


@app.get("/api/analytics/{campaign_id}")
async def api_analytics(campaign_id: int) -> dict:
    try:
        return {"campaign_id": campaign_id, "analytics": await snov_client.campaign_analytics(campaign_id)}
    except SnovError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e


@app.get("/")
async def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
