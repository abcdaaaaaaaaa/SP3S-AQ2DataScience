# SP3S-AQ2DataScience v5.5.1

## SP3S-AQ2DataScience What can be create?
"The first and only Arduino library where SP3S-AQ2 Gas Sensor combine with Data Science"

## 1) Advanced Data Science System for Regression Calculations
<img width="1264" height="577" alt="SP3S-AQ2 gas curves" src="https://github.com/user-attachments/assets/ae06c949-4866-4ac9-b63d-4d0cefb52e16" />

## 2) Ppm Analysis of SP3S-AQ2 Gases
<img width="1264" height="577" alt="SP3S-AQ2 Ppm Analysis" src="https://github.com/user-attachments/assets/4ba483c7-efab-4263-ab80-37324c43c375" />

## 3) Slope Estimation in Time-Dependent SP3S-AQ2 Gases
<img width="1264" height="577" alt="SP3S-AQ2 Gases Slope Estimation" src="https://github.com/user-attachments/assets/8dbb9f39-81b5-444e-b7a2-682ffa55e793" />

## Ppm Formullas

<img width="360" alt="log" src="https://github.com/user-attachments/assets/c0d1db76-0c69-4725-80fc-aed740fcbac8" />

![loghello)](https://github.com/user-attachments/assets/5b251bec-9677-421d-9101-ccb1e3ad4d2e)

<img width="1264" alt="image1" src="https://github.com/user-attachments/assets/63fcad55-8c34-4520-a2b6-af4c509d6888" />

<img width="1264" alt="image2" src="https://github.com/user-attachments/assets/2aeeeef4-0d06-45f1-9f49-b4e513cc5dea" />

The first formula is determined according to all points while the second formula is determined according to the first and last point. (if R^2 = 1 (%100) always: logm = valueb, logb = log10(valuea)).

## y = ax^b  --> ppm = a×ratio^b
<b> Therefore, we need to make a transition according to the formula:

<img width="400" alt="image3" src="https://github.com/user-attachments/assets/9706b917-7ce9-4bc9-a3bb-171a11e46052" />

<b> In data graphs, the x-axis is given as ppm and the y-axis is given as ratio.

## Determining coefficients a and b according to the ratio
<table>
<tr>
<td>

| Methane            | a      | b       |
| ------------------ | ------ | ------- |
| R > 0.952          | 1.1086 | -0.0448 |
| 0.94 < R <= 0.952  | 0.9867 | -0.0105 |
| 0.906 < R <= 0.94  | 1.097  | -0.0335 |
| 0.878 < R <= 0.906 | 1.0513 | -0.0261 |
| 0.842 < R <= 0.878 | 1.1424 | -0.0381 |
| R <= 0.842         | 2.2563 | -0.1231 |

</td>
<td>

| IsoButane          | a      | b       |
| ------------------ | ------ | ------- |
| R > 0.821          | 1.0725 | -0.0786 |
| 0.658 < R <= 0.821 | 1.5342 | -0.1838 |
| 0.514 < R <= 0.658 | 1.8529 | -0.2248 |
| 0.351 < R <= 0.514 | 3.1315 | -0.3168 |
| 0.231 < R <= 0.351 | 4.8725 | -0.3808 |
| R <= 0.231         | 4.0796 | -0.3586 |

</td>
<td>

| CO                 | a      | b       |
| ------------------ | ------ | ------- |
| R > 0.658          | 1.4117 | -0.2244 |
| 0.428 < R <= 0.658 | 2.2176 | -0.3572 |
| 0.274 < R <= 0.428 | 2.7757 | -0.406  |
| 0.148 < R <= 0.274 | 5.0696 | -0.5116 |
| 0.084 < R <= 0.148 | 5.2111 | -0.5156 |
| R <= 0.084         | 3.0264 | -0.4477 |

</td>
</tr>
<tr>
<td>

| Ethanol            | a      | b       |
| ------------------ | ------ | ------- |
| R > 0.554          | 1.6105 | -0.3138 |
| 0.303 < R <= 0.554 | 3.0468 | -0.5012 |
| 0.148 < R <= 0.303 | 6.1074 | -0.6522 |
| 0.067 < R <= 0.148 | 6.3217 | -0.6583 |
| 0.042 < R <= 0.067 | 1.2629 | -0.4251 |
| R <= 0.042         | 1.0192 | -0.3983 |

</td>
<td>

| Hydrogen           | a      | b       |
| ------------------ | ------ | ------- |
| R > 0.444          | 1.5579 | -0.3691 |
| 0.237 < R <= 0.444 | 2.6156 | -0.5214 |
| 0.139 < R <= 0.237 | 2.2189 | -0.4857 |
| 0.07 < R <= 0.139  | 3.5841 | -0.5698 |
| 0.05 < R <= 0.07   | 0.5806 | -0.3063 |
| R <= 0.05          | 0.2205 | -0.1853 |

</td>
</tr>
</table>

## Determining SensorCalibrationValue

<img width="786" height="430" alt="image4" src="https://github.com/user-attachments/assets/8a3f9416-2590-475d-a270-36262b8742c2" />

## V = I × R

<img width="841" height="671" alt="image5" src="https://github.com/user-attachments/assets/8971e631-d1ce-4369-a3c0-ea07def2776f" />

-------------------------

<img width="543" height="63" alt="image6" src="https://github.com/user-attachments/assets/4c7eb93d-3937-49c9-8365-1525d3d22fd4" />

## Final ppm calculation

<img width="825" alt="image7" src="https://github.com/user-attachments/assets/7ab79171-ae4a-4bee-b012-90755a209cbe" />

## Check out all our DataScience libraries under the SpaceData series!

"The first and only Arduino library series where Gas Sensors and Geiger Counter combine with Data Science"

| Library | Scope |
|---------|---------|
| <a href="https://github.com/abcdaaaaaaaaa/MQDataScience">MQDataScience  | MQ2, MQ3, MQ4, MQ5, MQ6, MQ7, MQ8, MQ9, MQ131_LOW, MQ131_HIGH, MQ135, MQ136, MQ137, MQ138, MQ214, MQ216, MQ303A, MQ303B, MQ306A, MQ307A, MQ309A Gas Sensors  |
| <a href="https://github.com/abcdaaaaaaaaa/TGSDataScience">TGSDataScience  | TGS2600, TGS2610, TGS2611 TGS2620, TGS2612, TGS2442, TGS2201, TGS4161, TGS8100, TGS813, TGS822, TGS2602, TGS6812 Gas Sensors |
| <a href="https://github.com/abcdaaaaaaaaa/MG811DataScience">MG811DataScience  | MG811 Gas Sensor  |
| <a href="https://github.com/abcdaaaaaaaaa/SP3S-AQ2DataScience">SP3S-AQ2DataScience  | SP3S-AQ2-01 Gas Sensor  |
| <a href="https://github.com/abcdaaaaaaaaa/RadioactiveDataScience">RadioactiveDataScience  | Geiger Counter  |

## For detailed explanation, You can also check out the github <a href="https://github.com/abcdaaaaaaaaa/SP3S-AQ2DataScience/wiki">Wiki Page!

## You can access the library's article <a href="https://www.spacepedia.info/SP3S-AQ2DataScience">Here!
