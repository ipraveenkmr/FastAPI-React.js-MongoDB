from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.items import router as items_router

# FastAPI app
app = FastAPI()

# Configure CORS
origins = [
    "*",
]
# origins = ["http://localhost:3000",]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items_router, tags=["Items"], prefix="/api")