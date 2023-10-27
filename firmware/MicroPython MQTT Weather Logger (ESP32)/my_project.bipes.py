#Code automatically generated by BIPES (http://www.bipes.net.br)#Author: 'Nerval Junior'#IOT ID: 0#Description: 'My project'import secretsimport ssd1306from machine import Pin, I2Cimport networkimport machineimport timeimport ujsonfrom umqtt.simple import MQTTClientoled_width = 128oled_height = 64i2c_rst = Pin(16, Pin.OUT)i2c_rst.value(0)time.sleep_ms(5)i2c_rst.value(1)i2c_scl = Pin(15, Pin.OUT, Pin.PULL_UP)i2c_sda = Pin(4, Pin.OUT, Pin.PULL_UP)i2c = I2C(scl=i2c_scl, sda=i2c_sda)oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)oled.fill(0)MQTT_CLIENT_ID=secrets.MQTT_CLIENT_IDMQTT_BROKER = secrets.MQTT_BROKERMQTT_USER = secrets.MQTT_USERMQTT_PASSWORD = secrets.MQTT_PASSWORDMQTT_TOPIC = secrets.MQTT_TOPICMQTT_CLIENT_ID = "micropython-weather-demo"MQTT_BROKER = "broker.mqttdashboard.com"MQTT_USER = ""MQTT_PASSWORD = ""MQTT_TOPIC = "wokwi-weather"'''# Configuraes MQTTMQTT_CLIENT_ID = "mqtt"MQTT_BROKER = "192.168.0.14"MQTT_USER = ""MQTT_PASSWORD = ""MQTT_TOPIC = "sala/resistencia"'''SSID = secrets.SSIDPASSWORD = secrets.PASSWORD# Conectar  rede Wi-Fiprint("Connecting to WiFi", end="")sta_if = network.WLAN(network.STA_IF)sta_if.active(True)sta_if.connect(SSID, PASSWORD)connecting_message = "Connecting to WiFi"connecting_dots = ""while not sta_if.isconnected():    connecting_dots += "."    if len(connecting_dots) > 3:        connecting_dots = ""  # Limpa os pontos aps 4 pontos    oled.fill(0)    oled.text(connecting_message, 0, 16)    oled.text("Please wait...", 0, 32)    oled.text(connecting_dots, 0, 48)  # Exibe os pontos no canto inferior direito    oled.show()    print(".", end="")    time.sleep(0.1)print("Connected to WiFi!")# Conectar ao servidor MQTTprint("Connecting to MQTT server... ", end="")client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)client.connect()print(" Connected!")oled.text(sta_if.ifconfig()[0], 0, 0)oled.text("Conectado!", 0, 25)oled.show()potenciometro_pin = machine.Pin(37)adc = machine.ADC(potenciometro_pin)while True:    leitura = adc.read()    print("Leitura do potenciometro")    print("Valor        Volts")    valor_resistencia = leitura * 3.3 / 1023    print("{:<13} {:.2f}".format(leitura, valor_resistencia))    print('$BIPES-DATA:', 11, ',', valor_resistencia)    print('$BIPES-DATA:', 1, ',', leitura)    # Criar e enviar a mensagem MQTT    message = ujson.dumps({"potenciometro": leitura, "resistencia":valor_resistencia})    print("Reporting to MQTT topic {}: {}".format(MQTT_TOPIC, message))    client.publish(MQTT_TOPIC, message)    # Atualizar o OLED com o valor do potencimetro    oled.fill(0)    oled.text("Potenciometro:", 0, 0)    oled.text(str(leitura), 0, 16)    oled.text("Voltage (V):", 0, 32)    oled.text("{:.2f}".format(valor_resistencia), 0, 48)    oled.show()    time.sleep(1)