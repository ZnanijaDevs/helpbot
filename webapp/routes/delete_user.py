from fastapi import status, Response, BackgroundTasks
from pydantic import conint

from webapp import app
from webapp.background_tasks.delete_message_by_user import delete_message_by_user


@app.post('/delete_user/{user_id}')
async def delete_user(user_id: conint(gt=3), background_tasks: BackgroundTasks):
    background_tasks.add_task(delete_message_by_user, user_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
