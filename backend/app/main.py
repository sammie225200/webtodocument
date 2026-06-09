from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine

from app.routers.auth import router as auth_router
from app.routers.generate import router as generate_router

# NEW ROUTERS
from app.routers.sites import router as sites_router
from app.routers.preview import router as preview_router
from app.routers.download import router as download_router
from app.routers.publish import router as publish_router
from app.routers.feedback import router as feedback_router
from app.routers.admin import router as admin_router


# Create tables
Base.metadata.create_all(bind=engine)

# Create folders
Path("generated").mkdir(exist_ok=True)
Path("published").mkdir(exist_ok=True)

app = FastAPI(
    title="Document To Website API",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static published websites
app.mount(
    "/published",
    StaticFiles(directory="published"),
    name="published"
)

# ROUTERS
app.include_router(
    auth_router,
    prefix="/api"
)

app.include_router(
    generate_router,
    prefix="/api"
)

app.include_router(
    sites_router,
    prefix="/api"
)

app.include_router(
    preview_router,
    prefix="/api"
)

app.include_router(
    download_router,
    prefix="/api"
)

app.include_router(
    publish_router,
    prefix="/api"
)

app.include_router(
    feedback_router,
    prefix="/api"
)

app.include_router(
    admin_router,
    prefix="/api"
)


@app.get("/")
def root():
    return {
        "message": "Document To Website API Running",
        "docs": "/docs"
    }


# DEBUG ROUTES
print("\nREGISTERED ROUTES:\n")

for route in app.routes:
    try:
        print(
            f"{route.path} -> {route.methods}"
        )
    except Exception:
        pass

print("\nEND ROUTES\n")