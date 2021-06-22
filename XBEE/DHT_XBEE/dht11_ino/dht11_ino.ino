#include "dht11.h"
#define DHT11PIN 4

dht11 DHT11;

void setup()
{
  Serial.begin(9600);
 
}

char var[10];
char var1[10];
float hum,temp;
String temper(char vars[10])
{
  String v="Temp: ";
  v.concat(vars);
  return v;
}
String humid(char vars[10])
{
  String v="Humi: ";
  v.concat(vars);
  return v;
}
void writeString(String stringData) { // Used to serially push out a String with Serial.write()

  for (int i = 0; i < stringData.length(); i++)
  {
    Serial.write(stringData[i]);// Push each char 1 by 1 on each loop pass
  }

}
String vs;
void loop()
{
  for(int count=1000;count>0;count--)
  {
  Serial.println();
  int chk = DHT11.read(DHT11PIN);
  hum=(float)DHT11.humidity;
  temp=(float)DHT11.temperature;

  dtostrf(hum,3,3,var);
  dtostrf(temp,3,3,var1);
  
  delay(1000);
  if(count%2==0)
  {
  vs=temper(var1);
  writeString(vs);
  }
  else{
    vs=humid(var);
    writeString(vs);
  }
  delay(1500);
  }
}
