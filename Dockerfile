FROM python:3.11.9


WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD sh -c "alembic upgrade head && python -m src.main"