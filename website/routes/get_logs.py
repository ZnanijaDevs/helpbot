import os
import time
from fastapi.responses import FileResponse
from website import app


@app.get(os.environ['LOGGER_PUBLIC_ENDPOINT'])
async def get_logs():
    return FileResponse(
        'logger.log',
        media_type='application/octet-stream',
        filename=f"helpbot-{time.time()}.log"
    )
