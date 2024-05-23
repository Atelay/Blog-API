from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from src.config import SWAGGER_PARAMETERS
from src.authors.router import router as authors
from src.categories.router import router as categories
from src.posts.router import router as posts
from src.tags.router import router as tags


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

app.include_router(authors)
app.include_router(tags)
app.include_router(categories)
app.include_router(posts)
