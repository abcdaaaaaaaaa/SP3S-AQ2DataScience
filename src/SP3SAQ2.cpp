#include "SP3SAQ2.h"
#include <math.h>

SP3SAQ2::SP3SAQ2(int bitadc, byte pin)
{
  _bitadc = pow(2,bitadc)-1;
  _pin = pin;
}

struct GasData { float a, b; };

GasData gases[] = {
    {1.1034, -0.0377 }, // Methane
    {1.583,  -0.214  }, // IsoButane
    {1.9582, -0.3468 }, // CO
    {2.2885, -0.4504 }, // Ethanol
    {1.8967, -0.4468 }  // Hydrogen
};

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
    GasData g = gases[idx];
    float calValue;
    float calAir = inverseYaxb(g.a, 0.666, g.b);
    if (idx == 0) calValue = 0.03167312;
    else if (idx == 4) calValue = 0.001;
    else calValue = fmap(calAir, 10, 10000, 0, 1);
    float ratio = (calValue * (sensorVal - 1)) / (sensorVal * (calValue - 1));
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
