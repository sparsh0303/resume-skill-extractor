FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

# Set environment variables so Flask knows where to start
ENV FLASK_APP=backend/main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

EXPOSE 5000

CMD ["flask", "run"]
