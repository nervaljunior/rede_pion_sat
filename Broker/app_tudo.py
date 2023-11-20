from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import FastAPI
import paho.mqtt.client as mqtt
import requests


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://193.203.174.233:3033/set_log"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


mqtt_broker = "test.mosquitto.org"
mqtt_port = 1883
mqtt_topic = "sala/resistencia"

received_data = {}


class MqttData(BaseModel):
    data: str


i=0

def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    received_data[mqtt_topic] = payload
    print(f"Received MQTT data on topic {mqtt_topic}: {payload}")
    global i
    if i==10 :
        dados={"client":3 ,"dado":received_data}
        
        response=requests.post("http://193.203.174.233:3033/set_log",json=dados)
        
        print(response.json)
        i==0
    print(i)
    i+=1


mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect(mqtt_broker, mqtt_port)
mqtt_client.subscribe(mqtt_topic)
mqtt_client.loop_start()


@app.get('/get_data')
async def get_mqtt_data():   
    return {
        "Mensagem_MQTT": received_data.get(mqtt_topic, "Nenhum dado recebido via MQTT")
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


