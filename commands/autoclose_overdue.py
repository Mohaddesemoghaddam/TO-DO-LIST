from services.task_service import TaskService

def run():
    try:
        task_service = TaskService()
        closed_count = task_service.autoclose_overdue_tasks()
        print(f"[SUCCESS] Auto-closed {closed_count} overdue tasks.")
    except Exception as e:
        print(f"[ERROR] Auto-close failed: {e}")

if __name__ == "__main__":
    run()
