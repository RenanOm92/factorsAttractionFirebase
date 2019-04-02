import json
import pandas as pd
import matplotlib.pyplot as plt
import math  

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
print(df['ratio'])
#df = df[['email','device','condition','coord_original_X_relative','coord_user_X_relative','coord_original_Y_relative','coord_user_Y_relative', 'version']]

#df = df[df.version == '1.3']

#print(df.groupby(['email']).count())

#print(df)

### DATA CLEANING OF NOISE - Based on the data distribution, Clean all the points where the difference from original and user (heigh and width) is more than 10% from the screen size

df_cleaned = df.copy()

# plt.scatter(df_cleaned.coord_original_X_relative,df_cleaned.coord_user_X_relative, c='green')
# plt.scatter(df_cleaned.coord_original_Y_relative,df_cleaned.coord_user_Y_relative, c='green')
# plt.show()

print("Interactions before cleaning: "+str(df_cleaned.shape[0]))

df_cleaned = df_cleaned[ (abs(df_cleaned.coord_original_X_relative - df_cleaned.coord_user_X_relative)) <= 0.1]
df_cleaned = df_cleaned[ (abs(df_cleaned.coord_original_Y_relative - df_cleaned.coord_user_Y_relative)) <= 0.1]

# plt.scatter(df_cleaned.coord_original_X_relative,df_cleaned.coord_user_X_relative, c='green')
# plt.scatter(df_cleaned.coord_original_Y_relative,df_cleaned.coord_user_Y_relative, c='green')
# plt.show()

print("Interactions after cleaning: "+str(df_cleaned.shape[0]))


def calculateDistanceTwoPoints(x1,y1,x2,y2):  
     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
     return dist

def averageDistanceOriginalUser(dataframe):
	dataframe['distance_between_original_user_in_percentage'] =  dataframe.apply(lambda x: calculateDistanceTwoPoints(x.coord_original_X_relative, x.coord_original_Y_relative, x.coord_user_X_relative, x.coord_user_Y_relative) * 100, axis = 1)
	averageDistance = dataframe['distance_between_original_user_in_percentage'].mean()
	print("Average distance from Original position to User position: "+str(averageDistance)+ '%')

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

def calculateDistanceFromFactorAndPlotPoints(dataframe,threshold):

	dataframe = dataframe[dataframe.coord_user_X_relative >= (dataframe.factor_X - threshold)] 
	dataframe = dataframe[dataframe.coord_user_X_relative <= (dataframe.factor_X + threshold)]
	dataframe = dataframe[dataframe.coord_user_Y_relative >= (dataframe.factor_Y - threshold)]
	dataframe = dataframe[dataframe.coord_user_Y_relative <= (dataframe.factor_Y + threshold)]

	dataframe['distance_factor_to_original'] =  dataframe.apply(lambda loop: calculateDistanceTwoPoints(loop.factor_X, loop.factor_Y, loop['coord_original_X_relative'], loop['coord_original_Y_relative']), axis = 1)
	dataframe['distance_factor_to_user'] = dataframe.apply(lambda loop: calculateDistanceTwoPoints(loop.factor_X, loop.factor_Y, loop['coord_user_X_relative'], loop['coord_user_Y_relative']), axis = 1)
	dataframe['distance_difference_in_percentage'] = ( dataframe['distance_factor_to_original'] - dataframe['distance_factor_to_user'] ) * 100

	df_closer = dataframe.copy()
	df_farther = dataframe.copy()
	df_closer = df_closer[df_closer.distance_difference_in_percentage >= 0]
	df_farther = df_farther[df_farther.distance_difference_in_percentage < 0]

	print("Points which got closer to the attraction factor: "+str(df_closer.shape[0]))
	print("Points which got farther to the attraction factor: "+str(df_farther.shape[0]))
	averageDistanceOriginalUser(dataframe)

	plt.scatter(df_farther.coord_user_X_relative,df_farther.coord_user_Y_relative, c='red', alpha=0.9)
	plt.scatter(df_closer.coord_user_X_relative,df_closer.coord_user_Y_relative, c='green', alpha=0.9)
	plt.scatter(dataframe.factor_X,dataframe.factor_Y, c='blue')
	plt.xlim(0,1)
	plt.ylim(0,1)
	plt.show()

	

### CALCULATION points

df_Calibration = df_cleaned[df_cleaned.condition == 'Calibration']
averageDistanceOriginalUser(df_Calibration)

df_ClickHereBottomLeft = df_cleaned[df_cleaned.condition == 'ClickHereBottomLeft']
df_ClickHereBottomLeft = calculateFactorButtonBottomLeft(df_ClickHereBottomLeft)
calculateDistanceFromFactorAndPlotPoints(df_ClickHereBottomLeft,0.15)

df_ClickHereTopRight = df_cleaned[df_cleaned.condition == 'ClickHereTopRight']
df_ClickHereTopRight = calculateFactorButtonTopRight(df_ClickHereTopRight)
calculateDistanceFromFactorAndPlotPoints(df_ClickHereTopRight,0.15)

df_Face = df_cleaned[df_cleaned.condition == 'Face']
df_Face = calculateFactorFace(df_Face)
calculateDistanceFromFactorAndPlotPoints(df_Face,0.15)

df_SpiralLeft = df_cleaned[df_cleaned.condition == 'SpiralLeft']
df_SpiralLeft = calculateFactorSpiralLeft(df_SpiralLeft)
calculateDistanceFromFactorAndPlotPoints(df_SpiralLeft,0.15)

df_SpiralCenter = df_cleaned[df_cleaned.condition == 'SpiralCenter']
df_SpiralCenter = calculateFactorSpiralCenter(df_SpiralCenter)
calculateDistanceFromFactorAndPlotPoints(df_SpiralCenter,0.15)

