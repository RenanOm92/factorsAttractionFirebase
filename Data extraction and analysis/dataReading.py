import json
import pandas as pd

### LOAD DATA INTO DATAFRAME

versions = ['1.0','1.1','1.2','1.3']

df = pd.DataFrame()

# Open the json file and loads
with open('factorsAttraction.json') as json_data:
	obj = json.load(json_data)

	# Iterate for every version
	for version in versions:
		print(version)
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

df['coord_original_left_relative'] = df['coord_original_left'] / df['width']
df['coord_user_left_relative'] = df['coord_user_left'] / df['width']
df['coord_original_top_relative'] = df['coord_original_top'] / df['height']
df['coord_user_top_relative'] = df['coord_user_top'] / df['height']

df = df[['email','device','condition','coord_original_left_relative','coord_user_left_relative','coord_original_top_relative','coord_user_top_relative']]

print(df)