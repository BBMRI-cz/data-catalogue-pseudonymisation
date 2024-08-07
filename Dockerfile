FROM bitnami/python:3.10

RUN mkdir /pseudo-app

WORKDIR /pseudo-app

ADD requirements.txt .
ADD run_pseudonymization_pipeline.py .
ADD pseudonymization/ pseudonymization/
ADD tests/ tests/

RUN pip install -r requirements.txt

USER 1001

CMD ["pytest", "tests"]