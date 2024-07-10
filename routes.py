from flask import Blueprint, render_template, request, redirect, url_for, send_file
from app.boilerplateGenerator import create_boilerplate
from config import Config
from flask import session
import stripe
import shutil

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
    template_themes = ['darkly', 'flatly', 'journal', 'litera', 'lux', 'minty', 'quartz', 'solar', 'vapor']
    return render_template('build.html', themes=template_themes)

@main.route('/preview', methods=['POST'])
def preview():
    app_name = request.form['app_name'] 
    app_description = request.form['app_description']
    app_theme = request.form['app_theme'] + ".css"
    app_mode = request.form['app_mode']

    session['app_name'] = app_name
    session['app_description'] = app_description
    session['app_theme'] = app_theme
    session['app_mode'] = app_mode

    return render_template('preview.html', app_name=app_name, app_description=app_description, app_theme=app_theme, app_mode=app_mode)

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
    app_description = session['app_description']
    app_theme = session['app_theme']
    app_mode = session['app_mode']

    return render_template('success.html', app_name=app_name, app_description=app_description, app_theme=app_theme, app_mode=app_mode)

@main.route('/cancel')
def cancel():
    return render_template('cancel.html')

@main.route('/download', methods=['POST'])
def download():
    app_name = session['app_name']
    app_description = session['app_description']
    app_theme = session['app_theme']
    app_mode = session['app_mode']

    temp_dir = create_boilerplate(app_name, app_description, app_theme, app_mode)
    zip_path = shutil.make_archive(temp_dir, 'zip', temp_dir)
    return send_file(zip_path, as_attachment=True, download_name=app_name+".zip")
