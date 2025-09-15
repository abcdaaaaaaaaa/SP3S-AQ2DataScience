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

GasConstants SP3SAQ2::get_constants(int idx, float ratio) {
    GasConstants g;

    switch (idx) {
        case 0: // Methane
            if (ratio > 0.952) { g.a = 1.1086; g.b = -0.0448; }
            else if (ratio > 0.94) { g.a = 0.9867; g.b = -0.0105; }
            else if (ratio > 0.906) { g.a = 1.097; g.b = -0.0335; }
            else if (ratio > 0.878) { g.a = 1.0513; g.b = -0.0261; }
            else if (ratio > 0.842) { g.a = 1.1424; g.b = -0.0381; }
            else { g.a = 2.2563; g.b = -0.1231; }
            break;

        case 1: // IsoButane
            if (ratio > 0.821) { g.a = 1.0725; g.b = -0.0786; }
            else if (ratio > 0.658) { g.a = 1.5342; g.b = -0.1838; }
            else if (ratio > 0.514) { g.a = 1.8529; g.b = -0.2248; }
            else if (ratio > 0.351) { g.a = 3.1315; g.b = -0.3168; }
            else if (ratio > 0.231) { g.a = 4.8725; g.b = -0.3808; }
            else { g.a = 4.0796; g.b = -0.3586; }
            break;

        case 2: // CO
            if (ratio > 0.658) { g.a = 1.4117; g.b = -0.2244; }
            else if (ratio > 0.428) { g.a = 2.2176; g.b = -0.3572; }
            else if (ratio > 0.274) { g.a = 2.7757; g.b = -0.406; }
            else if (ratio > 0.148) { g.a = 5.0696; g.b = -0.5116; }
            else if (ratio > 0.084) { g.a = 5.2111; g.b = -0.5156; }
            else { g.a = 3.0264; g.b = -0.4477; }
            break;

        case 3: // Ethanol
            if (ratio > 0.554) { g.a = 1.6105; g.b = -0.3138; }
            else if (ratio > 0.303) { g.a = 3.0468; g.b = -0.5012; }
            else if (ratio > 0.148) { g.a = 6.1074; g.b = -0.6522; }
            else if (ratio > 0.067) { g.a = 6.3217; g.b = -0.6583; }
            else if (ratio > 0.042) { g.a = 1.2629; g.b = -0.4251; }
            else { g.a = 1.0192; g.b = -0.3983; }
            break;

        case 4: // Hydrogen
            if (ratio > 0.444) { g.a = 1.5579; g.b = -0.3691; }
            else if (ratio > 0.237) { g.a = 2.6156; g.b = -0.5214; }
            else if (ratio > 0.139) { g.a = 2.2189; g.b = -0.4857; }
            else if (ratio > 0.07) { g.a = 3.5841; g.b = -0.5698; }
            else if (ratio > 0.05) { g.a = 0.5806; g.b = -0.3063; }
            else { g.a = 0.2205; g.b = -0.1853; }
            break;
    }

    return g;
}

float SP3SAQ2::calculateppm(float sensorVal, int idx) {
    float calValue;

    GasConstants g = get_constants(idx, 0.666);
    float calAir = inverseYaxb(g.a, 0.666, g.b);
    
    if (idx == 0) calValue = 0.03167312;
    else if (idx == 4) calValue = 0.001;
    else calValue = fmap(calAir, 10, 10000, 0, 1);

    float ratio = (calValue * (sensorVal - 1)) / (sensorVal * (calValue - 1));
    g = get_constants(idx, ratio);

    return limit(inverseYaxb(g.a, ratio, g.b), 0, 10000);
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
