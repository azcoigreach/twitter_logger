FROM python:2.7.14-jessie

WORKDIR /usr/src/app
RUN chmod +x /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

ADD /app ./

CMD ["python", "twitter_logger.py"]