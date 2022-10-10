from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

# Init FastAPI app
app = FastAPI(docs_url=None, openapi_url=None)

# Mount templates
templates = Jinja2Templates(directory='webapp/templates')

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['GET', 'POST']
)
