from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from src.config import SWAGGER_PARAMETERS
from src.utils import lifespan
from src import api_routers


app = FastAPI(
    default_response_class=ORJSONResponse,
    swagger_ui_parameters=SWAGGER_PARAMETERS,
    title="Blog App",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

[app.include_router(router, prefix="/api/v1") for router in api_routers]
