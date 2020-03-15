# === Imports === 
import re
import pandas as pd

import convert_to_html

from flask import Flask, render_template, request, redirect

# === Flask ===
# Start application
app = Flask(__name__)

# Application configurations
app.config["FILE_UPLOAD"] = './files' # folder to save uploaded files
app.config["FILE_EXTENSIONS"] = ['.csv'] # permitted extensions
app.config["FILE_REGEX"] = '(.*)_(Metawear_\d+-\d+-\d+T\d+\.\d+\.\d+\.\d+_\w+)_([\w\s]+)_(.*)\.(.*)' # Regex for file names
# Regex sections
# 	1: Name, as given by whoever is using the Metawear app
#	2: Metadata, as given by the app
#	3: Type of data, e.g. Accelerometer, gyroscope
#	4: (Most likely) firmware version of the sensors
#	5: File extension

# === HTML ===
# Home page
@app.route('/', methods=["GET", "POST"])
def home_page(): 
	"""
	Function to handle the home page.
	The home page will have an 'upload' button at the top.
	If anything has been uploaded, the last uploaded file will have its metrics displayed.
	"""
	dataframe = None # Dataframe to hold metrics

	# Check for request
	# If it is a GET, then nothing was posted
	# If it was a POST, then a file was previously uploaded
	if request.method == "GET":
		# Nothing needs to be done
		True

	elif request.method == "POST":
		# Post
		# We ensure there are files to be posted
		if request.files: 

			# Extract uploaded files 
			raw_files = request.files.getlist("files")

			# print(request.files["files"])
			# print(request.files.get('files'))
			# print(request.files["files"] == request.files.get('files'))
			# # print(pd.read_csv(request.files["files"]))
			# print(pd.read_csv(request.files.get('files')))

			# We only extract the files that fit the given extensions
			filtered_files = []

			for extension in app.config["FILE_EXTENSIONS"]:
				filtered_files.extend(list(filter(lambda x: x.filename.endswith(extension), raw_files)))

			# We want to group the files based on their names
			# This should happen before saving it
			# The files, grouped based on their names, should be accessible through a JSON array
			# [TODO] Any file that doesn't come in an accelerometer/gyroscope pair should evoke an error
			# Any 'exceptional case' will be handled by future releases
			jsons = []
			for file in filtered_files:
				# Get the filename
				filename = file.filename 

				# Extract the regex
				regex = re.search(app.config["FILE_REGEX"], filename)

				# Ensure that it is not 'None'
				# [TODO] What if it is None?
				assert regex is not None
				
				# Collect regex groups
				sensor_filename = regex.group(1)
				sensor_metadata = regex.group(2)
				sensor_datatype = regex.group(3)
				sensor_version = regex.group(4)
				sensor_extension = regex.group(5)

				# Set sensor datatype to lowercase
				sensor_datatype = sensor_datatype.lower()

				# Generate extra variables
				complete_filename = sensor_filename + '_' + sensor_metadata

				# Collect existing filenames to be compared
				existing_filenames = [t['name'] for t in jsons]

				# Check if the filename already exists
				if complete_filename in existing_filenames:
					# Loop through each JSON to find the match
					for jx, j in enumerate(jsons):
						if j['name'] == complete_filename:		
							# Assert that the sensor_datatype doesn't already exist
							# [TODO] Something if it already exists because, how could it?

							assert sensor_datatype not in j.keys()

							jsons[jx][sensor_datatype] = file

							break 
							 
				else:
					# None of the files representing the session have been added, so add a new JSON
					jsons.append({
						'name': complete_filename,
						'saved_name': sensor_filename,
						'metadata': sensor_metadata,
						sensor_datatype: file,
						'version': sensor_version
					})

			# Debugging
			# Ensure the collection worked
			# for jx, j in enumerate(jsons):
			# 	print(jx, j)
				
			# We filter only those with complete accelerometer and gyroscope fields
			# In the future, other values may be used and this may have to be changed
			# However, for this version, only accelerometer and gyroscope values are needed
			filtered_jsons = list(filter(lambda x: 'accelerometer' in x.keys() and 'gyroscope' in x.keys(), jsons))

			# Check that #jsons# is the same length as #filtered_jsons#
			# If not, then it suggests some files were not included as they coudn't be paired up ala accelerometer and gyroscope
			# [TODO] If the files could not be included, send a warning/alert
			if len(jsons) == len(filtered_jsons):
				True
			else:
				True

			# We save each file, while setting the 'last file' as the final file in filtered_jsons
			# The last file will be the file with its metrics displayed. 
			# [TODO] We will want to give them a notice that multiple files were uploaded, and thus only the last one is being displayed. 
			j = None 
			
			for j in filtered_jsons: 
				# [TODO] Do not save if it will overwrite
				for file in (j['accelerometer'], j['gyroscope']):
					# Repeat it for the accelerometer and gyroscope files

					try:
						# Ensure it is saved
						file.save(app.config["FILE_UPLOAD"] + '/' + file.filename)
						print('[SAVE SUCCESS] ' + file.filename)

						# Reset stream
						file.stream.seek(0)
					except Exception as e:
						print('[ERROR] ' + file.filename)
						print(e)

			# [TODO] Display metrics
			if j: 
				dataframe = get_metrics(j)
			True

			print(dataframe, type(dataframe))

			# [TODO] Unsure of exact purpose of redirect()
			# It was added mainly due to the URL in the README, under Resources
			# return redirect(request.url)
		else: 
			# There are no files, so we don't do anything
			True

	print(dataframe, type(dataframe))

	return build_page(dataframe)


def build_page(dataframe):
	"""
	The function to build the HTML for the home page. 
	If there are no metrics to display, then it shouldn't bulid the metrics table.
	Otherwise, it should build the metrics table.

	Parameters
	----------
	dataframe (DataFrame())
		Dataframe to be displayed. If None, show nothing. 
	"""
	html = render_template('upload.html')

	if dataframe is not None:
		html += '<hr>'

		html += convert_to_html.dataframe_to_table(dataframe)

	return html


def get_metrics(json):
	"""
	Function to extract the metrics for the given file.

	Parameters
	----------
	json ({}):
		Fields:
			name: 
			saved_name:
			metadata:
			accelerometer:
			gyroscope:
			version: 
	"""
	# Parse into dataframe
	json['accel_df'] = pd.read_csv(json['accelerometer'])
	json['gyro_df'] = pd.read_csv(json['gyroscope'])

	True 

	return copy(json)['accel_df']


def copy(json):
	"""
	Generates a copy of the JSON to be passed into the metric functions. 
	"""
	new_json = {}

	# Strings are immediately copied upon assignment
	new_json['name'] = json['name']
	new_json['saved_name'] = json['saved_name']
	new_json['metadata'] = json['metadata']

	new_json['version'] = json['version']

	# Do not include FileStorage objectes
	new_json['accelerometer'] = None 
	new_json['gyroscope'] = None

	# Add copies of dataframes
	new_json['accel_df'] = json['accel_df'].copy()
	new_json['gyro_df'] = json['gyro_df'].copy()

	return new_json