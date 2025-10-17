FROM python:3.13-slim
 
# Set work directory
WORKDIR /app
 
# Copy app code
COPY requirements.txt .
 
RUN pip install -r requirements.txt
 
COPY . .
 
# Set the default port
EXPOSE 8010
 
# Run using uv
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8010"]