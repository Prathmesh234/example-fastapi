
from fastapi import FastAPI
from . import models
from .database import engine
from sqlalchemy.orm import Session
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

##models creates all the tables in the database based on the classes we have defined in the models.py file
#now that we have alembic creating our database tables we really do not have to do the bind=engine part 
#models.Base.metadata.create_all(bind=engine)
#print("Created the database tables")
app = FastAPI()
origins=["https://www.google.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return "Hello World Bananananana !!!!!"
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)




