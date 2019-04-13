import json
import pandas as pd
import matplotlib.pyplot as plt
import math  
import seaborn as sns
import numpy as np

### LOAD DATA INTO DATAFRAME

versions = ['1.0','1.1','1.2','1.3']

df = pd.DataFrame()

# Open the json file and loads
with open('factorsAttraction.json') as json_data:
	obj = json.load(json_data)

	# Iterate for every version
	for version in versions:
		#print(version)
		df_aux = pd.DataFrame(obj['__collections__'][version])
		df_aux = df_aux.transpose()
		
		# Add the version to the dataframe
		df_aux['version'] = version

		# First version used different variable names
		if version == '1.0':
			df_aux['coord_original_left'] = df_aux['originalLeft']
			df_aux['coord_original_top'] = df_aux['originalTop']
			df_aux['coord_user_left'] = df_aux['userLeft']
			df_aux['coord_user_top'] = df_aux['userTop']
			df_aux = df_aux.drop(['originalLeft', 'originalTop', 'userLeft', 'userTop'], axis = 1)

		# First two versions were only calibration phases
		if (version == '1.0') or (version == '1.1'):
			df_aux['condition'] = 'Calibration'

		# Delete the data where clickHere was centerlized, the face was different, and spirals was also center.
		if (version == '1.2'):
			df_aux = df_aux[df_aux.condition != 'Spiral']
			df_aux = df_aux[df_aux.condition != 'Face']
			df_aux = df_aux[df_aux.condition != 'ClickHere']

		# Append version to the dataframe 
		df = df.append(df_aux)
		df = df.drop(['__collections__'], axis = 1)

# Remove the 'px' characther from the columns
df['coord_original_left'] = df.apply(lambda x: int(x['coord_original_left'].strip('px')), axis = 1) 
df['coord_original_top'] = df.apply(lambda x: int(x['coord_original_top'].strip('px')), axis = 1) 
df['coord_user_left'] = df.apply(lambda x: int(x['coord_user_left'].strip('px')), axis = 1) 
df['coord_user_top'] = df.apply(lambda x: int(x['coord_user_top'].strip('px')), axis = 1) 


### DO TRANSFORMATION OF PIXELS TO % RELATIVE TO THE SCREEN SIZE

# Extract width and height from the field screenSize
f1 = lambda x: int(x["screenSize"].split("x")[0])
f2 = lambda x: int(x["screenSize"].split("x")[1])
df['width'] = df.apply(f1, axis = 1)
df['height'] = df.apply(f2, axis = 1)

# Transform Top to Y
df['coord_original_Y'] = df.apply(lambda x: x['height'] - x['coord_original_top'], axis = 1) 
df['coord_user_Y'] = df.apply(lambda x: x['height'] - x['coord_user_top'], axis = 1)
df['coord_original_X'] = df['coord_original_left']
df['coord_user_X'] = df['coord_user_left']

df['coord_original_X_relative'] = df['coord_original_X'] / df['width']
df['coord_user_X_relative'] = df['coord_user_X'] / df['width']
df['coord_original_Y_relative'] = df['coord_original_Y'] / df['height']
df['coord_user_Y_relative'] = df['coord_user_Y'] / df['height']

df['ratio'] = df['width'] / df['height']

#df = df[['email','device','condition','coord_original_X_relative','coord_user_X_relative','coord_original_Y_relative','coord_user_Y_relative', 'version']]

#df = df[df.version == '1.3']

print("Number of unique e-mails: "+str(df.groupby(['email']).count().shape[0]))

#print(df)

### DATA CLEANING OF NOISE - Based on the data distribution, Clean all the points where the difference from original and user (heigh and width) is more than 10% from the screen size

# df_cleaned = df.copy()


# plt.scatter(df_cleaned.coord_original_X_relative,df_cleaned.coord_user_X_relative, c='#2bbf42', label="Width", alpha=0.8)
# plt.scatter(df_cleaned.coord_original_Y_relative,df_cleaned.coord_user_Y_relative, c='#378743', label="Height", alpha=0.8)
# plt.xlabel('Original cross position ')
# plt.ylabel('User feedback cross position')
# #Relation between original and user feedback cross position for Width and Height relative to the screen size with noise
# plt.legend()
# plt.grid(b=True, alpha= 0.1)
# plt.title("Noisy data")
# plt.show()

# print("Interactions before cleaning: "+str(df_cleaned.shape[0]))

# df_cleaned = df_cleaned[ (abs(df_cleaned.coord_original_X_relative - df_cleaned.coord_user_X_relative)) <= 0.1]
# df_cleaned = df_cleaned[ (abs(df_cleaned.coord_original_Y_relative - df_cleaned.coord_user_Y_relative)) <= 0.1]

# plt.scatter(df_cleaned.coord_original_X_relative,df_cleaned.coord_user_X_relative, c='#2bbf42', label="Width", alpha=0.8)
# plt.scatter(df_cleaned.coord_original_Y_relative,df_cleaned.coord_user_Y_relative, c='#378743', label="Height", alpha=0.8)
# plt.xlabel('Original cross position ')
# plt.ylabel('User feedback cross position')
# #Relation between original and user feedback cross position for Width and Height relative to the screen size after data cleaning
# plt.legend()
# plt.grid(b=True, alpha= 0.1)
# plt.title("After data cleaning")
# plt.show()

# print("Interactions after cleaning: "+str(df_cleaned.shape[0]))

def calculateDistanceTwoPoints(x1,y1,x2,y2):  
     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
     return dist

def calculateDistanceOriginalUser(dataframe):
	dataframe['distance_between_original_user_in_percentage'] =  dataframe.apply(lambda x: calculateDistanceTwoPoints(x.coord_original_X_relative, x.coord_original_Y_relative, x.coord_user_X_relative, x.coord_user_Y_relative) * 100, axis = 1)
	mean_sd_DistanceOriginalUser(dataframe)
	return dataframe

standardDeviation = 0
def mean_sd_DistanceOriginalUser(dataframe):
	averageDistance = dataframe['distance_between_original_user_in_percentage'].mean()
	global standardDeviation 
	standardDeviation= dataframe['distance_between_original_user_in_percentage'].std()
	print("Average distance from Original position to User position: "+str(averageDistance)+ '%')
	print("Standard deviation from the distance between original to user: "+str(standardDeviation))

### CALCULATION FACTOR OF ATTRACTION POSITION OF FACE
def calculateFactorFace(dataframe):
	# Resolution of the image of the face
	width_face_image_original = 1280
	height_face_image_original = 720
	ratio_face_image1 = width_face_image_original / height_face_image_original
	ratio_face_image2 = height_face_image_original / width_face_image_original
	# Ratio of the screen size for each interaction
	dataframe['ratio_screen_size'] = dataframe['width'] / dataframe['height']

	# Check if the image size is dimensioned by the height or width
	dataframe['axes_to_calculate_img_size'] = dataframe['ratio_screen_size'].apply(lambda x: 'X' if (x < ratio_face_image1) else 'Y')

	# Calculate the Width and Height of the image face
	dataframe['img_size_width'] = dataframe.apply(lambda x: x['width'] if (x['axes_to_calculate_img_size'] == 'X') else (x['height'] * ratio_face_image1), axis=1)
	dataframe['img_size_height'] = dataframe.apply(lambda x: (x['width'] * ratio_face_image2) if (x['axes_to_calculate_img_size'] == 'X') else x['height'], axis=1)

	# Factor of attraction in the % of the image
	img_factor_X = 0.55
	img_factor_Y = 0.73

	# Calculate the factor of attraction of the missing eye in relation with the % of the screen (widht and height)
	#((screen size - img size) / 2  + % img size) / screen size
	dataframe['factor_X'] = (((dataframe['width'] - dataframe['img_size_width']) / 2) + (img_factor_X * dataframe['img_size_width'])) / dataframe['width']
	dataframe['factor_Y'] = (((dataframe['height'] - dataframe['img_size_height']) / 2) + (img_factor_X * dataframe['img_size_height'])) / dataframe['height']

	return dataframe

def calculateFactorButtonBottomLeft(dataframe):
	width_button_image_original = 87
	height_button_image_original = 32

	dataframe['factor_X'] = (dataframe['width'] * 0.2 + (width_button_image_original / 2 )) / dataframe['width']
	dataframe['factor_Y'] = (dataframe['height'] * 0.2 + (height_button_image_original / 2 )) / dataframe['height']

	return dataframe

def calculateFactorButtonTopRight(dataframe):
	width_button_image_original = 87
	height_button_image_original = 32

	dataframe['factor_X'] = (dataframe['width'] * 0.8 - (width_button_image_original / 2 )) / dataframe['width']
	dataframe['factor_Y'] = (dataframe['height'] * 0.8 - (height_button_image_original / 2 )) / dataframe['height']

	return dataframe

def calculateFactorSpiralLeft(dataframe):
	# Resolution of the image of the face
	width_spiral_image_original = 720
	height_spiral_image_original = 720

	# Calculate the Width and Height of the image spiral
	dataframe['img_size_height'] = dataframe['width'] / 2

	# Factor of attraction in the % of the image, always at the center of the spiral
	img_factor_Y = 0.5

	# Calculate the factor of attraction of center of the spiral in relation with the % of the screen (widht and height)
	dataframe['factor_X'] = 0.25 # the spiral left is always covering the left half size of the screen
	dataframe['factor_Y'] = (dataframe['height'] - (dataframe['img_size_height'] * img_factor_Y)) / dataframe['height']

	return dataframe

def calculateFactorSpiralCenter(dataframe):
	# Resolution of the image of the face
	width_spiral_image_original = 720
	height_spiral_image_original = 720

	# Calculate the Width and Height of the image spiral
	dataframe['img_size_height'] = dataframe['width'] / 2

	# Factor of attraction in the % of the image, always at the center of the spiral
	img_factor_Y = 0.5

	# Calculate the factor of attraction of center of the spiral in relation with the % of the screen (widht and height)
	dataframe['factor_X'] = 0.5 # the spiral left is always covering the left half size of the screen
	dataframe['factor_Y'] = (((dataframe['height'] - dataframe['img_size_height']) / 2) + (dataframe['img_size_height'] * img_factor_Y)) / dataframe['height']

	return dataframe

def calculateDistanceFromFactorAndPlotPoints(dataframe,threshold,title):

	dataframe['distance_factor_to_original'] =  dataframe.apply(lambda loop: calculateDistanceTwoPoints(loop.factor_X, loop.factor_Y, loop['coord_original_X_relative'], loop['coord_original_Y_relative']), axis = 1)
	dataframe['distance_factor_to_user'] = dataframe.apply(lambda loop: calculateDistanceTwoPoints(loop.factor_X, loop.factor_Y, loop['coord_user_X_relative'], loop['coord_user_Y_relative']), axis = 1)
	# threshold
	dataframe = dataframe[(dataframe.distance_factor_to_original <= threshold) | (dataframe.distance_factor_to_user <= threshold)]

	dataframe['distance_difference_in_percentage'] = ( dataframe['distance_factor_to_original'] - dataframe['distance_factor_to_user'] ) * 100

	# print the means for every column
	#print(dataframe.mean(axis=0))

	df_closer = dataframe.copy()
	df_farther = dataframe.copy()
	df_closer = df_closer[df_closer.distance_difference_in_percentage >= 0]
	df_farther = df_farther[df_farther.distance_difference_in_percentage < 0]

	closer_quantity = str(df_closer.shape[0])
	farther_quantity = str(df_farther.shape[0])

	plt.scatter(df_closer.coord_user_X_relative,df_closer.coord_user_Y_relative, c='#378743', alpha=0.9, label='Closer: '+closer_quantity)
	plt.scatter(df_farther.coord_user_X_relative,df_farther.coord_user_Y_relative, c='#990e0c', alpha=0.9, label= 'Farther: '+ farther_quantity)
	plt.scatter(dataframe.factor_X,dataframe.factor_Y, c='#0c2a99', label= 'Factor of attraction')
	plt.legend()
	plt.grid(b=True, alpha= 0.1)
	plt.xlim(0,1)
	plt.xlabel('Width screen scaled')
	plt.ylabel('Height screen scaled')
	plt.title(title)
	plt.ylim(0,1)

	print("Points which got closer to the attraction factor: "+closer_quantity)
	print("Points which got farther to the attraction factor: "+farther_quantity)

	plt.show()

	return dataframe


### Calculation of difference between mouse and touchescreen
# df_device = df_cleaned.copy()
# print(df_device.groupby(['device']).count())
# df_device = calculateDistanceOriginalUser(df_device)
# print(df_device.groupby(['device']).mean())
# df_mouse = df_device[df_device.device == 'Mouse']
# df_mouse = df_mouse[df_mouse.condition != 'Calibration']
# print(df_mouse.distance_between_original_user_in_percentage.mean())
# df_touch = df_device[df_device.device == 'Touchscreen']
# df_touch = df_touch[df_touch.condition != 'Calibration']
# print(df_touch.distance_between_original_user_in_percentage.mean())

### CALCULATION points
# df_anova = pd.DataFrame()
# threshold = 0.25

# print("\n ----------- \n")
# print("Calibration")
# df_Calibration = df_cleaned[df_cleaned.condition == 'Calibration']
# df_Calibration = calculateDistanceOriginalUser(df_Calibration)
# df_anova = df_anova.append(df_Calibration[['condition','distance_between_original_user_in_percentage']])

# print("\n ----------- \n")

# print("ClickHereBottomLeft")
# df_ClickHereBottomLeft = df_cleaned[df_cleaned.condition == 'ClickHereBottomLeft']
# df_ClickHereBottomLeft = calculateFactorButtonBottomLeft(df_ClickHereBottomLeft)
# df_ClickHereBottomLeft = calculateDistanceFromFactorAndPlotPoints(df_ClickHereBottomLeft, threshold, "Attraction result from click here bottom left scenario")
# df_ClickHereBottomLeft = calculateDistanceOriginalUser(df_ClickHereBottomLeft)
# df_anova = df_anova.append(df_ClickHereBottomLeft[['condition','distance_between_original_user_in_percentage']])
# print("\n ----------- \n")

# print("ClickHereTopRight")
# df_ClickHereTopRight = df_cleaned[df_cleaned.condition == 'ClickHereTopRight']
# df_ClickHereTopRight = calculateFactorButtonTopRight(df_ClickHereTopRight)
# df_ClickHereTopRight = calculateDistanceFromFactorAndPlotPoints(df_ClickHereTopRight, threshold, "Attraction result from click here top right scenario")
# df_ClickHereTopRight = calculateDistanceOriginalUser(df_ClickHereTopRight)
# df_anova = df_anova.append(df_ClickHereTopRight[['condition', 'distance_between_original_user_in_percentage']])
# print("\n ----------- \n")

# print("Face")
# df_Face = df_cleaned[df_cleaned.condition == 'Face']
# df_Face = calculateFactorFace(df_Face)
# df_Face = calculateDistanceFromFactorAndPlotPoints(df_Face,threshold, "Attraction result from face missing eye scenario")
# df_Face = calculateDistanceOriginalUser(df_Face)
# df_anova = df_anova.append(df_Face[['condition', 'distance_between_original_user_in_percentage']])
# print("\n ----------- \n")

# print("SpiralLeft")
# df_SpiralLeft = df_cleaned[df_cleaned.condition == 'SpiralLeft']
# df_SpiralLeft = calculateFactorSpiralLeft(df_SpiralLeft)
# df_SpiralLeft = calculateDistanceFromFactorAndPlotPoints(df_SpiralLeft,threshold, "Attraction result from spiral on the top left scenario")
# df_SpiralLeft = calculateDistanceOriginalUser(df_SpiralLeft)
# df_anova = df_anova.append(df_SpiralLeft[['condition', 'distance_between_original_user_in_percentage']])
# print("\n ----------- \n")

# print("SpiralCenter")
# df_SpiralCenter = df_cleaned[df_cleaned.condition == 'SpiralCenter']
# df_SpiralCenter = calculateFactorSpiralCenter(df_SpiralCenter)
# df_SpiralCenter = calculateDistanceFromFactorAndPlotPoints(df_SpiralCenter,threshold, "Attraction result from spiral on the center scenario")
# df_SpiralCenter = calculateDistanceOriginalUser(df_SpiralCenter)
# df_anova = df_anova.append(df_SpiralCenter[['condition', 'distance_between_original_user_in_percentage']])
# print("\n ----------- \n")

### BOX PLOT
# df_anova.boxplot('distance_between_original_user_in_percentage', by='condition')
# plt.xlabel('Scenarios')
# plt.xticks(size=6)
# plt.ylabel('Distance (% of the screen total size)')
# plt.title("Distance from the original to user position by scenario")
# plt.grid(b=True, alpha= 0.1)
# plt.show()

# plt.scatter(df_anova.condition,df_anova.distance_between_original_user_in_percentage, c='#378743', alpha=0.9)
# plt.xlabel('Scenarios')
# plt.xticks(size=6)
# plt.ylabel('Distance (% of the screen total size)')
# plt.title("Distance from original to user position of each interaction by scenario")
# plt.grid(b=True, alpha= 0.1)
# plt.show()

### ANOVA CALCULATION
# import statsmodels.api as sm
# from statsmodels.formula.api import ols

# mod = ols('distance_between_original_user_in_percentage ~ condition', data = df_anova).fit()
# aov_table = sm.stats.anova_lm(mod, typ=2)
# print(aov_table)

# esq_sm = aov_table['sum_sq'][0]/(aov_table['sum_sq'][0]+aov_table['sum_sq'][1])

# print("eta squared: "+str(esq_sm))

# df_anova.to_csv('data_2way_15threshold.csv')


### DISTRIBUTION 
def distributionPlot(dataframe,color,label):
	sns.distplot(dataframe, kde=True, rug=True, color=color, label=label)
	plt.xlabel('Distance (% of the screen total size)')
	plt.title("Distribution of distance difference, 15% threshold")
	plt.grid(b=True, alpha= 0.1)


# distributionPlot(df_ClickHereBottomLeft[['distance_difference_in_percentage']],"yellow","Click here bottom left")
# distributionPlot(df_ClickHereTopRight[['distance_difference_in_percentage']],"blue", "Click here top right")
# distributionPlot(df_Face[['distance_difference_in_percentage']],"green", "Face")
# distributionPlot(df_SpiralLeft[['distance_difference_in_percentage']],"red", "Spiral left")
# distributionPlot(df_SpiralCenter[['distance_difference_in_percentage']],"purple", "Spiral center")
# plt.xlim(-13,13)
# plt.ylim(0,0.3)
# plt.legend()
# plt.show()


#### ATTRACTION DOCUMENTING
def getQuadrant(coordinate,valueToBeDivided):
	quadrant = math.floor((coordinate*100)/valueToBeDivided)
	return quadrant

def getQuadrantTotal(row,column):
	quadrant = (column * 14 ) + row
	return quadrant

def createMatrix(dataframe,valueToBeDivided):
	matrix = np.zeros((14*14,14*14) ,dtype=int)
	for i in range(dataframe.shape[0]):
	# for i in range(10):
		quad_x_original = getQuadrant(dataframe.loc[dataframe.index[i],'coord_original_X_relative'],valueToBeDivided)
		quad_y_original = getQuadrant(dataframe.loc[dataframe.index[i],'coord_original_Y_relative'],valueToBeDivided)
		quad_x_user = getQuadrant(dataframe.loc[dataframe.index[i],'coord_user_X_relative'],valueToBeDivided)
		quad_y_user = getQuadrant(dataframe.loc[dataframe.index[i],'coord_user_Y_relative'],valueToBeDivided)

		quad_total_original = getQuadrantTotal(quad_x_original,quad_y_original)
		quad_total_user = getQuadrantTotal(quad_x_user,quad_y_user)
		# print(quad_total_original)
		# print(quad_total_user)
		# print("-")

		# if (quad_total_user == 78):
		# 	print(quad_x_user)
		# 	print(dataframe.loc[dataframe.index[i],'coord_user_X_relative'])
		# 	print(quad_y_user)
		# 	print(dataframe.loc[dataframe.index[i],'coord_user_Y_relative'])

		matrix[quad_total_original][quad_total_user] += 1

	return matrix 

def putRatioRows(matrix):
	matrix2 = pd.DataFrame(matrix)
	for i in range(len(matrix)):
		sum = np.sum(matrix[i][:])	
		if (sum > 0):
			matrix2.iloc[i,:] = matrix2.iloc[i,:] / sum
	return (matrix2.as_matrix())

def sumOfEachColumn(matrix):
	list_sum = []
	for i in range(len(matrix[0])):
		sum = np.sum(matrix[:,i])
		list_sum.append(sum)
	return list_sum


def documentingAttractor(dataframe,scenario):
	dataframe = dataframe[dataframe.condition == scenario]

	matrix = createMatrix(dataframe,valueToBeDivided)
	# print(matrix[:,78])
	matrix = putRatioRows(matrix)
	sum_in_each_column = sumOfEachColumn(matrix)
	# print(sum_in_each_column)
	# print(dataframe.shape[0])
	return sum_in_each_column



all_data_df = df.copy()
all_data_df = calculateDistanceOriginalUser(all_data_df)
# Calculate side of the square based on the standard deviation as diagonal of square
side_square = (math.sqrt(2)*standardDeviation)/2
print("Side of the square: "+str(side_square))
# Standard Deviation of 10.375 and side of square of 7.336, so lets divide the screen in 14 squares in the horizontal, each of 7.143, and 14 on the vertical.
# 7.143 * 14 = 100.01 .... So we always divide the coordinate by 7.143 and round to the lower int and we will get each quadrant, from 0 until 13. Matrix of 14x14
valueToBeDivided = 7.143

list_calibration = documentingAttractor(all_data_df,"Calibration")
list_calibration = ((list_calibration / sum(list_calibration)) * 100)
list_bottomleft = documentingAttractor(all_data_df,"ClickHereBottomLeft")
list_bottomleft = ((list_bottomleft / sum(list_bottomleft)) * 100)
list_topright = documentingAttractor(all_data_df,"ClickHereTopRight")
list_topright = ((list_topright / sum(list_topright)) * 100)
list_face = documentingAttractor(all_data_df,"Face")
list_face = ((list_face / sum(list_face))* 100)
list_spiralleft = documentingAttractor(all_data_df,"SpiralLeft")
list_spiralleft = ((list_spiralleft / sum(list_spiralleft)) * 100)
list_spiralcenter = documentingAttractor(all_data_df,"SpiralCenter")
list_spiralcenter =((list_spiralcenter/ sum(list_spiralcenter)) * 100)

def printFormat(lista):
	for i in range(13,-1,-1):
		print(i+1)
		print(lista[(i*14):(i*14)+14])

# printFormat(list_calibration)
# print(max(list_calibration))
# print("ClickHereBottomLeft")
# printFormat(list_bottomleft)
# print(max(list_bottomleft))
# printFormat((list_topright))
# print(max(list_topright))
# printFormat((list_face))
# print(max(list_face))
# printFormat((list_spiralleft))
# print(max(list_spiralleft))
printFormat((list_spiralcenter))
print(max(list_spiralcenter))