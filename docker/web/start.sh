!#/bin/bash

echo "Apply migrations on db"
/usr/local/bin/poetry run alembic upgrade head


echo "Start service web ..."
/usr/local/bin/poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload