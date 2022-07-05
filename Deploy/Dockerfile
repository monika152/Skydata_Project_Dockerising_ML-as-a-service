FROM python:3.10.0

WORKDIR /interstellar

COPY . /interstellar

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python"]

CMD ["app.py", "--host", "0.0.0.0" ]