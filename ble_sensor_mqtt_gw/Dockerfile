FROM python:3

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y bluez bluez-tools libglib2.0-dev wget patch && apt-get clean
COPY requirements.txt bluepy-helper.patch ./
RUN pip install --no-cache-dir -r requirements.txt
RUN wget -q https://files.pythonhosted.org/packages/27/91/6cfca10bee9862f93015413cf9e6a52c3081a71f1518963396a055128f8e/bluepy-1.3.0.tar.gz && tar xfz bluepy-1.3.0.tar.gz && patch -d bluepy-1.3.0 -p1 < bluepy-helper.patch && tar cfz bluepy-1.3.0.tar.gz bluepy-1.3.0 && pip install --no-cache-dir ./bluepy-1.3.0.tar.gz

COPY ./ble_sensor_mqtt_gw.py ./ble_sensor_mqtt_gw.py

CMD [ "python", "./ble_sensor_mqtt_gw.py" ]
