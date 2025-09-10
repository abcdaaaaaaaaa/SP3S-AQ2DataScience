#include "SP3SAQ2.h"
#include <math.h>

SP3SAQ2::SP3SAQ2(int bitadc, byte pin)
{
  _bitadc = pow(2,bitadc)-1;
  _pin = pin;
}

void SP3SAQ2::begin() {
    pinMode(_pin, INPUT);
}

float SP3SAQ2::read() {
    int adc = analogRead(_pin);
    float SensorVal = (float)adc / (float)_bitadc;
    return SensorVal;
}

float SP3SAQ2::fmap(float x, float in_min, float in_max, float out_min, float out_max) {
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min; // Arduino ide's map function does not support float structure.
}

float SP3SAQ2::inverseYaxb(float a, float y, float b) {
    return pow(y / a, 1.0 / b);
}

float SP3SAQ2::limit(float value, float minVal, float maxVal) {
    if (value < minVal) return minVal;
    if (value > maxVal) return maxVal;
    return value;
}

float SP3SAQ2::calculateppm(float sensorVal, int idx) {
    float calValue, a_gas, b_gas;
    float ratio = (calValue * (sensorVal - 1)) / (sensorVal * (calValue - 1));
    
    switch (idx) {
        case 0: // Methane
            if (ratio > 0.952) { a_gas = 1.1086; b_gas = -0.0448; }
            else if (ratio <= 0.952 && ratio > 0.94) { a_gas = 0.9867; b_gas = -0.0105; }
            else if (ratio <= 0.94 && ratio > 0.906) { a_gas = 1.097; b_gas = -0.0335; }
            else if (ratio <= 0.906 && ratio > 0.878) { a_gas = 1.0513; b_gas = -0.0261; }
            else if (ratio <= 0.878 && ratio > 0.842) { a_gas = 1.1424; b_gas = -0.0381; }
            else if (ratio <= 0.842) { a_gas = 2.2563; b_gas = -0.1231; }
            break;

        case 1: // IsoButane
            if (ratio > 0.821) { a_gas = 1.0725; b_gas = -0.0786; } 
            else if (ratio <= 0.821 && ratio > 0.658) { a_gas = 1.5342; b_gas = -0.1838; }
            else if (ratio <= 0.658 && ratio > 0.514) { a_gas = 1.8529; b_gas = -0.2248; }
            else if (ratio <= 0.514 && ratio > 0.351) { a_gas = 3.1315; b_gas = -0.3168; }
            else if (ratio <= 0.351 && ratio > 0.231) { a_gas = 4.8725; b_gas = -0.3808; }
            else if (ratio <= 0.231) { a_gas = 4.0796; b_gas = -0.3586; }
            break;

        case 2: // CO
            if (ratio > 0.658) { a_gas = 1.4117; b_gas = -0.2244; }
            else if (ratio <= 0.658 && ratio > 0.428) { a_gas = 2.2176; b_gas = -0.3572; }
            else if (ratio <= 0.428 && ratio > 0.274) { a_gas = 2.7757; b_gas = -0.406; }
            else if (ratio <= 0.274 && ratio > 0.148) { a_gas = 5.0696; b_gas = -0.5116; }
            else if (ratio <= 0.148 && ratio > 0.084) { a_gas = 5.2111; b_gas = -0.5156; }
            else if (ratio <= 0.084) { a_gas = 3.0264; b_gas = -0.4477; }
            break;

        case 3: // Ethanol
            if (ratio > 0.554) { a_gas = 1.6105; b_gas = -0.3138; }
            else if (ratio <= 0.554 && ratio > 0.303) { a_gas = 3.0468; b_gas = -0.5012; }
            else if (ratio <= 0.303 && ratio > 0.148) { a_gas = 6.1074; b_gas = -0.6522; }
            else if (ratio <= 0.148 && ratio > 0.067) { a_gas = 6.3217; b_gas = -0.6583; }
            else if (ratio <= 0.067 && ratio > 0.042) { a_gas = 1.2629; b_gas = -0.4251; }
            else if (ratio <= 0.042) { a_gas = 1.0192; b_gas = -0.3983; }
            break;

        case 4: // Hydrogen
            if (ratio > 0.444) { a_gas = 1.5579; b_gas = -0.3691; }
            else if (ratio <= 0.444 && ratio > 0.237) { a_gas = 2.6156; b_gas = -0.5214; }
            else if (ratio <= 0.237 && ratio > 0.139) { a_gas = 2.2189; b_gas = -0.4857; }
            else if (ratio <= 0.139 && ratio > 0.07) { a_gas = 3.5841; b_gas = -0.5698; }
            else if (ratio <= 0.07 && ratio > 0.05) { a_gas = 0.5806; b_gas = -0.3063; }
            else if (ratio <= 0.05) { a_gas = 0.2205; b_gas = -0.1853; }
            break;
    }
    
    float calAir = inverseYaxb(a_gas, 0.666, b_gas);
    if (idx == 0) calValue = 0.03167312;
    else if (idx == 4) calValue = 0.001;
    else calValue = fmap(calAir, 10, 10000, 0, 1);
  
    return limit(inverseYaxb(a_gas, ratio, b_gas), 0, 10000);
}

float SP3SAQ2::exponential_interpolate(float x, float x_min, float x_max, float ppm_min, float ppm_max) {
    float log_min = log10(ppm_min);
    float log_max = log10(ppm_max);
    float ratio = (float)(x - x_min) / (x_max - x_min);
    float log_val = log_min + ratio * (log_max - log_min);
    return pow(10, log_val);
}

float SP3SAQ2::airConcentration(float sensorVal) {
    return exponential_interpolate(sensorVal, 0, 1, 2, 5);
}

