FROM python:3.13-slim

WORKDIR /app

COPY . /app

ENV PYTHONPATH="${PYTHONPATH}:/app"

RUN pip install -r requirements.txt

#CMD ["python", "-m","mcp_server.main"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]