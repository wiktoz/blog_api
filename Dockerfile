FROM python:3.14-rc-slim-bookworm

WORKDIR /blog_api

COPY . /blog_api

RUN apt-get update && apt-get install build-essential libffi-dev -y

RUN pip install -r requirements.txt
RUN chmod +x /blog_api/start.sh

EXPOSE 5000

ENTRYPOINT ["/blog_api/start.sh"]