#include <WiFi.h>
#include <PubSubClient.h>

// Configurações WiFi e MQTT
const char* ssid = "Cobertura";
const char* password = "Dev@!2024";
const char* mqtt_server = "10.0.0.97";
const int mqtt_port = 1885;
const char* mqtt_topic = "ComandoVoz";

// Pines dos LEDs
#define LED_1 13
#define LED_2 27
#define LED_3 33

WiFiClient espClient;
PubSubClient client(espClient);

// Função para conectar ao WiFi
void connectWiFi() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConectado ao WiFi");
}

// Função para reconectar ao MQTT se desconectado
void reconnectMQTT() {
  while (!client.connected()) {
    Serial.print("Tentando se conectar ao MQTT...");
    if (client.connect("ESP32Client")) {
      Serial.println("Conectado ao MQTT");
      client.subscribe(mqtt_topic);  // Inscreve-se no tópico
    } else {
      Serial.print("Falhou, rc=");
      Serial.print(client.state());
      delay(2000);
    }
  }
}

// Callback para processar mensagens recebidas
void callback(char* topic, byte* payload, unsigned int length) {
  String mensagem = "";
  for (unsigned int i = 0; i < length; i++) {
    mensagem += (char)payload[i];
  }
  Serial.print("Mensagem recebida: ");
  Serial.println(mensagem);

  // Controle dos LEDs
  if (mensagem == "1") digitalWrite(LED_1, HIGH);
  else if (mensagem == "0") digitalWrite(LED_1, LOW);
  else if (mensagem == "2") digitalWrite(LED_2, HIGH);
  else if (mensagem == "3") digitalWrite(LED_2, LOW);
  else if (mensagem == "4") digitalWrite(LED_3, HIGH);
  else if (mensagem == "5") digitalWrite(LED_3, LOW);
  else if (mensagem == "6") {
    // Liga os 3 LEDs
    digitalWrite(LED_1, HIGH);
    digitalWrite(LED_2, HIGH);
    digitalWrite(LED_3, HIGH);
    Serial.println("Comando enviado: Ligar todos os LEDs");
  }
  else if (mensagem == "7") {
    // Desliga os 3 LEDs
    digitalWrite(LED_1, LOW);
    digitalWrite(LED_2, LOW);
    digitalWrite(LED_3, LOW);
    Serial.println("Comando enviado: Desligar todos os LEDs");
  }
}

void setup() {
  Serial.begin(115200);

  pinMode(LED_1, OUTPUT);
  pinMode(LED_2, OUTPUT);
  pinMode(LED_3, OUTPUT);

  connectWiFi();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnectMQTT();
  }
  client.loop();
}
