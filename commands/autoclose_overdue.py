import time
import schedule
from db.session import SessionLocal
from services.task_service import TaskService


# def job():
#     print("⏳ Checking for late tasks...")
#     db = SessionLocal()
#     service = TaskService(db)

#     updated_count = service.close_late_tasks()

#     db.close()

#     print(f"✔ Updated {updated_count} late tasks at {datetime.utcnow()}")

# def main():
#     # Run every 2 minutes
#     schedule.every(2).minutes.do(job)
    
#     while True:
#         schedule.run_pending()
#         time.sleep(1)

# if __name__ == "__main__":
#     main()
def job():
    db = SessionLocal()
    service = TaskService(db)
    closed = service.close_late_tasks()
    db.close()
    print(f"[AUTO] Closed {closed} late tasks.")

schedule.every(2).minutes.do(job)

print("Auto-close task scheduler started... (every 2 minutes)")

while True:
    schedule.run_pending()
    time.sleep(1)