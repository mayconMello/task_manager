from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.infra.dramatiq.tasks import task_send_due_notifications_task

scheduler = AsyncIOScheduler()

scheduler.add_job(task_send_due_notifications_task.send, 'cron', hour=1, minute=0)
