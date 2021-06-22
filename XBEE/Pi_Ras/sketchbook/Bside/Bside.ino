char var[10];
void setup()
{
  Serial.begin(9600);
}
void loop()
{
  unsigned long st;
  st=millis();
  while((Serial.available()<11) && ((millis()-st)<1500))
  {
  }
  if(Serial.available()<11)
  {
    Serial.println("ERROR");
  }
  else
  {
    for(int i=0;i<10;i++)
    {
      var[i]=Serial.read();
    }
    Serial.println(var);
  }
}
