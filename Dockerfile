FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./setup.py /code/setup.py
COPY ./larvaecount /code/larvaecount
COPY ./MANIFEST.in /code/MANIFEST.in

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install -e /code

CMD ["python3", "-m", "larvaecount.app", "--host=\"0.0.0.0\"", "--port=\"7860\""]
