import uvicorn

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware
from api import test, view, cropData, statusData

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(test.router)
app.include_router(view.router)
app.include_router(cropData.router)
app.include_router(statusData.router)

HOST = "0.0.0.0"
# PORT = 80
# HOST = "127.0.0.1"
PORT = 8080


if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
