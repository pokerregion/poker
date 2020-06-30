FROM chris060986/python-lxml-docker:latest
WORKDIR /tmp

COPY dist/poker*.whl /tmp/poker-0.30.0-py3-none-any.whl

RUN pip install /tmp/poker-0.30.0-py3-none-any.whl
