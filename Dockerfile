FROM python:3

WORKDIR /app

ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV PYTHONUNBUFFERED 1

EXPOSE 5000

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

COPY config.py /app

CMD ["python", "./app/__init__.py"]