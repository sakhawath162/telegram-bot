FROM python:3.12-alpine
RUN apk add --no-cache tzdata
WORKDIR /app
COPY bot.py messages.py ./
ENV DB_PATH=/data/bot.db PYTHONUNBUFFERED=1
VOLUME /data
CMD ["python", "bot.py"]
