FROM python:2
#RUN apt-get update && apt-get install -y python-dev
COPY . /usr/src/featherbot
WORKDIR /usr/src/featherbot/featherduster/
RUN apt-get update && apt-get install libgmp3-dev -y
RUN python setup.py install
RUN pip install slackbot
WORKDIR /usr/src/featherbot
CMD [ "python", "./featherbot.py" ]
