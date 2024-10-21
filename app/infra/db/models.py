import uuid
from datetime import datetime

from sqlalchemy import Column, String, UUID, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.infra.db.base import Base


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    name = Column(
        String,
        nullable=False
    )
    email = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )
    password = Column(
        String,
        nullable=False
    )

    role = Column(
        String(20),
        default='MEMBER'
    )

    tasks = relationship(
        "TaskModel",
        back_populates="user"
    )
    comments = relationship(
        "CommentModel",
        back_populates="user"
    )

    created_at = Column(
        DateTime,
        default=datetime.now
    )
    updated_at = Column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now
    )


class CategoryModel(Base):
    __tablename__ = "categories"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    name = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    tasks = relationship(
        "TaskModel",
        back_populates="category"
    )


class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    title = Column(String(100), nullable=False)
    description = Column(String, nullable=True)
    due_date = Column(DateTime, nullable=True)
    priority = Column(
        String(20),
        default='medium'
    )
    created_at = Column(
        DateTime,
        default=datetime.now
    )
    updated_at = Column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now
    )
    is_completed = Column(
        Boolean,
        default=False
    )

    user_id = Column(
        UUID,
        ForeignKey("users.id"),
        nullable=False
    )
    category_id = Column(
        UUID,
        ForeignKey("categories.id"),
        nullable=True
    )

    user = relationship(
        "UserModel",
        back_populates="tasks"
    )
    category = relationship(
        "CategoryModel",
        back_populates="tasks"
    )
    subtasks = relationship(
        "SubtaskModel",
        back_populates="task",
        cascade="all, delete-orphan"
    )
    comments = relationship(
        "CommentModel",
        back_populates="task",
        cascade="all, delete-orphan"
    )
    attachments = relationship(
        "AttachmentModel",
        back_populates="task",
        cascade="all, delete-orphan"
    )


class SubtaskModel(Base):
    __tablename__ = "subtasks"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    title = Column(
        String(100),
        nullable=False
    )
    is_completed = Column(
        Boolean,
        default=False
    )

    task_id = Column(
        UUID,
        ForeignKey("tasks.id"),
        nullable=False
    )

    task = relationship(
        "TaskModel",
        back_populates="subtasks"
    )


class CommentModel(Base):
    __tablename__ = "comments"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    content = Column(
        String(),
        nullable=False
    )
    created_at = Column(
        DateTime,
        default=datetime.now
    )
    task_id = Column(
        UUID,
        ForeignKey("tasks.id"),
        nullable=False
    )

    task = relationship(
        "TaskModel",
        back_populates="comments"
    )

    user_id = Column(
        UUID,
        ForeignKey("users.id"),
        nullable=False
    )

    user = relationship(
        "UserModel",
        back_populates="comments"
    )


class AttachmentModel(Base):
    __tablename__ = "attachments"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    original_name = Column(
        String(),
        nullable=False
    )
    filename = Column(
        String(),
        nullable=False
    )
    file_path = Column(
        String(),
        nullable=False
    )

    task_id = Column(
        UUID,
        ForeignKey("tasks.id"),
        nullable=False
    )

    task = relationship(
        "TaskModel",
        back_populates="attachments"
    )
