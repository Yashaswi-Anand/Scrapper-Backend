# run.py
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from views.views import router as api_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Scrapper Backend API!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
