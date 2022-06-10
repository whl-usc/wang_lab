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
> Filter 1: Determine the average of the first 25 Vec (V) values. Only data points with Vec (V) >= 10x the average are kept. This differentiates for when data reading begins and when voltage is applied, since application of voltage significantly changes the Vec.
> Filter 2: Determine the average of 20 Vec values after voltage is applied. Subtract the average from each Vec value. Only data points that >= +0.005V the average are kept. This filters out any artifacts that are substantially lower (noise). 
> The mean of 5 Vec data points is taken for all values curated after the filters. 

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
<p align="right">(<a href="#top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

Wilson Lee - wilsonhl@usc.edu

Project Link: [https://github.com/wlee9829/wang_lab](https://github.com/wlee9829/wang_lab)
<p align="right">(<a href="#top">back to top</a>)</p>
