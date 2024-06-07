FROM python:3.11-slim-buster


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /app

# Install dependencies
COPY requirement.txt /app/
RUN pip install --no-cache-dir -r requirement.txt


COPY . /app/

EXPOSE 8000


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
