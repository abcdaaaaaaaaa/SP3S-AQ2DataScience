// (1) The library also supports data science applications such as gradient ppm's Slope Estimation from Python!:
// (1) https://github.com/abcdaaaaaaaaa/SP3S-AQ2DataScience/blob/main/DataScience/

#include <SP3SAQ2.h>

#define ADC_BIT_RESU (12) // for ESP32
#define pin          (35) // D35 (ADC1)

float sensorVal, Air, Methane, IsoButane, CO, Ethanol, Hydrogen;

SP3SAQ2 sensor(ADC_BIT_RESU, pin);

void setup() {
    Serial.begin(115200); // for ESP32
    sensor.begin(); 
	  // WARNING: To get accurate results, please use the resistance 10kΩ (RL) value! 
	  // otherwise the results will not reflect the truth
}

void loop() {
    sensorVal = sensor.read();
    
  	Air = sensorVal > 0 ? sensor.airConcentration(sensorVal) : 0;

    Serial.print("Air: ");
    Serial.println(Air);
    Serial.println();
        
    Methane = sensor.calculateppm(sensorVal, 0);
    IsoButane = sensor.calculateppm(sensorVal, 1);
    CO = sensor.calculateppm(sensorVal, 2);
    Ethanol = sensor.calculateppm(sensorVal, 3);
    Hydrogen = sensor.calculateppm(sensorVal, 4);
      
    Serial.println();
    Serial.print("Methane: ");
    Serial.println(Methane);
    Serial.print("IsoButane: ");
    Serial.println(IsoButane);
    Serial.print("CO: ");
    Serial.println(CO);
    Serial.print("Ethanol: ");
    Serial.println(Ethanol);
    Serial.print("Hydrogen: ");
    Serial.println(Hydrogen);
      
    Serial.println("----------");
    delay(5000); // You can customize the waiting time according to the sensor you use.
}

