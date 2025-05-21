import uuid

from typing import List, Optional
from fastapi import APIRouter, HTTPException

from app.database.db_connection import create_session
from app.model.Task import TaskTable, Task

router = APIRouter()


@router.get('/tasks', response_model=List[Task])
def get_user_tasks(user_uuid: uuid.UUID):
    session = create_session()
    try:
        existing_user_tasks = session.query(TaskTable).filter_by(user_uuid=user_uuid).all()
        if not existing_user_tasks:
            raise HTTPException(status_code=404, detail=f'no existing tasks for this user {user_uuid}')
        return existing_user_tasks
    finally:
        session.close()


# @router.put('/tasks/{id}')
# def put_task_of_user(
#         user_uuid: uuid.UUID,
#         title: str,
#         description: Optional[str],
#         is_complete: bool
# ):
#     session = create_session()
#     try:
#         existing_user_tasks = session.query(TaskTable).filter_by(user_uuid=user_uuid).all()
#     finally:
#         session.close()


