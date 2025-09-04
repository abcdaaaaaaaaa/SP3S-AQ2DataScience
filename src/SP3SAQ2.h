#ifndef SP3SAQ2_H
#define SP3SAQ2_H

#include <Arduino.h>

class SP3SAQ2 {
public:
    SP3SAQ2(int bitadc, byte pin);
    void begin();
    float read();
    float calculateppm(float sensorVal, int idx);
    float exponential_interpolate(float x, float x_min, float x_max, float ppm_min, float ppm_max);
    float airConcentration(float sensorVal);

private:
    byte _pin;
    int _bitadc;
    float fmap(float x, float in_min, float in_max, float out_min, float out_max);
    float inverseYaxb(float a, float y, float b);
    float limit(float value, float minVal, float maxVal);
};

#endif
