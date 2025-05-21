FROM python:3.10

# Set working directory inside the container
WORKDIR /app

# Copy everything into the container
COPY . /app

# Set Python path to recognize `app/` as top-level
ENV PYTHONPATH=/app

# Install dependencies
RUN pip install -r requirements.txt

# Expose app port
EXPOSE 5050

# Run the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5050"]
