FROM python:alpine


WORKDIR app/

COPY . .

RUN pip install aiogram requests python-dotenv


CMD ["python","./app/bot.py"]





