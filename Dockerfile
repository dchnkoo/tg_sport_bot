FROM python:3.10.13

RUN apt-get update

WORKDIR /tg_bot

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x ./*.sh

CMD [ "./bot.sh" ]