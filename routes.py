from flask import Blueprint, render_template, redirect, url_for, send_file, request, session
from app.boilerplateGenerator import create_boilerplate
from config import Config
import yaml
import stripe
import shutil
import tempfile

main = Blueprint('main', __name__)

stripe_keys = {
    "secret_key": Config.STRIPE_SECRET_KEY,
    "publishable_key": Config.STRIPE_PUBLISHABLE_KEY,
}
stripe.api_key = stripe_keys["secret_key"]

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/build')
def build():
    template_themes = {'darkly':'https://bootswatch.com/5/darkly/bootstrap.css',
                       'flatly':'https://bootswatch.com/5/flatly/bootstrap.css',
                       'journal':'https://bootswatch.com/5/journal/bootstrap.css',
                       'litera':'https://bootswatch.com/5/litera/bootstrap.css',
                       'lux':'https://bootswatch.com/5/lux/bootstrap.css',
                       'minty':'https://bootswatch.com/5/minty/bootstrap.css',
                       'quartz':'https://bootswatch.com/5/quartz/bootstrap.css',
                       'solar':'https://bootswatch.com/5/solar/bootstrap.css',
                       'vapor':'https://bootswatch.com/5/vapor/bootstrap.css'}
    return render_template('build.html', themes=template_themes.keys())

@main.route('/preview', methods=['POST'])
def preview():
    app_name = request.form['app_name'] 
    app_tagline = request.form['app_tagline']
    app_description = request.form['app_description']
    app_theme = request.form['app_theme']
    app_mode = request.form['app_mode']

    session['app_name'] = app_name
    session['app_tagline'] = app_tagline
    session['app_description'] = app_description
    session['app_theme'] = app_theme
    session['app_mode'] = app_mode

    return render_template('preview.html', app_name=app_name, app_tagline=app_tagline, app_description=app_description, app_theme=app_theme, app_mode=app_mode)

@main.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': 'price_1PYG5fEuLRCStLTCNAV4fg0k',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=url_for('main.success', _external=True),
            cancel_url=url_for('main.cancel', _external=True),
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

@main.route('/success')
def success():
    app_name = session['app_name']
    app_tagline = session['app_tagline']
    app_description = session['app_description']
    app_theme = session['app_theme']
    app_mode = session['app_mode']

    return render_template('success.html', app_name=app_name, app_tagline=app_tagline, app_description=app_description, app_theme=app_theme, app_mode=app_mode)

@main.route('/cancel')
def cancel():
    return render_template('cancel.html')

@main.route('/download', methods=['POST'])
def download():
    app_name = session['app_name']
    app_tagline = session['app_tagline']
    app_description = session['app_description']
    app_theme = session['app_theme']
    app_mode = session['app_mode']

    # Zip boilerplate code
    temp_dir = create_boilerplate(app_name, app_tagline, app_description, app_theme, app_mode)
    zip_path = shutil.make_archive(temp_dir, 'zip', temp_dir)
    return send_file(zip_path, as_attachment=True, download_name=app_name.strip().replace(" ", "_")+".zip")

    # # Create config file
    # config_data = {
    #     "name": app_name,
    #     "tagline": app_tagline,
    #     "description": app_description,
    #     "theme": app_theme,
    #     "mode": app_mode,
    #     "application_secret_key": 'your_application_secret_key',
    #     "stripe_secret_key": 'your_stripe_secret_key',
    #     "stripe_publishable_key": 'your_stripe_publishable_key',
    #     "stripe_price_id": 'your_stripe_price_id',
    # }

    # with tempfile.NamedTemporaryFile(delete=False, suffix='.yml', mode='w') as temp_file:
    #     yaml.dump(config_data, temp_file, sort_keys=False)
    #     temp_file_path = temp_file.name

    # # Send the temporary file as an attachment
    # return send_file(temp_file_path, as_attachment=True, download_name='config.yml')
