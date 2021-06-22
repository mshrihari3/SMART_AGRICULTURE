char var[15];
void setup()
{
  Serial.begin(9600);
}
void loop()
{
  unsigned long st;
  st=millis();
  while((Serial.available()<17) && ((millis()-st)<2750))//17DHT2750,19-2650
  {
  }
  if(Serial.available()<9)
  {
    Serial.println("NO SERIAL COM, YET!!!");
  }
  else
  {
    for(int i=0;i<14;i++)//14,12
    {
      var[i]=Serial.read();
    }
    Serial.println(var);
  }
}
