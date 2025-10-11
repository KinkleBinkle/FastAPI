from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from models import Base
from routes import books, students


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Cleanup (optional)
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)

app = FastAPI(lifespan=lifespan)

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # or specify e.g. ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root
@app.get("/")
async def read_root():
    return {"message": "Books & Students API - Modularized"}

# Include Routers
app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(students.router, prefix="/students", tags=["Students"])
