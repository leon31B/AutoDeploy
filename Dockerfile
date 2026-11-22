# Use official lightweight Python base image
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

# Set working directory inside container
WORKDIR /app

# Create a dedicated non-root user and group for security
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser

# Copy and install dependencies first (leverages Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY app.py .

# Change ownership of application files to non-root user
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Expose container port
EXPOSE 5000

# Run Flask application using Gunicorn production WSGI server
# Dynamically binds to $PORT provided by host/Render (defaulting to 5000)
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 2 --threads 4 --timeout 60 app:app"]
