import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, JSON, Boolean, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import declarative_base

Base = declarative_base()

def get_utc_now():
    return datetime.now(timezone.utc)

class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String, index=True, nullable=False)
    original_request = Column(String, nullable=False)
    status = Column(String, nullable=False, default="pending")
    created_at = Column(DateTime(timezone=True), default=get_utc_now)
    completed_at = Column(DateTime(timezone=True), nullable=True)

class HITLQueue(Base):
    __tablename__ = "hitl_queue"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=False)
    subtask_id = Column(String, nullable=False)
    tenant_id = Column(String, index=True, nullable=False)
    reason = Column(String, nullable=False)
    context_json = Column(JSONB, nullable=False)
    status = Column(String, nullable=False, default="pending")
    decision = Column(String, nullable=True)
    sla_deadline = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)

class MemoryEpisode(Base):
    __tablename__ = "memory_episodes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=False)
    tenant_id = Column(String, index=True, nullable=False)
    content = Column(String, nullable=False)
    quality_score = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)

class ToolCall(Base):
    __tablename__ = "tool_calls"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=False)
    tool_name = Column(String, nullable=False)
    input_data = Column(JSONB, nullable=False)
    output_data = Column(JSONB, nullable=True)
    execution_time_ms = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)
