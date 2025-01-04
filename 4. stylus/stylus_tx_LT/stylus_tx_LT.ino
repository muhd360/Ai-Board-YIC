#include <VirtualWire.h>

#define buttonPinA 6 // Button to send command 'a'
#define buttonPinB 7 // Button to send command 'b'
#define buttonPinC 8 // Button to send command 'c'

void setup()
{
    Serial.begin(9600); // Initialize serial communication
    vw_set_tx_pin(12);  // Set the TX pin
    vw_setup(2000);     // Bits per second for RF communication

    pinMode(buttonPinA, INPUT_PULLUP); // Configure buttons as input with pull-up resistors
    pinMode(buttonPinB, INPUT_PULLUP);
    pinMode(buttonPinC, INPUT_PULLUP);
}

void loop()
{
    char message[2] = ""; // Array to hold the message (1 char + null terminator)

    // Check button presses and send corresponding commands
    if (digitalRead(buttonPinA) == LOW) // Button A pressed
    {
        message[0] = 'a';
        vw_send((uint8_t *)message, strlen(message));
        vw_wait_tx(); // Wait until the message is sent
        Serial.println("Sent: a");
        delay(500); // Debounce delay
    }
    else if (digitalRead(buttonPinB) == LOW) // Button B pressed
    {
        message[0] = 'b';
        vw_send((uint8_t *)message, strlen(message));
        vw_wait_tx(); // Wait until the message is sent
        Serial.println("Sent: b");
        delay(500); // Debounce delay
    }
    else if (digitalRead(buttonPinC) == LOW) // Button C pressed
    {
        message[0] = 'c';
        vw_send((uint8_t *)message, strlen(message));
        vw_wait_tx(); // Wait until the message is sent
        Serial.println("Sent: c");
        delay(500); // Debounce delay
    }
}
