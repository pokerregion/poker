FROM python:3-alpine
WORKDIR /tmp

COPY dist/poker*.whl /tmp/poker-0.30.0-py3-none-any.whl

RUN apk add --update --no-cache g++ gcc libxslt-dev

RUN pip install /tmp/poker-0.30.0-py3-none-any.whl

CMD ["poker"]
