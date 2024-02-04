# read the doc: https://huggingface.co/docs/hub/spaces-sdks-docker
# you will also find guides on how best to write your Dockerfile

FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./setup.py /code/setup.py
COPY ./eggcount /code/eggcount
COPY ./MANIFEST.in /code/MANIFEST.in

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install -e /code

CMD ["python3", "-m", "eggcount.app", "--host=\"0.0.0.0\"", "--port=\"7860\""]
