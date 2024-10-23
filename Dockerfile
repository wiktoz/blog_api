FROM python:3.14-rc-slim-bookworm

WORKDIR /blog_api

COPY . /blog_api

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]