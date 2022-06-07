#include "DHT.h"        // including the library of DHT11 temperature and humidity sensor
#define DHTTYPE DHT11   // DHT 11
#include "Fetch.h"
#include "recipes/WiFi.h"
#include <stdlib.h>

#include <SPI.h>
#include <Wire.h>

#define SSID "TIM-29283289"
#define PASSPHRASE "Ma?12nean#"

#define sensor    A0

int gasLevel = 0;         //int variable for gas level
String quality ="";

const unsigned long SECOND = 1000;
const unsigned long HOUR = 3600*SECOND;
int wait = 1000;

#define dht_dpin 2
DHT dht(dht_dpin, DHTTYPE); 
void setup(void) {
  Serial.begin(9600);
  connectWiFi(SSID, PASSPHRASE);

  pinMode(sensor,INPUT);
  
  dht.begin();
  delay(700);
}

int comp(const void *cmp1, const void *cmp2) {
  int a = *((int *)cmp1);
  int b = *((int *)cmp2);

  return a > b ? 1 : (a < b ? -1 : 0);
}

void loop() {
    Response response;
    char url[100];
    int gas[5] = {0}, i;
    float h;
    float t;

    do {
      h = dht.readHumidity();
    } while(h != h);
    do {
      t = dht.readTemperature();
    } while(t != t);

    for (i = 0; i < 5; i++) {
      gas[i] = analogRead(sensor);
      delay(500);
    }
    qsort(gas, 5, sizeof(int), comp);
    gasLevel = gas[2];

    if(gasLevel<181){
      quality = "  GOOD!";
    } else if (gasLevel >181 && gasLevel<225){
      quality = "  Poor!";
    } else if (gasLevel >225 && gasLevel<300){
      quality = "Very bad!";
    } else if (gasLevel >300 && gasLevel<350){
      quality = "ur dead!";
    }else{
      quality = " Toxic";   
    }
           
    Serial.print("Current humidity = ");
    Serial.print(h);
    Serial.print("%  ");
    Serial.print("temperature = ");
    Serial.print(t);
    Serial.print("C  ");
    Serial.print("quality = ");
    Serial.print(gasLevel);
    Serial.println(quality);

    sprintf(url,"https://aq-heroku.herokuapp.com/saveData/%f/%f/%d", t, h, gasLevel);

    if (wait == 0) {
      do {
        RequestOptions options;
        options.method = "GET";
        response = fetch(url, options);
      } while (response.text() != "true");

      for (int i = 0; i < 8; i++) {
        delay(15 * (60 * SECOND));
        Serial.println("waited");
      }
    } else {
      wait -= 1;
      delay(500);
    }
}
