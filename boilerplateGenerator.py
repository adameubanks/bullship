import os
import tempfile
from string import Template
#import requests

def create_boilerplate(name="App Name", tagline="App Tagline", description="App Description", theme="App Theme", mode="Light"):
	temp_dir = tempfile.mkdtemp()
	app_dir = os.path.join(temp_dir, name.strip().replace(" ", "_"))
	os.makedirs(app_dir, exist_ok=True)
	os.makedirs(app_dir+'/templates/', exist_ok=True)
	os.makedirs(app_dir+'/static/', exist_ok=True)

	index_file_path="/home/adam/Projects/Fullstack/bullship/boilerplate/templates/index.html"
	layout_file_path="/home/adam/Projects/Fullstack/bullship/boilerplate/templates/layout.html"
	app_file_path="/home/adam/Projects/Fullstack/bullship/boilerplate/app.py"
	config_file_path="/home/adam/Projects/Fullstack/bullship/boilerplate/config.py"

	# Fetch the existing app.py content from a URL
	# response = requests.get(source_url)
	# if response.status_code == 200:
	# 	content = response.text
	# else:
	# 	raise Exception(f"Failed to fetch app.py from {source_url}. Status code: {response.status_code}")

	with open(index_file_path, 'r') as f:
		index_content = Template(f.read())
	modified_content = index_content.substitute(name=name, tagline=tagline, description=description)
	with open(os.path.join(app_dir+'/templates/', 'index.html'), 'w') as target_file:
		target_file.write(modified_content)

	with open(layout_file_path, 'r') as f:
		layout_content = Template(f.read())
	# Get text color for navbar
	if mode == "dark" or mode == "primary":
		text_color = "text-white"
	else:
		text_color = "text-dark"
	modified_content = layout_content.substitute(name=name, tagline=tagline, theme=theme, mode=mode, text_color=text_color)
	with open(os.path.join(app_dir+'/templates/', 'layout.html'), 'w') as target_file:
		target_file.write(modified_content)

	with open(app_file_path, 'r') as f:
		app_content = f.read()
	with open(os.path.join(app_dir, 'app.py'), 'w') as target_file:
		target_file.write(app_content)

	with open(config_file_path, 'r') as f:
		config_content = f.read()
	with open(os.path.join(app_dir, 'config.py'), 'w') as target_file:
		target_file.write(config_content)

	with open(os.path.join(app_dir, 'requirements.txt'), 'w') as f:
		f.write("Flask==2.0.1\n")

	return temp_dir