from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.roadmap_generator import generate_roadmap


app = FastAPI()

# Configure CORS to allow requests from your frontend origin
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # You can use ["*"] to allow all origins in development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RoadmapRequest(BaseModel):
    skill: str
    duration: str
    level: str


@app.post("/generate")
def generate_endpoint(req: RoadmapRequest):
    roadmap = generate_roadmap(req.skill, req.duration, req.level)
    return {
        "skill": req.skill,
        "duration": req.duration,
        "level": req.level,
        "roadmap": roadmap
    }
