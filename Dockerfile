FROM python:3

WORKDIR /usr/src/app

RUN apt-get update 
RUN apt-get install ffmpeg libsm6 libxext6 vim -y
#RUN apt-get install -y apt-utils build-essential bluez bluez-tools python3-dev python3-pip libglib2.0-dev libboost-python-dev libboost-thread-dev libbluetooth-dev
#Fix TimeZone issue.
ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "sh", "./humidifier.sh" ]