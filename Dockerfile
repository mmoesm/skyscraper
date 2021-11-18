FROM python:3.9.4-alpine3.13

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 80

CMD ["uvicorn",  "main:app", "--host", "0.0.0.0", "--port", "80"]