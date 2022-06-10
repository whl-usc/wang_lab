'''
contact:    wilsonhl@usc.edu
date:       2022_06_09
python:     python3.10
script:     frsa.py

framerate_shift_analysis.py
This script is used to determine
the start/end points of a biosensing 
instrument file based on mathematical trends. 

'''

# Import packages
import sys, os
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd; pd.options.mode.chained_assignment = None
import seaborn as sns
import statistics as stats

# Usage instructions
if len(sys.argv) < 4:
    print("\nUsage:		python3 framerate_shift_analysis.py data.xlsx graphs voltage_low voltage_high")
    print("\ndata.xlsx:	Name of .xlsx file from the SPRM machine")
    print("graphs:		y/n to print graphs or not")
    print("voltage_lo:	Lowest voltage value")
    print("voltage_hi:	Highest voltage value")
    sys.exit()

file = os.path.splitext(str(sys.argv[1])); file_name = file[0]

if sys.argv[2] == "y":
	graphs = str(sys.argv[2])
elif sys.argv[2] == "n":
	graphs = str(sys.argv[2])
else:
	print("'graphs' value must be either: y or n")
	sys.exit()

voltage_lo = float(sys.argv[3])
voltage_hi = float(sys.argv[4])

# Read the .xlsx file and average ROI-based columns, Remove other values.
print(str(datetime.now())[:-7] + " Opening .xlsx and reading data...")
df = pd.read_excel(sys.argv[1], 0, header=0)
df["number"] = np.arange(len(df))
ROI = df.filter(like='Roi'); df["ROI_mean"] = ROI.mean(axis=1)
df_small = df[["number", "ROI_mean", "Vec (V)"]]

df_small.to_csv(file_name+'.csv', index = None, header = True)
print(str(datetime.now())[:-7] + " File saved as " + file_name + ".csv")

# Plot graphs; ROI_mean, Vec (V).

if graphs == "y":
	# Set up figure parameters
	sns.set(rc={"figure.figsize":(6,6)}); sns.set_style("white")
	color = sns.color_palette('bright')
	# Plot ROI_mean
	ax = sns.lineplot(x="number", y='ROI_mean', data=df_small, palette=color, hue=None)
	ax.set(xlabel=" ", ylabel="ROI_mean"); sns.despine()
	ax.get_figure().savefig(file_name+"_ROI_mean.png")
	outfile = str(file_name+"_ROI_mean.png")
	print(str(datetime.now())[:-7] + " Graph complete, check for " + str(outfile) + ".")
	# Plot Vec(V)
	ax = sns.lineplot(x="number", y='Vec (V)', data=df_small, palette = color, hue=None)
	ax.set(xlabel=" ", ylabel="Vec (V)"); sns.despine()
	ax.set_ylim(voltage_lo,voltage_hi)
	ax.get_figure().savefig(file_name+"_Vec.png")
	outfile = str(file_name+"_Vec.png")
	print(str(datetime.now())[:-7] + " Graph complete, check for " + str(outfile) + ".")
else:
	print(str(datetime.now())[:-7] + " Omitted graph plotting...")

# Determine where to start checking from; anything great than 10x the baseline average is checked.
vec_0 = float(df_small.iloc[1:25,[2]].mean())
df_0 = df_small.loc[df_small['Vec (V)'] > (10*vec_0)]

# Determine the start point based on the average trends.
vec_1 = float(df_0.iloc[5:25,[2]].mean())
df_1 = df_0.loc[df_0['Vec (V)'] >= (vec_1-0.005)]

mean_5 = []
for i in range(0,len(df_1)):
	avg_i5 = (float(df_0.iloc[i+1,[2]] + df_0.iloc[i+2,[2]] + df_0.iloc[i+3,[2]] + df_0.iloc[i+4,[2]] + df_0.iloc[i+5,[2]]))/5
	mean_5.append(avg_i5)
df_1["mean_5"]=mean_5

cutoff = -1.5E-04 #This value may need to be changed if no start point is found.

for i in range(0,len(df_1)-2):
	sub1 = float(df_1.iloc[i+2,[3]] - df_1.iloc[i+1,[3]])
	sub2 = float(df_1.iloc[i+3,[3]] - df_1.iloc[i+2,[3]])
	if sub1 > cutoff and sub2 > cutoff:
		continue
	elif sub1 < cutoff and sub2 < cutoff:
		start_point = int(df_1.iloc[i+1,[0]])
		print(str(datetime.now())[:-7] + " Start point:	" + str(start_point))
		break
	elif sub1 < cutoff and sub2 > cutoff:
		continue
	elif sub1 > cutoff and sub2 < cutoff:
		continue
	else:
		print("No start point determined, please check the cutoff value in line 91.")

# Determine the end point based on the average trends.
large_values = df_small['Vec (V)'].nlargest(n=1000)
peak = large_values.index.tolist()
midpoint = np.median(peak)
mid_plus = int(midpoint + 200); mid_minus = int(midpoint - 200)
df_end = df_small.iloc[mid_minus:mid_plus]
max_value = df_end['Vec (V)'].nlargest(n=1)
x = max_value.index.tolist(); end_point = str(x)[1:-1]
print(str(datetime.now())[:-7] + " End point:		" + str(end_point))


# Compare the trend to the "start point" of the ROI_mean graph.
roi_0 = (df_small.iloc[start_point:,[1]]); roi_1 = roi_0.reset_index()
mean_5 = []
for i in range(0,len(roi_1)):
	avg_i5 = (float(roi_1.iloc[i,[1]] + roi_1.iloc[i,[1]] + roi_1.iloc[i,[1]] + roi_1.iloc[i,[1]] + roi_1.iloc[i,[1]]))/5
	mean_5.append(avg_i5)
roi_1["mean_5"]=mean_5

cutoff = -5.0E-04 #This value may need to be changed if no start point is found.

diff = []
for i in range(0,len(roi_1)-2):
	sub1 = float(roi_1.iloc[i+2,[1]] - roi_1.iloc[i+1,[1]])
	sub2 = float(roi_1.iloc[i+3,[1]] - roi_1.iloc[i+2,[1]])
	if sub1 > cutoff and sub2 > cutoff:
		continue
	elif sub1 < cutoff and sub2 < cutoff:
		start_point = int(roi_0.iloc[i+1,[0]])
		print(str(datetime.now())[:-7] + "Trend at Vec (V) determined start point matches ROI_mean.")
		break
	elif sub1 < cutoff and sub2 > cutoff:
		continue
	elif sub1 > cutoff and sub2 < cutoff:
		continue
	else:
		print("Trend does not match, please check the cutoff value in line 131.")

'''
When we do the analysis, we look at a gridded chip. You can have one ROI (one dataset from one larger box) or fragment into smaller areas (Roi# (%)). When voltage is applied, it takes data from all of the ROI (squares) at the same time.
BF-Roi is "bright field" ROI. When analyzing data, needed to unclick the brightfield. Can ignore this column.
After the last Roi (say Roi88), add a column and take the average of all of the ROI. 
Make a graph of the average ROI (scatter plotted with line)
Make a graph of the Vec(V) plot (lineplot with line). The voltage range is ...0.02V to -0.55V... (voltage range changes).
The dips are the cycles ("2 cycles") from the name of the experiment.

############

Copy the voltage graph and average ROI graphs to another dataframe. 
Make a Vec(V) Start Point graph. It is zoomed in on the Vec(V) graph, especially when the voltage is applied. (When the voltage is applied, the Delta should be +/- certain value).
When the start point is determined, write it down as the x-value. Go to the average ROI graph. The start point is going to be the same numerical value. We will try to find the same characteristics (say +/- values to the the left and right of a data point).
End point is just the maximum value on the peak (for both peaks).


########

Along with the data recorded, there is an image captured. Take the first image and subtract from the whole video as "background". Select the area (say the whole area or where the nanoparticles are) and plot the intensity. 
"Original" graph is the raw analysis of intensity of an image. index vs intensity determined by a program.
If we compare the average ROI graph with the "original" graph, we can see the x values are shifted. After determined the start+end points, do a shift of the data values using equation (n-1)/n

########
VEC > ROI > ImageJ
'''





