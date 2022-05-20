from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

# Init FastAPI app
app = FastAPI(docs_url=None)

# Mount static files
app.mount('/static', StaticFiles(directory='website/static'), name='static')

# Mount templates
templates = Jinja2Templates(directory='website/templates')

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['https://znanija.com', 'https://brainly.com'],
    allow_methods=['GET', 'POST']
)
