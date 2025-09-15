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
    {'name': 'Methane', 'ppmvals': (10, 10000), 'ratio': (0.726, 1), 'calvalue': 0.0533256},
    {'name': 'IsoButane', 'ppmvals': (10, 10000), 'ratio': (0.15, 0.895)},
    {'name': 'CO', 'ppmvals': (10, 10000), 'ratio': (0.049, 0.842)},
    {'name': 'Ethanol', 'ppmvals': (10, 10000), 'ratio': (0.026, 0.782)},
    {'name': 'Hydrogen', 'ppmvals': (10, 10000), 'ratio': (0.04, 0.666), 'calvalue': 0.001}
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

def get_constants(name, ratio):
    a = np.full_like(ratio, np.nan, dtype=float)
    b = np.full_like(ratio, np.nan, dtype=float)
    
    match name:
        case 'Methane':
            cond1 = ratio > 0.952
            cond2 = (ratio <= 0.952) & (ratio > 0.94)
            cond3 = (ratio <= 0.94) & (ratio > 0.906)
            cond4 = (ratio <= 0.906) & (ratio > 0.878)
            cond5 = (ratio <= 0.878) & (ratio > 0.842)
            cond6 = ratio <= 0.842
            
            a[cond1], b[cond1] = 1.1086, -0.0448
            a[cond2], b[cond2] = 0.9867, -0.0105
            a[cond3], b[cond3] = 1.097, -0.0335
            a[cond4], b[cond4] = 1.0513, -0.0261
            a[cond5], b[cond5] = 1.1424, -0.0381
            a[cond6], b[cond6] = 2.2563, -0.1231
            
        case 'IsoButane':
            cond1 = ratio > 0.821
            cond2 = (ratio <= 0.821) & (ratio > 0.658)
            cond3 = (ratio <= 0.658) & (ratio > 0.514)
            cond4 = (ratio <= 0.514) & (ratio > 0.351)
            cond5 = (ratio <= 0.351) & (ratio > 0.231)
            cond6 = ratio <= 0.231
            
            a[cond1], b[cond1] = 1.0725, -0.0786
            a[cond2], b[cond2] = 1.5342, -0.1838
            a[cond3], b[cond3] = 1.8529, -0.2248
            a[cond4], b[cond4] = 3.1315, -0.3168
            a[cond5], b[cond5] = 4.8725, -0.3808
            a[cond6], b[cond6] = 4.0796, -0.3586
            
        case 'CO':
            cond1 = ratio > 0.658
            cond2 = (ratio <= 0.658) & (ratio > 0.428)
            cond3 = (ratio <= 0.428) & (ratio > 0.274)
            cond4 = (ratio <= 0.274) & (ratio > 0.148)
            cond5 = (ratio <= 0.148) & (ratio > 0.084)
            cond6 = ratio <= 0.084
            
            a[cond1], b[cond1] = 1.4117, -0.2244
            a[cond2], b[cond2] = 2.2176, -0.3572
            a[cond3], b[cond3] = 2.7757, -0.406
            a[cond4], b[cond4] = 5.0696, -0.5116
            a[cond5], b[cond5] = 5.2111, -0.5156
            a[cond6], b[cond6] = 3.0264, -0.4477
            
        case 'Ethanol':
            cond1 = ratio > 0.554
            cond2 = (ratio <= 0.554) & (ratio > 0.303)
            cond3 = (ratio <= 0.303) & (ratio > 0.148)
            cond4 = (ratio <= 0.148) & (ratio > 0.067)
            cond5 = (ratio <= 0.067) & (ratio > 0.042)
            cond6 = ratio <= 0.042
            
            a[cond1], b[cond1] = 1.6105, -0.3138
            a[cond2], b[cond2] = 3.0468, -0.5012
            a[cond3], b[cond3] = 6.1074, -0.6522
            a[cond4], b[cond4] = 6.3217, -0.6583
            a[cond5], b[cond5] = 1.2629, -0.4251
            a[cond6], b[cond6] = 1.0192, -0.3983
            
        case 'Hydrogen':
            cond1 = ratio > 0.444
            cond2 = (ratio <= 0.444) & (ratio > 0.237)
            cond3 = (ratio <= 0.237) & (ratio > 0.139)
            cond4 = (ratio <= 0.139) & (ratio > 0.07)
            cond5 = (ratio <= 0.07) & (ratio > 0.05)
            cond6 = ratio <= 0.05
            
            a[cond1], b[cond1] = 1.5579, -0.3691
            a[cond2], b[cond2] = 2.6156, -0.5214
            a[cond3], b[cond3] = 2.2189, -0.4857
            a[cond4], b[cond4] = 3.5841, -0.5698
            a[cond5], b[cond5] = 0.5806, -0.3063
            a[cond6], b[cond6] = 0.2205, -0.1853
            
    return a, b

fig = make_subplots(rows=1, cols=2, subplot_titles=[f"Ratio", f"Sensor"])
color_palette = pc.qualitative.Plotly

for i, gas in enumerate(gas_params):
    minair, maxair = gas['ppmvals']
    gasname = gas['name']
    
    minratio, maxratio = gas['ratio']
    
    valuea, valueb = get_constants(gasname, CalibrateAir)
    calAir = inverseyaxb(valuea, CalibrateAir, valueb)
    
    try: CalValue = gas['calvalue']
    except Exception: CalValue = interpolate(calAir, minair, maxair, 0, 1)
    
    sensitivity, minvalue, maxvalue = ppmLimits()
    ratio_vals = vals(minratio, maxratio, sensitivity)
    
    valuea_ratio, valueb_ratio = get_constants(gasname, ratio_vals)
    ppm_surface_ratio = ppm(valuea_ratio, valueb_ratio, ratio_vals)
    
    color = color_palette[i % len(color_palette)]
    
    fig.add_trace(go.Scatter(x=ratio_vals, y=ppm_surface_ratio, mode='lines', name=f"{gasname} Ratio", line=dict(color=color)), row=1, col=1)
    
    SensorValue_vals = vals(minvalue, maxvalue, sensitivity)
    SensorRatio_vals = SensorRLCalRL * Air * CalValue * (SensorValue_vals - 1) / (SensorValue_vals * (CalValue - 1))
    
    valuea_sensor, valueb_sensor = get_constants(gasname, SensorRatio_vals)
    ppm_surface_sensor = inverseyaxb(valuea_sensor, SensorRatio_vals, valueb_sensor)
    
    fig.add_trace(go.Scatter(x=SensorValue_vals, y=ppm_surface_sensor, mode='lines', name=f"{gasname} Sensor", line=dict(color=color)), row=1, col=2)

fig.update_layout(title=f"PPM Diagrams for {SensorName} Gases", xaxis=dict(title='X: Ratio'), yaxis=dict(title='Y: Ratio Ppm'), xaxis2=dict(title='X: SensorValue'), yaxis2=dict(title='Y: Sensor Ppm'), template='plotly_dark')
fig.write_html(f"{SensorName}_gases_ppm.html")
