#include <ArduinoJson.h>
#include "DHT.h"
#define DHTPIN 2 
#define DHTTYPE DHT11

DHT dht(DHTPIN,DHTTYPE);
  
const int capacity = JSON_OBJECT_SIZE(4);
StaticJsonBuffer<capacity> jb;
JsonObject& obj = jb.createObject();

void setup() {
    Serial.begin(9600);
    dht.begin();
}

void loop() {
    delay(1000);

    float t = dht.readTemperature();
    float h = dht.readHumidity();
    float hic = dht.computeHeatIndex(t,h,false);
    bool error = true;

    if (isnan(h) || isnan(t)) {
    error = false;
    return;
    }

    obj.set("Temperature", t);
    obj.set("Humidity", h);
    obj.set("Heat index", hic);
    obj.set("Validity", error);

    obj.prettyPrintTo(Serial);
}
