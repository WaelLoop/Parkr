char serialData;
int led1 = 2;
int led2 = 4;
int led3 = 6;
void setup() {
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(led3, OUTPUT);
  Serial.begin(9600);
  // put your setup code here, to run once:
  // They are free at first
  digitalWrite(led1,HIGH);
  digitalWrite(led2,HIGH);
  digitalWrite(led3,HIGH);

}

void loop() {
  if(Serial.available()>0){
    serialData= Serial.read();
    Serial.print(serialData);
  
    // Light 1
    if(serialData == '1') {
      digitalWrite(led1,HIGH);
    }
    else if(serialData == '0'){
      digitalWrite(led1, LOW);
    }
  
    //Light 2
    if(serialData == '3'){
      digitalWrite(led2,HIGH);
    }
    else if(serialData == '2'){
      digitalWrite(led2, LOW);
    }
    
    //Light 3
    if(serialData == '5') {
      digitalWrite(led3,HIGH);
    }
    else if(serialData == '4'){
      digitalWrite(led3, LOW);
    }
  
  }
}
  
  
  // put your main code here, to run repeatedly:
 

 
