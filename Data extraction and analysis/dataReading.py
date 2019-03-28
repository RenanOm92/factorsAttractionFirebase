import json
import pandas as pd
import matplotlib.pyplot as plt
import math 

def calculateDistance(x1,y1,x2,y2):  
     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
     return dist  

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

#df = df[['email','device','condition','coord_original_X_relative','coord_user_X_relative','coord_original_Y_relative','coord_user_Y_relative', 'version']]

#df = df[df.version == '1.3']



#print(df.groupby(['email']).count())

#print(df)

### DATA CLEANING OF NOISE

#to do

#plt.scatter(df.coord_original_left_relative,df.coord_user_left_relative, c='yellow')
#plt.scatter(df.coord_original_top_relative,df.coord_user_top_relative, c='blue', alpha=0.5)
#plt.show()

### CALCULATION FACTOR OF ATTRACTION POSITION OF FACE

ratio_face_image1 = 1280/720
ratio_face_image2 = 720/1280

def calculateFaceFactor(df):
	df['ratio_screen_size'] = df['width'] / df['height']

	df['axes_to_calculate_img_size'] = df.apply(lambda x: 'X' if (x['ratio_screen_size'] < ratio_face_image1) else 'Y')

	df['img_size_width'] = df.apply(lambda x: x['width'] if (x['axes_to_calculate_img_size'] == 'X') else (x['height'] * ratio_face_image1))
	df['img_size_height'] = df.apply(lambda x: (x['width'] * ratio_face_image2) if (x['axes_to_calculate_img_size'] == 'X') else x['height'])

	df['factor_face_X'] = 0.55

	#((screen size - img size) / 2  + % img size) / screen size





### CALCULATION points

df_ClickHereBottomLeft = df[df.condition == 'ClickHereBottomLeft']

threshold = 0.15
button_X = 0.2
button_Y = 0.2

df_ClickHereBottomLeft = df_ClickHereBottomLeft[df_ClickHereBottomLeft.coord_user_X_relative >= (button_X - threshold)] 
df_ClickHereBottomLeft = df_ClickHereBottomLeft[df_ClickHereBottomLeft.coord_user_X_relative <= (button_X + threshold)]
df_ClickHereBottomLeft = df_ClickHereBottomLeft[df_ClickHereBottomLeft.coord_user_Y_relative >= (button_Y - threshold)]
df_ClickHereBottomLeft = df_ClickHereBottomLeft[df_ClickHereBottomLeft.coord_user_Y_relative <= (button_Y + threshold)]

df_ClickHereBottomLeft['distance_factor_to_original'] =  df_ClickHereBottomLeft.apply(lambda x: calculateDistance(button_X,button_Y,x['coord_original_X_relative'],x['coord_original_Y_relative']), axis = 1)
df_ClickHereBottomLeft['distance_factor_to_user'] = df_ClickHereBottomLeft.apply(lambda x: calculateDistance(button_X,button_Y,x['coord_user_X_relative'],x['coord_user_Y_relative']), axis = 1)
df_ClickHereBottomLeft['distance_difference'] = df_ClickHereBottomLeft['distance_factor_to_original'] - df_ClickHereBottomLeft['distance_factor_to_user']
df_ClickHereBottomLeft['distance_difference_in_percentage'] = df_ClickHereBottomLeft['distance_difference'] * 100

df_closer = df_ClickHereBottomLeft.copy()
df_farther = df_ClickHereBottomLeft.copy()
df_closer = df_closer[df_closer.distance_difference >= 0]
df_farther = df_farther[df_farther.distance_difference < 0]

print(df_ClickHereBottomLeft.distance_difference_in_percentage)

plt.scatter(df_closer.coord_user_X_relative,df_closer.coord_user_Y_relative, c='green')
plt.scatter(df_farther.coord_user_X_relative,df_farther.coord_user_Y_relative, c='red')
plt.scatter(button_X,button_Y, c='blue')
plt.xlim(0,1)
plt.ylim(0,1)
plt.show()


