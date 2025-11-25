from db.session import get_db
from models.project import Project
from repositories.base_repository import BaseRepository

class ProjectRepository(BaseRepository[Project]):
    def __init__(self, session=None):
        super().__init__(session or get_db(), Project)
if __name__ == "__main__":
    from db.session import get_db

    try:
        db = next(get_db())
        print("✅ Database engine created successfully.")
    except Exception as e:
        print("❌ Error connecting to database:", e)
