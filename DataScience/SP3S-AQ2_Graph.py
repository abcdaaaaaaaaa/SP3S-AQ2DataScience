import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.colors as pc

SensorName = 'SP3S-AQ2'
Air = 1
CleanAir = 0.666
CalibrateAir = CleanAir
MinAirPpm = 2
MaxAirPpm = 5
SensorRLCalRL = 1

gas_params = [
    {'name': 'Methane', 'ppmvals': (10, 10000), 'ppm': (1.1034, -0.0377), 'calvalue': 0.03167312},
    {'name': 'IsoButane', 'ppmvals': (10, 10000), 'ppm': (1.583, -0.214)},
    {'name': 'CO', 'ppmvals': (10, 10000), 'ppm': (1.9582, -0.3468)},
    {'name': 'Ethanol', 'ppmvals': (10, 10000), 'ppm': (2.2885, -0.4504)},
    {'name': 'Hydrogen', 'ppmvals': (10, 10000), 'ppm': (1.8967, -0.4468), 'calvalue': 0.001}
]

def interpolate(value, old_min, old_max, new_min, new_max):
    return (value - old_min) * (new_max - new_min) / (old_max - old_min) + new_min

def yaxb(valuea, value, valueb):
    return valuea * np.power(value, valueb)

def inverseyaxb(valuea, value, valueb):
    return np.power(value / valuea, 1 / valueb)

def vals(minval, maxval, count):
    return np.linspace(minval, maxval, count)

def ppmLimits():
    minvalue = SensorRLCalRL * Air * CalValue / (-maxratio * CalValue + maxratio + SensorRLCalRL * Air * CalValue)
    maxvalue = SensorRLCalRL * Air * CalValue / (-minratio * CalValue + minratio + SensorRLCalRL * Air * CalValue)
    sensitivity = 100
    if maxvalue <= minvalue:
        sensitivity = 1
        maxvalue = minvalue
    else:
        print(f"{gasname}: {CalValue}")
        print(sensitivity, minvalue, maxvalue)
    return sensitivity, minvalue, maxvalue

def ppm(valuea, valueb, ratio):
    return inverseyaxb(valuea, ratio, valueb)

def SensorppmModels(valuea, valueb, SensorValue):
    SensorRatio_value = SensorRLCalRL * Air * CalValue * (SensorValue - 1) / (SensorValue * (CalValue - 1))
    return inverseyaxb(valuea, SensorRatio_value, valueb)

fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=[f"Ratio", f"Sensor"]
)
    
color_palette = pc.qualitative.Plotly

for i, gas in enumerate(gas_params):
    minair, maxair = gas['ppmvals']
    gasname = gas['name']
    valuea, valueb = gas['ppm']
    
    minratio = yaxb(valuea, maxair, valueb)
    maxratio = yaxb(valuea, minair, valueb)
    
    calAir = inverseyaxb(valuea, CalibrateAir, valueb)
    try: CalValue = gas['calvalue']
    except Exception: CalValue = interpolate(calAir, minair, maxair, 0, 1)

    minair, maxair = minair, maxair

    sensitivity, minvalue, maxvalue = ppmLimits()
    ratio_vals = vals(minratio, maxratio, 100)

    SensorValue_vals = vals(minvalue, maxvalue, 100)
    
    color = color_palette[i % len(color_palette)]
    
    ppm_surface_ratio = [ppm(valuea, valueb, ratio) for ratio in ratio_vals]
    fig.add_trace(go.Scatter(
        x=ratio_vals,
        y=ppm_surface_ratio,
        mode='lines',
        name=f"{gasname} Ratio",
        line=dict(color=color)
    ), row=1, col=1)
    
    ppm_surface_sensor = [SensorppmModels(valuea, valueb, SensorValue) for SensorValue in SensorValue_vals]
    fig.add_trace(go.Scatter(
        x=SensorValue_vals,
        y=ppm_surface_sensor,
        mode='lines',
        name=f"{gasname} Sensor",
        line=dict(color=color)
    ), row=1, col=2)
    

fig.update_layout(
    title=f"PPM Diagrams for {SensorName} Gases",
    xaxis=dict(title='X: Ratio'),
    yaxis=dict(title='Y: Ratio Ppm'),
    xaxis2=dict(title='X: SensorValue'),
    yaxis2=dict(title='Y: Sensor Ppm'),
    template='plotly_dark'
)

fig.write_html(f"{SensorName}_gases_ppm.html")
