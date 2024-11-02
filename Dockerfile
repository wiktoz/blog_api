FROM python:3.14-rc-slim-bookworm

WORKDIR /blog_api

COPY . /blog_api

RUN apt-get update && apt-get install -y build-essential libffi-dev libpq-dev

RUN pip install -r requirements.txt
RUN chmod +x /blog_api/start.sh

EXPOSE 5000

ENTRYPOINT ["sh", "/blog_api/start.sh"]