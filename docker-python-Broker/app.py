import paho.mqtt.client as mqtt
import requests
import json


mqtt_broker = "mosquitto"
mqtt_port = 1883
mqtt_topic = "/messages"

api_url="http://193.203.174.233:3033"
api_endpoint="/set_log"
api_headers = {"Content-Type": "application/json"}

def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    print(f"Mensagem MQTT recebida: {payload}")

    enviar_para_api(payload)

def enviar_para_api(data):
    try:
        payload = {
        "client": 10,
        "dados": data}

        response = requests.post(api_url + api_endpoint, data=json.dumps(payload), headers=api_headers)

        if response.status_code == 200:
            print("Dados enviados com sucesso para a API REST.")
        else:
            print(f"Falha ao enviar dados para a API REST. Código de status: {response.status_code}")
    except Exception as e:
        print(f"Erro ao enviar dados para a API REST: {str(e)}")

client = mqtt.Client()
client.on_message = on_message

client.connect(mqtt_broker, mqtt_port, 60)

client.subscribe(mqtt_topic)

client.loop_forever()
