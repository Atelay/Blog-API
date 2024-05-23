from src.authors.router import router as authors
from src.categories.router import router as categories
from src.posts.router import router as posts
from src.tags.router import router as tags

api_routers = [
    authors,
    tags,
    categories,
    posts,
]

from .main import app
