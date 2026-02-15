import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from aiohttp import web

from app.database import get_session_factory, init_db
from app.routes import (
    create_advertisement,
    delete_advertisement,
    get_advertisement,
    index,
    list_advertisements,
    update_advertisement,
)

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
}


@web.middleware
async def cors_middleware(request: web.Request, handler):
    if request.method == "OPTIONS":
        return web.Response(status=204, headers=CORS_HEADERS)
    response = await handler(request)
    for key, value in CORS_HEADERS.items():
        response.headers[key] = value
    return response


async def on_startup(app: web.Application):
    await init_db()
    app["session_factory"] = get_session_factory()


def create_app():
    app = web.Application(middlewares=[cors_middleware])
    app.on_startup.append(on_startup)
    app.router.add_get("/", index)
    app.router.add_get("/api/advertisements", list_advertisements)
    app.router.add_post("/api/advertisements", create_advertisement)
    app.router.add_get("/api/advertisements/{ad_id}", get_advertisement)
    app.router.add_put("/api/advertisements/{ad_id}", update_advertisement)
    app.router.add_delete("/api/advertisements/{ad_id}", delete_advertisement)
    return app


def main():
    port = int(os.environ.get("PORT", 5001))
    app = create_app()
    web.run_app(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
