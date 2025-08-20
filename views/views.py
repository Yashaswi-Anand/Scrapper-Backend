# views/views.py
from fastapi import APIRouter
from services.api_functions import  get_simple_data

router = APIRouter()

@router.get("/latest_job_list")
async def get_simple_data_endpoint(tech_job: str, location: str):
    """
    Endpoint to get simple data.
    http://localhost:8000/simple_data?tech_job=python_developer&location=pune
    """
    return get_simple_data(tech_job, location)
