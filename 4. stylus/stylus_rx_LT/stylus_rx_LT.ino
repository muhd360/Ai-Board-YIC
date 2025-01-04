#include <VirtualWire.h>

#define ledPinA 2
#define ledPinB 3
#define ledPinC 4

void setup()
{
    Serial.begin(9600); // Initialize serial communication
    vw_set_rx_pin(11);
    vw_setup(2000);
    pinMode(ledPinA, OUTPUT);
    pinMode(ledPinB, OUTPUT);
    pinMode(ledPinC, OUTPUT);
    vw_rx_start();
}

void loop()
{
    uint8_t buf[VW_MAX_MESSAGE_LEN];
    uint8_t buflen = VW_MAX_MESSAGE_LEN;

    if (vw_get_message(buf, &buflen)) // Check if a message is received
    {
        Serial.print("Received: ");
        for (uint8_t i = 0; i < buflen; i++)
        {
            Serial.print((char)buf[i]); // Print each character of the received message
        }
        Serial.println(); // Add a newline for better readability

        // Process the received message
        if (buflen > 0)
        {
            switch (buf[0])
            {
            case 'a':
                digitalWrite(ledPinA, HIGH);
                digitalWrite(ledPinB, LOW); // Turn off other LEDs
                digitalWrite(ledPinC, LOW);
                Serial.println("LED A is ON");
                break;

            case 'b':
                digitalWrite(ledPinB, HIGH);
                digitalWrite(ledPinA, LOW); // Turn off other LEDs
                digitalWrite(ledPinC, LOW);
                Serial.println("LED B is ON");
                break;

            case 'c':
                digitalWrite(ledPinC, HIGH);
                digitalWrite(ledPinA, LOW); // Turn off other LEDs
                digitalWrite(ledPinB, LOW);
                Serial.println("LED C is ON");
                break;

            default:
                Serial.println("Unknown command received.");
                break;
            }
        }
    }
}
