#include <Adafruit_AHTX0.h>
#include <Adafruit_BMP280.h>
#include <SSD1306Wire.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "WiFi.h"
#include "AsyncUDP.h"

const char * ssid = "MTSRouter-001957";
const char * password = "PL3TNH9U";

char s[30];

double temperature;
double humidity;
double pressure;
int i;
char tempStr[10] = "";
char humStr[10] = "";
char presStr[10] = "";
char sendTemp[10];
char sendHum[10];
char sendPres[10];

SSD1306Wire display(0x3c, 21, 22);

//String  humStr, presStr;

Adafruit_AHTX0 aht;
Adafruit_BMP280 bmp;
AsyncUDP udp;

Adafruit_Sensor *aht_hum, *aht_temp, *bmp_pres;

void setup() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  aht.begin();
  bmp.begin(BMP280_ADDRESS_ALT, BMP280_CHIPID);
  display.init();
  
  udp.connect(IPAddress(192,168,1,3), 9000);

  display.flipScreenVertically();
  
  Serial.begin(115200);

    bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
                  Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
                  Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
                  Adafruit_BMP280::FILTER_X16,      /* Filtering. */
                  Adafruit_BMP280::STANDBY_MS_500); /* Standby time. */
  
  aht_temp = aht.getTemperatureSensor();
  aht_temp->printSensorDetails();
  aht_hum = aht.getHumiditySensor();
  aht_hum->printSensorDetails();
  bmp_pres = bmp.getPressureSensor();
  bmp_pres->printSensorDetails();

}

double roundation (double x){
  x = x*10;
  x = round(x);
  x = x/10;
  return x;
}

void loop() {  
  sensors_event_t temp;
  sensors_event_t pres;
  sensors_event_t hum;
  aht_temp->getEvent(&temp);
  bmp_pres->getEvent(&pres);
  aht_hum->getEvent(&hum);

  temperature = roundation(temp.temperature);
  dtostrf(temperature,3,1,tempStr);
  strcpy(sendTemp, tempStr);
  strcat(tempStr, " °C");
  
  humidity = hum.relative_humidity;
  while(humidity == 0.0){
    sensors_event_t hum;
    aht_hum->getEvent(&hum);
    humidity = hum.relative_humidity;
    Serial.print(humidity);
    delay(1);
  }
  
  humidity = roundation(humidity);
  dtostrf(humidity,4,1,humStr);
  strcpy(sendHum, humStr);
  strcat(humStr, " %");
  
  pressure = roundation(pres.pressure);
  dtostrf(pressure,5,1,presStr);
  strcpy(sendPres, presStr);
  strcat(presStr, " hPa");
  
  for(i=0; i<50; i++){
    display.clear();
    display.setFont(ArialMT_Plain_16);
    display.drawString(0-i*3,0,"TEMPERATURE");
    display.drawString(150-i*3,0,"HUMIDITY");

    display.setFont(ArialMT_Plain_24);
    display.drawString(0-i*3,30,tempStr);
    display.drawString(150-i*3,30,humStr);
    delay (1);
    display.display();
    }
    
    delay(1000);

    for(i=0; i<50; i++){
    display.clear();
    display.setFont(ArialMT_Plain_16);
    display.drawString(0-i*3,0,"HUMIDITY");
    display.drawString(150-i*3,0,"PRESSURE");

    display.setFont(ArialMT_Plain_24);
    display.drawString(0-i*3,30,humStr);
    display.drawString(150-i*3,30,presStr);
    delay (1);
    display.display();
    }
    
    delay(1000);

    for(i=0; i<50; i++){
    display.clear();
    display.setFont(ArialMT_Plain_16);
    display.drawString(0-i*3,0,"PRESSURE");
    display.drawString(150-i*3,0,"TEMPERATURE");

    display.setFont(ArialMT_Plain_24);
    display.drawString(0-i*3,30,presStr);
    display.drawString(150-i*3,30,tempStr);
    delay (1);
    display.display();
    }

    delay(1000);

    strcpy(s, sendTemp);
    strcat(s, ":");
    strcat(s, sendHum);
    strcat(s, ":");
    strcat(s, sendPres);
    udp.broadcastTo(s, 9000);
    
}
