import paho.mqtt.client as mqtt
import requests
import json

# Configurações MQTT
mqtt_broker = "test.mosquitto.org"
mqtt_port = 1883
mqtt_topic = "/messages"

# Configurações da API REST
api_url="http://193.203.174.233:3033"
api_endpoint="/set_log"
api_headers = {"Content-Type": "application/json"}

# Callback para lidar com mensagens MQTT recebidas
def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    print(f"Mensagem MQTT recebida: {payload}")

    # Enviar os dados para a API REST
    enviar_para_api(payload)

# Função para enviar dados para a API REST via POST
def enviar_para_api(data):
    try:
        # Montar os dados da requisição
        payload = {
        "client": 10,
        "dados": data}

        # Enviar a solicitação POST para a API REST
        response = requests.post(api_url + api_endpoint, data=json.dumps(payload), headers=api_headers)

        # Verificar o código de status da resposta
        if response.status_code == 200:
            print("Dados enviados com sucesso para a API REST.")
        else:
            print(f"Falha ao enviar dados para a API REST. Código de status: {response.status_code}")
    except Exception as e:
        print(f"Erro ao enviar dados para a API REST: {str(e)}")

# Configurar o cliente MQTT
client = mqtt.Client()
client.on_message = on_message

# Conectar ao broker MQTT
client.connect(mqtt_broker, mqtt_port, 60)

# Subscrever ao tópico MQTT
client.subscribe(mqtt_topic)

# Loop para manter a conexão MQTT ativa
client.loop_forever()
