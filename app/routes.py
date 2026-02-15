from aiohttp import web
from pydantic import ValidationError
from sqlalchemy import select
from app.models import Advertisement
from app.schemas import AdvertisementCreate, AdvertisementUpdate


async def list_advertisements(request: web.Request) -> web.Response:
    async with request.app["session_factory"]() as session:
        stmt = select(Advertisement).order_by(
            Advertisement.created_at.desc()
        )
        result = await session.execute(stmt)
        ads = result.scalars().all()
        return web.json_response([ad.to_dict() for ad in ads])


async def create_advertisement(request: web.Request) -> web.Response:
    try:
        body = await request.json()
    except Exception:
        return web.json_response(
            {"error": "Invalid JSON or missing fields"}, status=400
        )
    try:
        data = AdvertisementCreate.model_validate(body)
    except ValidationError as e:
        return web.json_response({"errors": e.errors()}, status=400)
    async with request.app["session_factory"]() as session:
        ad = Advertisement(
            title=data.title,
            description=data.description,
            owner=data.owner,
        )
        session.add(ad)
        await session.commit()
        await session.refresh(ad)
        return web.json_response(ad.to_dict(), status=201)


async def get_advertisement(request: web.Request) -> web.Response:
    ad_id = int(request.match_info["ad_id"])
    async with request.app["session_factory"]() as session:
        ad = await session.get(Advertisement, ad_id)
        if ad is None:
            return web.json_response(
                {"error": "Advertisement not found"}, status=404
            )
        return web.json_response(ad.to_dict())


async def delete_advertisement(request: web.Request) -> web.Response:
    ad_id = int(request.match_info["ad_id"])
    async with request.app["session_factory"]() as session:
        ad = await session.get(Advertisement, ad_id)
        if ad is None:
            return web.json_response(
                {"error": "Advertisement not found"}, status=404
            )
        await session.delete(ad)
        await session.commit()
        return web.Response(status=204)


async def update_advertisement(request: web.Request) -> web.Response:
    ad_id = int(request.match_info["ad_id"])
    try:
        body = await request.json()
    except Exception:
        return web.json_response({"error": "Invalid JSON"}, status=400)
    try:
        data = AdvertisementUpdate.model_validate(body)
    except ValidationError as e:
        return web.json_response({"errors": e.errors()}, status=400)
    async with request.app["session_factory"]() as session:
        ad = await session.get(Advertisement, ad_id)
        if ad is None:
            return web.json_response(
                {"error": "Advertisement not found"}, status=404
            )
        payload = data.model_dump(exclude_unset=True)
        for key, value in payload.items():
            setattr(ad, key, value)
        await session.commit()
        await session.refresh(ad)
        return web.json_response(ad.to_dict())


async def index(request: web.Request) -> web.Response:
    return web.Response(
        text=(
            "API объявлений. Эндпоинты: "
            "GET/POST /api/advertisements, "
            "GET/PUT/DELETE /api/advertisements/<id>"
        )
    )
