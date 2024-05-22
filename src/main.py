from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import ORJSONResponse

from src.config import SWAGGER_PARAMETERS


app = FastAPI(
    default_response_class=ORJSONResponse,
    swagger_ui_parameters=SWAGGER_PARAMETERS,
    title="Blog App",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
