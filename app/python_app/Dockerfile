FROM python:3

WORKDIR app

COPY app/ app/

RUN pip install -r app/requirements.txt


EXPOSE 5000

CMD ["python", "app/app.py"]