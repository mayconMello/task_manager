import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.middleware.asyncio import AsyncIO

from app.core.configs import settings
from app.infra.db.session import AsyncSessionLocal
from app.infra.factories.notification_factory import NotificationFactory

redis_broker = RedisBroker(host=settings.BROKER_HOST, port=settings.BROKER_PORT)
redis_broker.add_middleware(AsyncIO())
dramatiq.set_broker(redis_broker)

notification_factory = NotificationFactory()


@dramatiq.actor
async def task_send_due_notifications_task():
    async with AsyncSessionLocal() as session:
        use_case = notification_factory.send_due_task_notification_use_case(session)
        await use_case.execute()
