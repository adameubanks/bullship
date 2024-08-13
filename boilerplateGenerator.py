from string import Template
import tempfile
import os

def generate_variables_code(variables):
	# Generate Python code for app.py based on user-defined variables.
	variables_code = ""
	for variable in variables:
		safe_name = variable['name'].replace(' ', '_')
		variables_code += f'''
    {safe_name} = request.form.get('{variable['name']}', '')
    session['{safe_name}'] = {safe_name}'''
  
	return variables_code

def generate_render_variables(variables):
	# Generate variable names for render_template() in success route.
	render_vars = ', '.join([f'{var["name"].replace(" ", "_")} = session.get("{var["name"]}")' for var in variables])
	render_vars = ', '.join([f'{var["name"].replace(" ", "_")}={var["name"].replace(" ", "_")}' for var in variables])
	return render_vars

def create_boilerplate(name="App Name", tagline="App Tagline", description="App Description", theme="App Theme", mode="Light", variables={}):
	temp_dir = tempfile.mkdtemp()
	app_dir = os.path.join(temp_dir, name.strip().replace(" ", "_"))
	os.makedirs(app_dir, exist_ok=True)

	# Templates
	os.makedirs(app_dir+'/templates/', exist_ok=True)

	layout_file_path="./boilerplate/templates/layout.html"
	index_file_path="./boilerplate/templates/index.html"
	form_file_path="./boilerplate/templates/form.html"
	success_file_path="./boilerplate/templates/success.html"
	cancel_file_path="./boilerplate/templates/cancel.html"

	with open(layout_file_path, 'r') as f:
		layout_content = Template(f.read())
	if mode == "dark" or mode == "primary":
		text_color = "text-white"
	else:
		text_color = "text-dark"
	modified_content = layout_content.substitute(name=name, tagline=tagline, theme=theme, mode=mode, text_color=text_color)
	with open(os.path.join(app_dir+'/templates/', 'layout.html'), 'w') as target_file:
		target_file.write(modified_content)
	
	with open(index_file_path, 'r') as f:
		index_content = Template(f.read())
	modified_content = index_content.substitute(name=name, tagline=tagline, description=description)
	with open(os.path.join(app_dir+'/templates/', 'index.html'), 'w') as target_file:
		target_file.write(modified_content)

	# Generate form.html dynamically
	form_fields = ""
	for variable in variables:
		if variable['type'] == 'text':
			form_fields += f'''
				<div class="form-group">
					<label for="{variable['name']}">{variable['name']}</label>
					<input type="text" class="form-control" id="{variable['name']}" name="{variable['name']}" required>
				</div>
			'''
		elif variable['type'] == 'number':
			form_fields += f'''
				<div class="form-group">
					<label for="{variable['name']}">{variable['name']}</label>
					<input type="number" class="form-control" id="{variable['name']}" name="{variable['name']}" required></textarea>
				</div>
					'''
		elif variable['type'] == 'dropdown':
			options = "\n".join([f'<option value="{item}">{item}</option>' for item in variable['dropdown_items']])
			form_fields += f'''
				<div class="form-group">
					<label for="{variable['name']}">{variable['name']}</label>
					<select class="form-control" id="{variable['name']}" name="{variable['name']}" required>
						{options}
					</select>
				</div>
			'''

	with open(form_file_path, 'r') as f:
		form_content = Template(f.read())
	modified_form_content = form_content.substitute(form_fields=form_fields)
	with open(os.path.join(app_dir+'/templates/', 'form.html'), 'w') as target_file:
		target_file.write(modified_form_content)

	with open(success_file_path, 'r') as f:
		success_content = f.read()
	with open(os.path.join(app_dir+'/templates/', 'success.html'), 'w') as target_file:
		target_file.write(success_content)

	with open(cancel_file_path, 'r') as f:
		cancel_content = f.read()
	with open(os.path.join(app_dir+'/templates/', 'cancel.html'), 'w') as target_file:
		target_file.write(cancel_content)
	
	# Static files
	os.makedirs(app_dir+'/static/', exist_ok=True)
	os.makedirs(app_dir+'/static/css', exist_ok=True)
	os.makedirs(app_dir+'/static/img', exist_ok=True)

	css_file_path="./boilerplate/static/css/main.css"
	favicon_file_path="./boilerplate/static/img/favicon.ico"
	logo_file_path="./boilerplate/static/img/logo.svg"

	with open(css_file_path, 'r') as f:
		css_content = f.read()
	with open(os.path.join(app_dir+'/static/css', 'main.css'), 'w') as target_file:
		target_file.write(css_content)

	with open(favicon_file_path, 'rb') as f:
		favicon_content = f.read()
	with open(os.path.join(app_dir+'/static/img', 'favicon.ico'), 'wb') as target_file:
		target_file.write(favicon_content)

	with open(logo_file_path, 'rb') as f:
		logo_content = f.read()
	with open(os.path.join(app_dir+'/static/img', 'logo.svg'), 'wb') as target_file:
		target_file.write(logo_content)
	
	# App files
	app_file_path="./boilerplate/app.py"
	config_file_path="./boilerplate/config.py"
	readme_file_path="./boilerplate/README.md"

	with open(app_file_path, 'r') as f:
		app_content = f.read()

	# Prepare dynamic variables code
	variables_code = generate_variables_code(variables)
	render_variables = generate_render_variables(variables)
	app_content = app_content.replace("{VARIABLES_HERE}", variables_code)
	app_content = app_content.replace("{VARIABLES_RENDER_HERE}", render_variables)

	with open(os.path.join(app_dir, 'app.py'), 'w') as target_file:
		target_file.write(app_content)

	with open(config_file_path, 'r') as f:
		config_content = f.read()
	with open(os.path.join(app_dir, 'config.py'), 'w') as target_file:
		target_file.write(config_content)

	with open(readme_file_path, 'r') as f:
		readme_content = f.read()
	with open(os.path.join(app_dir, 'README.md'), 'w') as target_file:
		target_file.write(readme_content)

	with open(os.path.join(app_dir, 'requirements.txt'), 'w') as f:
		f.write("Flask==2.0.1\n")
		f.write("stripe\n")

	return temp_dir