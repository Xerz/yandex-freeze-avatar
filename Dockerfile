FROM chetan1111/botasaurus:latest

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

RUN mkdir app
WORKDIR /app
COPY . /app

CMD ["python", "main.py"]