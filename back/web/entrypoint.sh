#!/bin/sh

pip install -r requirements.txt

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."
    while ! (echo > /dev/tcp/$SQL_HOST/$SQL_PORT) >/dev/null 2>&1; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

mkdir -p alembic/versions
alembic revision --message="Init migration" --autogenerate
alembic upgrade head
python /usr/src/app/project/init_data.py

uvicorn project.main:app --port=1111 --host='0.0.0.0' --reload



exec "$@"