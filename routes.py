from flask import Blueprint, render_template, request, redirect, url_for
from config import Config
import stripe


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
    app_theme = request.form['app_theme'] + ".css"
    app_mode = request.form['app_mode']
    return render_template('preview.html', app_name=app_name, app_theme=app_theme, app_mode=app_mode)

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
    return render_template('success.html', app_name="App Name", app_theme="App Theme", app_mode="App Mode")

@main.route('/cancel')
def cancel():
    return render_template('cancel.html')