import os

SQLITE_FALLBACK_URI = "sqlite+aiosqlite:///instance/ads.db"


def get_database_uri():
    uri = os.environ.get("DATABASE_URL") or (
        "postgresql://localhost:5432/ads_db"
    )
    if uri.startswith("postgresql://") and "+asyncpg" not in uri:
        uri = uri.replace("postgresql://", "postgresql+asyncpg://", 1)
    if uri.startswith("sqlite"):
        uri = uri.replace("sqlite://", "sqlite+aiosqlite://", 1)
    return uri
