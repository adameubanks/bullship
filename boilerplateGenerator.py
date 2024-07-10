import tempfile
import os

def create_boilerplate(name="App Name", description="App Description", theme="App Theme", mode="Light"):
  temp_dir = tempfile.mkdtemp()
  app_dir = os.path.join(temp_dir, "my_flask_app")

  os.makedirs(app_dir)

  # Example files
  with open(os.path.join(app_dir, 'app.py'), 'w') as f:
    f.write(f"""from flask import Flask
    app = Flask(__name__)

    @app.route('/')
    def home():
      return '<h1>Welcome to {name}</h1><p>{description}</p><br><p>Theme: {theme}</p><br><p>Mode: {mode}</p>'

    if __name__ == '__main__':
      app.run(debug=True)
    """)

  with open(os.path.join(app_dir, 'requirements.txt'), 'w') as f:
    f.write("Flask==2.0.1\n")

  return temp_dir