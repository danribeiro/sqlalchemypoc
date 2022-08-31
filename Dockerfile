FROM python:3.5
ADD . /home/app
WORKDIR /home/app
RUN pip install -r requirements.txt
CMD python app.py