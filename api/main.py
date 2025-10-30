from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from api.dependencies.database import engine
from api.models import models
from api.controllers import orders, sandwiches, recipes, resources

# Create tables automatically
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow all CORS origins (for testing)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers (important part)
app.include_router(orders.router)
app.include_router(sandwiches.router)
app.include_router(recipes.router)
app.include_router(resources.router)
