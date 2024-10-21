FROM python:3.11.10-alpine3.20

RUN pip install --no-cache-dir gunicorn
COPY wsgi.py /app/

WORKDIR /app

# 2 workers and port 9009
CMD ["gunicorn", "-b", "0.0.0.0:9009", "--workers", "2", "wsgi:application"]