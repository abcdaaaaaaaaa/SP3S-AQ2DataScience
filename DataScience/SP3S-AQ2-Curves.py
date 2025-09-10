import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from scipy.optimize import curve_fit

def print_gas_table(gas_data, typ):
    if typ == 1:
        print()
        print("for ppm = a*ratio^b:")
        print()
        print("Gas    | a       | b")
        for gas, (a, b) in gas_data1.items():
            print(f"{gas.ljust(7)}| {str(a).ljust(8)}| {str(b).ljust(7)}")
        print()
    if typ == 2:
        print("for ppm = 10^[(log10(ratio)-b)/m]:")
        print()
        print("Gas    | m       | b")
        for gas, (m, b) in gas_data2.items():
            print(f"{gas.ljust(7)}| {str(m).ljust(8)}| {str(b).ljust(7)}")
        print()
            
sensor_name = 'SP3S-AQ2'

gases = {}
gas_data1 = {}
gas_data2 = {}

colornum = ListNumber = 0

fig = make_subplots(subplot_titles=["New Curve"])

while True:
    gas_name = input("Enter the gas name (or press 'Enter' to finish): ")
    if gas_name == '':
        break
    else:
        ListNumber += 1
        colornum += 1
        match colornum:
            case 1: hexcolor = "#40E0D0"  # Turquoise
            case 2: hexcolor = "#87CEFA"  # Light Sky Blue
            case 3: hexcolor = "#007FFF"  # Vivid Sky Blue
            case 4: hexcolor = "#CCCCFF"  # Periwinkle
            case 5: hexcolor = "#87CEEB"  # Sky Blue
            case 6: hexcolor = "#6A5ACD"  # Slate Blue
            case 7: hexcolor = "#4B0082"  # Indigo
            case 8: hexcolor = "#FFA500"  # Orange
            case 9: hexcolor = "#4169E1"  # Royal Blue
            case 10: hexcolor = "#0F52BA" # Sapphire
            case _: hexcolor = "Unknown"

    values = []
    values_input = input(f"Enter (x, y) values for {gas_name} as [(x1, y1), (x2, y2), ...]: ")
    try:
        values = eval(values_input)
        grouped_values = [(values[i], values[i+1]) for i in range(len(values)-1)]
        for idx, pair in enumerate(grouped_values, start=1):
            subgas_name = f"{gas_name}_{idx}"
            x_values = [pair[0][0], pair[1][0]]
            y_values = [pair[0][1], pair[1][1]]
            x = np.array(x_values)
            y = np.array(y_values)
            def func(x, a, b):
                return a * np.power(x, b)
            popt, pcov = curve_fit(func, x, y)
            residuals = y - func(x, *popt)
            ss_res = np.sum(residuals**2)
            ss_tot = np.sum((y - np.mean(y))**2)
            r_squared = 1 - (ss_res / ss_tot)
            gases[subgas_name] = {'a': popt[0], 'b': popt[1], 'R_squared': r_squared}
            a_rounded = round(popt[0], 4)
            b_rounded = round(popt[1], 4)
            b2 = np.log10(popt[0])
            b2_rounded = round(b2, 4)
            gas_data1[subgas_name] = (a_rounded, b_rounded)
            gas_data2[subgas_name] = (b_rounded, b2_rounded)
            print(f"{subgas_name}: logm={b_rounded}, logb={b2_rounded}, a={a_rounded}, b={b_rounded}, R²={r_squared:.4f}")
            new_x = np.linspace(min(x_values), max(x_values), 100)
            new_y = a_rounded * np.power(new_x, b_rounded)
            fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name=f'Datas {subgas_name} (R²={r_squared:.4f})', marker=dict(color=hexcolor)))
            fig.add_trace(go.Scatter(x=new_x, y=new_y, mode='lines', name=f'Curve {subgas_name}: y = {a_rounded} * x^{b_rounded}', marker=dict(color=hexcolor)))
    except Exception as e:
        print("An error occurred:", e)
        print("Invalid input format. Please enter the values as [(x1, y1), (x2, y2), ...]")

print_gas_table(gas_data1, 1)
print_gas_table(gas_data2, 2)

fig.update_layout(
    title=f'Regression Curves for {sensor_name}',
    autosize=True,  
    template='plotly_white',
    showlegend=True
)

fig.update_xaxes(title_text="Ppm (y)")
fig.update_yaxes(title_text="Ratio (x)")

fig.write_html(f"{sensor_name}_gas_curves.html")
