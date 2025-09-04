import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.optimize import curve_fit
import plotly.colors as pc
import pandas as pd
import MQInfo

SensorName = 'SP3S-AQ2'
df = pd.read_excel(f"{SensorName}_Datas.xlsx")

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

def roundf(*args):
    return tuple(round(x, 4) for x in args)

def round4(value):
    return np.round(value, 4)

def interpolate(value, old_min, old_max, new_min, new_max):
    return (value - old_min) * (new_max - new_min) / (old_max - old_min) + new_min

def exponential_interpolate(value, min_value, max_value, target_min, target_max):
    log_min = np.log10(target_min)
    log_max = np.log10(target_max)
    ratio = (value - min_value) / (max_value - min_value)
    log_val = log_min + ratio * (log_max - log_min)
    return np.power(10, log_val)

def yaxb(valuea, value, valueb):
    return valuea * np.power(value, valueb)

def inverseyaxb(valuea, value, valueb):
    return np.power(value / valuea, 1 / valueb)

def vals(minval, maxval, count):
    return np.linspace(minval, maxval, count)

def fit_time_with_r2(x, y):
    popt, _ = curve_fit(lambda x, a, b: yaxb(a, x, b), x, y)
    a, b = popt
    y_pred = yaxb(a, np.array(x), b)
    ss_res = np.sum((np.array(y) - y_pred) ** 2)
    ss_tot = np.sum((np.array(y) - np.mean(y)) ** 2)
    r2 = 1 - (ss_res / ss_tot)
    return a, b, r2

def filter_repeats(x, y):
    filtered_x = [x[0]]
    filtered_y = [y[0]]
    for i in range(1, len(y)):
        if (y[i - 1] != minair) and (y[i - 1] != maxair):
            filtered_x.append(x[i])
            filtered_y.append(y[i])
    return filtered_x, filtered_y

def vals(minval, maxval, count):
    return np.linspace(minval, maxval, count)

def limit(value, maxlim):
    return np.minimum(np.maximum(value, 0), maxlim)

def sensorlimit(value):
    return np.maximum(np.minimum(value, maxair), minair)

def SensorppmModels(valuea, valueb, SensorValue):
    SensorRatio_value = SensorRLCalRL * Air * CalValue * (SensorValue - 1) / (SensorValue * (CalValue - 1))
    return inverseyaxb(valuea, SensorRatio_value, valueb)


time, percentile = np.array(df["Time"], dtype=float), np.array(df["Per"], dtype=float)
percentile = limit(percentile, 100)
SensorValue = percentile / 100

a_percentile_time, b_percentile_time, r2_percentile_time = fit_time_with_r2(time, percentile)
a_percentile_time, b_percentile_time, r2_percentile_time = roundf(a_percentile_time, b_percentile_time, r2_percentile_time)

time_surface = vals(min(time), max(time)*2, 200)
percentile_surface = limit(yaxb(a_percentile_time, time_surface, b_percentile_time), 100)
SensorValue_surface = percentile_surface / 100

air = round4(exponential_interpolate(SensorValue, 0, 1, MinAirPpm, MaxAirPpm))
air_surface = limit(exponential_interpolate(SensorValue_surface, 0, 1, MinAirPpm, MaxAirPpm), MaxAirPpm)
    
GraphTitle = f"SensorAir Graph {MinAirPpm}-{MaxAirPpm} ppm"
fig = make_subplots(rows=1, cols=2, subplot_titles=[GraphTitle, f"{SensorName} Gases Graph ppms"])

color_palette = pc.qualitative.Plotly
    
for i, gas in enumerate(gas_params):
    minair, maxair = gas['ppmvals']
    gasname = gas['name']
    valuea, valueb = gas['ppm']
    
    calAir = inverseyaxb(valuea, CalibrateAir, valueb)
    try: CalValue = gas['calvalue']
    except Exception: CalValue = interpolate(calAir, minair, maxair, 0, 1)
        
    if i == 0:
        color = color_palette[i % len(color_palette)]
        fig.add_trace(go.Scatter(x=time, y=air, mode='markers', marker=dict(color=color), name="Real SensorAir"), row=1, col=1)
        fig.add_trace(go.Scatter(x=time_surface, y=air_surface, mode='lines', marker=dict(color=color), name=f"SensorAir R² = {r2_percentile_time}"), row=1, col=1)

    color = color_palette[i + 1 % len(color_palette)]

    ppm = limit(SensorppmModels(valuea, valueb, percentile/100), maxair)
    x1, y1 = filter_repeats(time, ppm)
    fig.add_trace(go.Scatter(x=x1, y=y1, mode='markers', marker=dict(color=color), name=f"Real {gasname}"), row=1, col=2)

    ppm_surface = limit(SensorppmModels(valuea, valueb, SensorValue_surface), maxair)
    x2, y2 = filter_repeats(time_surface, ppm_surface)
    fig.add_trace(go.Scatter(x=x2, y=y2, mode='lines', marker=dict(color=color), name=gasname), row=1, col=2)
    

fig.update_layout(
    title=f"{SensorName} Gases Slope Estimations",
    xaxis=dict(title='X: Time (w)'),
    yaxis=dict(title='Y: SensorAir (z)'),
    xaxis2=dict(title='X: Time (w)'),
    yaxis2=dict(title='Y: SensorPpm (z)'),
    template='plotly_dark'
)

fig.write_html(f"{SensorName}_Slope_Estimation.html")
