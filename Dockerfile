# Start from a slim official Python image matching our dev version (3.13).
# "slim" = much smaller than the full image, but still has what pip needs.
FROM python:3.13-slim

# PYTHONDONTWRITEBYTECODE: don't litter .pyc files inside the container.
# PYTHONUNBUFFERED: stream stdout/stderr straight out so `docker logs` is live.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# All subsequent commands run in /app inside the image.
WORKDIR /app

# Copy ONLY requirements first, then install. Docker caches each layer, so as
# long as requirements.txt is unchanged, rebuilds skip the (slow) pip install
# even when you edit your code. Order matters for fast rebuilds.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the project (main.py today, future cogs automatically).
# .dockerignore keeps .env, .venv, .git, etc. out of this.
COPY . .

# Run as a non-root user — good practice; a bug or exploit can't run as root.
RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

# The command that launches the bot when the container starts.
CMD ["python", "main.py"]
