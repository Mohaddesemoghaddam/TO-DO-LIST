from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_all_tasks():
    return {"message": "List of tasks"}
