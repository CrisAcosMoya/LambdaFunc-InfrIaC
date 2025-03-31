FROM python:3.8-slim

WORKDIR /app

COPY dependencies.txt dependencies.txt
RUN pip install --no-cache-dir -r dependencies.txt

COPY . .

EXPOSE 5000

ENV AWS_ACCESS_KEY_ID=test
ENV AWS_SECRET_ACCESS_KEY=test
ENV AWS_DEFAULT_REGION=us-east-1

CMD ["python", "app.py"]