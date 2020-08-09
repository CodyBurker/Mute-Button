// constants won't change. They're used here to set pin numbers:
const int BUTTON_PIN = 7;       // the number of the pushbutton pin
const int RED_LIGHT_PIN= 2; // Red light pin

// Variables will change:
int lastState = LOW;  // the previous state from the input pin
int buttonState;                // the current reading from the input pin
int lastButtonState = LOW;   // the previous reading from the input pin


// the following variables are unsigned longs because the time, measured in
// milliseconds, will quickly become a bigger number than can be stored in an int.
unsigned long lastDebounceTime = 0;  // the last time the output pin was toggled
unsigned long debounceDelay = 10;    // the debounce time; increase if the output flickers

String rcdState = "off"; // Set the state recieved via Serial to Low

void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  // initialize the pushbutton pin as an pull-up input
  // the pull-up input pin will be HIGH when the switch is open and LOW when the switch is closed.
  pinMode(BUTTON_PIN, INPUT);
  pinMode(RED_LIGHT_PIN, OUTPUT);
}

void loop() {
 // read the state of the switch into a local variable:
  int reading = digitalRead(BUTTON_PIN);
  
// If the switch changed, due to noise or pressing:
  if (reading != lastButtonState) {
    // reset the debouncing timer
    lastDebounceTime = millis();
    lastButtonState=reading;
  }

//  String state = "buttonState:\t" + buttonState ;
//  state = state + ", lastButtonState:\t" ;
//  state = state + lastButtonState;
//  state = state + ", lastDebounceTime:\t";
//  state = state + lastDebounceTime;;
//  Serial.println(state);

  if ((millis() - lastDebounceTime) > debounceDelay) {
    // whatever the reading is at, it's been there for longer than the debounce
    // delay, so take it as the actual current state:
    // if the button state has changed:
    if (reading != buttonState) {
      buttonState = reading;
      
      // only toggle the LED if the new button state is HIGH
      if (buttonState == LOW) {
        Serial.println("Toggle");
        digitalWrite(RED_LIGHT_PIN,LOW);
      }
    }
  }
  
  // Check if data is recieved
  if(Serial.available() >0){
    rcdState = Serial.readString();
    int light_state=LOW;
    if(rcdState=="off"){
      light_state=LOW;
    }
    if(rcdState=="on"){
      light_state=HIGH;
    }
    digitalWrite(RED_LIGHT_PIN,light_state);
  }
}
