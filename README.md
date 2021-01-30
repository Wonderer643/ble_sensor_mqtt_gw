# ble_sensor_mqtt_gw

Python based simlpe BLE->MQTT gateway for scanning the nearby devices and reading advertising data in case the device address match.

Reads advertising data of custom ESP32 sensor (see ble_esp_sensor_advert_conn repository) and Xiaomi Clear Glass sensor.

On reading the advertising data format the output to simple JSON containing "UserInformation": <sensor_characteric_like_Temperature> and "Value": <sensor_value> and output to the MQTT broker. MQTT topic is build as "sensor/<Device_Address>/<sensor_characteric_like_Temperature>"

Run as a standalone script. Also a Dockerfile provide, to run as docker image.
