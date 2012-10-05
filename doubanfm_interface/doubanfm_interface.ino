#include <LiquidCrystal.h> 
#include <Messenger.h>
#include <SoftwareSerial.h>

/*
 * Douban FM interface
 */

// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

SoftwareSerial mySerial(8, 9); // RX, TX

Messenger message = Messenger('^');

// Define the max size of the string
// The size must be big enough to hold the longest string you are expecting
#define MAXSIZE 128 

// Create a char array (string) to hold the received string
char inData[MAXSIZE];

//boolean fmStart = false;

long previousMillis = 0;
long interval = 3000;
 
void setup() {
  // initialize serial:
  mySerial.begin(9600);
  
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  
  //lcd.setCursor(0,0);
  lcd.print("Douban fm box");
  lcd.setCursor(0,1);
  lcd.print("by wolfg");  
  
  message.attach(messageCompleted);
}

void loop() {  
  unsigned long currentMillis = millis();
  
  while (mySerial.available()) {  
    message.process(mySerial.read());     
  }
  
  if (currentMillis - previousMillis > interval) {
    previousMillis = currentMillis;
    // read the input on analog pin 0:
    int channelValue = analogRead(A0);
    //if (mySerial.available()) {
      mySerial.print("tuner: ");
      mySerial.print(channelValue);
      mySerial.println();
    //}
  }
}

void messageCompleted() {
  
  while (message.available()) {
    
    if (message.checkString("fmbox init")) {
      //fmStart = true;
      lcd.clear();
      lcd.print("fmbox init");
    } else {
      //if (fmStart) {
        if (message.checkString("fmbox singer name")) { 
          //lcd.clear();        
          lcd.setCursor(0,1);
          message.copyString(inData,MAXSIZE); 
          lcd.print(inData); 
        } else if (message.checkString("fmbox song name")) {          
          lcd.setCursor(0,0); 
          message.copyString(inData,MAXSIZE); 
          lcd.print(inData);          
        } else if (message.checkString("fmbox clr")) {
            lcd.clear();
        }
      //}
    }
  }  
}

