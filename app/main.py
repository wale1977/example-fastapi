from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # allow other domains to communicate with our API

from . import models
from .database import engine
from .routers import post, user, auth, vote
# from .config import settings

# models.Base.metadata.create_all(bind=engine)  Alembic has taken over the operation of this

# origins = ["https://www.google.com", "https://www.youtube.com"]
origins = ["*"]   # It is the best practise to have a list of domains that can access our API, like the one above. * indicates all domain.

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# includes the routes
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

#------ Routes --------------------------
@app.get("/") # A decoraator
async def root():
    return {"message":"Welcome to my API"}