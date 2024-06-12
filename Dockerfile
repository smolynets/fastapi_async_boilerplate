FROM python:3.12

WORKDIR /backend

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY alembic.ini /app/alembic.ini

RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
