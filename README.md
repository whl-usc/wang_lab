<div id="top"></div>

<!-- PROJECT NAME -->
## frsa.py
FRSA stands for **F**rame**R**ate **S**hift **A**nalysis. 
frsa.py is used as an aid for SPRM data analysis.

<!-- ABOUT THE PROJECT -->
## About the Project

A gridded chip from the SPRM machine...
Can have one region-of-interest (ROI) or many smaller ones (_e_._g_., ROI1 (%)). 
When voltage is applied to the chip, data is captured for all of the ROI at the same time.

Analysis is as follows:

1. Take the mean of all the ROI at their respective timepoints.

> pandas: dataframe (written to a new .csv) containing only the data entry number, mean_ROI, and Vec (V).

2. Plot a lineplot of time _vs._ ROI mean and a lineplot of time _vs._ Vec (V).

<p float="left">
    <img src="https://github.com/wlee9829/wang_lab/blob/main/kno3_0.02v_2cycles_ROI_mean.png" width="200"/>
    &nbsp
    <img src="https://github.com/wlee9829/wang_lab/blob/main/kno3_0.02v_2cycles_Vec.png" width="200"/>

> seaborn: lineplots as plotted as described above. Note that the y-axis values for the time _vs._ Vec (V) plot are sensitive to the low and high voltage values.

4. Determine the start/end points of the application of voltage.

> The start and end points of voltage application are determined based on the trend of a mathematical average.
> For effective parsing of the original dataframe, the Vec (V) values are curated.

> Filter 1: Determine the average of the first 25 Vec (V) values. Only data points with a Vec (V) value >= 10x the average are kept. This differentiates for when data reading begins and voltage application, since applying voltage significantly changes Vec (V) values.

> Filter 2: Determine the average of 20 Vec (V) values after voltage is applied. Subtract the average from each Vec (V) value. Only data points with Vec (V) >= +0.005V the average are kept. This filters out any values that are significantly lower (_i.e._, artifacts or noise). 

> Each data point and the next four values are averaged and appended into a column. The difference of the each data point and the following data point are determined. Using a cutoff of -1.5E-04, if the difference of two consecutive averages are lower than the cutoff (_i.e._, Vec (V) is decreasing), the start point is determined.

> The end point is determined by parsing the original dataframe and curating the highest 1000 Vec (V) values. The endpoint must be one of the largest Vec (V) value in the dataset. By determining the median of the top 1000 values, the possible endpoint values are narrowed. From all Vec (V) values +/-200 the median, the largest is determined as the endpoint. 


    
<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started
Set up the program prior to running.

### Prerequisites

frsa.py was written using python3.10
* Opening .xlsx
```
pip install openpyxl
```
* Installing numpy
* Installing seaborn
* Installing
```
pip install ____
```

<!-- USAGE EXAMPLES -->
## Usage

The script requires no prior coding experience in order to use. 

Enter arguments as follows:
```
python3 frsa.py <file_name.xlsx> y/n voltage_low voltage_high
```
Example:
* File is called "kno3_0.025v.xlsx"
* "y" means a graph will be plotted
* -0.55 is the lowest voltage
* 0.2 is the highest voltage
```
python3 frsa.py kno3_0.025v.xlsx y -0.55 0.2
```

Example output:
```
    2022-06-10 16:10:24 Opening .xlsx and reading data...
    2022-06-10 16:10:31 File saved as kno3_0.02v_2cycles.csv
    2022-06-10 16:10:31 Omitted graph plotting...
    2022-06-10 16:10:31 Start point:        310
    2022-06-10 16:10:31 End point:          4212
    2022-06-10 16:10:42 Trend at Vec (V) determined start point matches ROI_mean.
```
<p align="right">(<a href="#top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

Wilson Lee - wilsonhl@usc.edu

Project Link: [https://github.com/wlee9829/wang_lab](https://github.com/wlee9829/wang_lab)
<p align="right">(<a href="#top">back to top</a>)</p>
