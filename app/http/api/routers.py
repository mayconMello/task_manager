from fastapi import APIRouter

from app.http.api.v1 import users, sessions, categories, tasks, subtasks, comments, attachments

router = APIRouter(prefix='/api/v1')

router.include_router(users.router, prefix='/users')
router.include_router(sessions.router, prefix='/sessions')
router.include_router(categories.router, prefix='/categories')
router.include_router(tasks.router, prefix='/tasks')
router.include_router(subtasks.router, prefix='/tasks')
router.include_router(comments.router, prefix='/tasks')
router.include_router(attachments.router, prefix='/tasks')
