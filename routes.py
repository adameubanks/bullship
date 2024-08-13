from flask import Blueprint, render_template, redirect, url_for, send_file, request, session, current_app
import stripe
import shutil
from app.boilerplateGenerator import create_boilerplate

main = Blueprint('main', __name__)

@main.before_app_first_request
def setup_stripe():
    # Set Stripe API key
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/build')
def build():
    template_themes = {
        'darkly': 'https://bootswatch.com/5/darkly/bootstrap.css',
        'flatly': 'https://bootswatch.com/5/flatly/bootstrap.css',
        'journal': 'https://bootswatch.com/5/journal/bootstrap.css',
        'litera': 'https://bootswatch.com/5/litera/bootstrap.css',
        'lux': 'https://bootswatch.com/5/lux/bootstrap.css',
        'minty': 'https://bootswatch.com/5/minty/bootstrap.css',
        'quartz': 'https://bootswatch.com/5/quartz/bootstrap.css',
        'solar': 'https://bootswatch.com/5/solar/bootstrap.css',
        'vapor': 'https://bootswatch.com/5/vapor/bootstrap.css'
    }
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
                    'price': current_app.config['STRIPE_PRICE_ID'],  # Access price_id directly from config
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
    app_name = session.get('app_name', 'Unknown App')
    app_tagline = session.get('app_tagline', 'No Tagline')
    app_description = session.get('app_description', 'No Description')
    app_theme = session.get('app_theme', 'No Theme')
    app_mode = session.get('app_mode', 'No Mode')

    return render_template('success.html', app_name=app_name, app_tagline=app_tagline, app_description=app_description, app_theme=app_theme, app_mode=app_mode)

@main.route('/cancel')
def cancel():
    return render_template('cancel.html')

@main.route('/download', methods=['POST'])
def download():
    app_name = session.get('app_name', 'Unknown App')
    app_tagline = session.get('app_tagline', 'No Tagline')
    app_description = session.get('app_description', 'No Description')
    app_theme = session.get('app_theme', 'No Theme')
    app_mode = session.get('app_mode', 'No Mode')

    # Zip boilerplate code
    temp_dir = create_boilerplate(app_name, app_tagline, app_description, app_theme, app_mode)
    zip_path = shutil.make_archive(temp_dir, 'zip', temp_dir)
    return send_file(zip_path, as_attachment=True, download_name=app_name.strip().replace(" ", "_") + ".zip")
