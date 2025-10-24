# ---- Dockerfile for Ollama Streamlit App ----

# Use lightweight Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Set environment variable to avoid Streamlit auto-launching browser
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLECORS=false
ENV STREAMLIT_SERVER_PORT=8501

# Command to run the app
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
