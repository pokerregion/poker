FROM python:3-alpine
WORKDIR /tmp

COPY dist/ /tmp

RUN python3 setup.py dist_wheel

CMD ["poker"]
