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
    {'name': 'Methane', 'ppmvals': (10, 10000), 'ppm': (1.1034, -0.0377), 'calvalue': 0.0533256},
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
    return np.clip(value, 0, maxlim)

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

def SensorppmModels(SensorValue, name):
    SensorRatio_value = SensorRLCalRL * Air * CalValue * (SensorValue - 1) / (SensorValue * (CalValue - 1))
    valuea, valueb =  get_constants(name, SensorRatio_value)
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
        
    valuea, valueb = get_constants(gasname, CalibrateAir)
    calAir = inverseyaxb(valuea, CalibrateAir, valueb)
    
    try: CalValue = gas['calvalue']
    except Exception: CalValue = interpolate(calAir, minair, maxair, 0, 1)
        
    if i == 0:
        color = color_palette[i % len(color_palette)]
        fig.add_trace(go.Scatter(x=time, y=air, mode='markers', marker=dict(color=color), name="Real SensorAir"), row=1, col=1)
        fig.add_trace(go.Scatter(x=time_surface, y=air_surface, mode='lines', marker=dict(color=color), name=f"SensorAir R² = {r2_percentile_time}"), row=1, col=1)

    color = color_palette[i + 1 % len(color_palette)]

    ppm = limit(SensorppmModels(percentile/100, gasname), maxair)
    x1, y1 = filter_repeats(time, ppm)
    fig.add_trace(go.Scatter(x=x1, y=y1, mode='markers', marker=dict(color=color), name=f"Real {gasname}"), row=1, col=2)

    ppm_surface = limit(SensorppmModels(SensorValue_surface, gasname), maxair)
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


