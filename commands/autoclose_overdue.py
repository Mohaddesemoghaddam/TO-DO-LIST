from datetime import date

from db.session import SessionLocal
from services.task_service import TaskService


def autoclose_overdue_tasks():
    """
    Auto-close all overdue tasks:
    - deadline < today
    - status != "done"
    """
    db = SessionLocal()

    try:
        service = TaskService(db)

        count = service.autoclose_overdue_tasks()

        print(f"[AUTO-CLOSE] {count} overdue tasks closed.")

    except Exception as e:
        print(f"[ERROR] Auto-close failed: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    autoclose_overdue_tasks()
