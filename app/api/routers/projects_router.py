from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_all_projects():
    return {"message": "List of projects"}
