FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

COPY ./api .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]