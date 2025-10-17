FROM python:3.13-slim

# Set work directory
WORKDIR /app

# Copy app code
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# Set the default port
ENV PORT=9000
EXPOSE 9000

# Run using uv
CMD ["python", "main.py"]


