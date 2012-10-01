/*
 * Douban FM interface
 */

#include <LiquidCrystal.h> 
#include <Messenger.h>

// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

Messenger message = Messenger('^');

// Define the max size of the string
// The size must be big enough to hold the longest string you are expecting
#define MAXSIZE 20 

// Create a char array (string) to hold the received string
char inData[MAXSIZE];
String msg;

boolean fmStart = false;
int channelValue = 0;

void messageCompleted() {
  
  //Serial.print("tunner: ");
  
  //Serial.print(channelValue);
  
  while (message.available()) {
    
    if (message.checkString("fmbox init")) {
      fmStart = true;
      lcd.clear();
      lcd.print("fmbox init");
    } else {
      if (fmStart) {
        boolean skip = false;
        if (message.checkString("fmbox singer")) { 
          lcd.clear();        
          lcd.setCursor(0,1);
        } else if (message.checkString("fmbox song name")) {          
          lcd.setCursor(0,0);          
        } else {
          skip = true;
          if (message.checkString("fmbox clr")) {
            lcd.clear();
          }
        }
        if (!skip) {
          message.copyString(inData,MAXSIZE); 
          lcd.print(inData);   
        }
      }
    }
  }  
}
 
void setup() {
  // initialize serial:
  Serial.begin(9600);
  
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  
  lcd.setCursor(0,0);
  lcd.print("Douban fm box");
  lcd.setCursor(0,1);
  lcd.print("by wolfg");  
  
  message.attach(messageCompleted);
}

void loop() {  
  // read the input on analog pin 0:
  channelValue = analogRead(A0);
  
  while (Serial.available()) {    
    message.process(Serial.read());     
  }
  
  //Serial.print("tunner: ");
  //Serial.println(channelValue);
  //delay(1);
}