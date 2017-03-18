from flask import Flask, render_template, abort, url_for, session, redirect, request
import os.path
import sys
import json
from admin.routes import admin_blueprint
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '../static/media'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def updateStartpage():
    config_file = open("config.json", "r")
    config_data = json.loads(config_file.read())
    STARTPAGE = config_data['startpage']
    config_file.close()
    return STARTPAGE

def updateTheme():
    config_file = open("config.json", "r")
    config_data = json.loads(config_file.read())
    THEME = config_data['theme']
    config_file.close()
    return THEME

def updateMenu():
    menu_file = open("menu.json", "r")
    menu_data = json.loads(menu_file.read())
    MENU = menu_data['menu']
    menu_file.close()
    return MENU


app = Flask(__name__, template_folder="themes/")

app.register_blueprint(admin_blueprint, url_prefix='/admin')

app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config.update(
    TEMPLATES_AUTO_RELOAD = True
)
# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

csrf = CSRFProtect(app)

@app.route('/')
def index():
    STARTPAGE = updateStartpage()
    menu = updateMenu()
    theme = updateTheme()
    app.run
    if not os.path.isfile("content/%s.json" % STARTPAGE):
        abort(404)
    file = open("content/%s.json" % STARTPAGE, "r")
    json_data = json.loads(file.read())
    content = json_data['content']
    return render_template('%s/home.html' % theme, theme=theme, menu = menu, content = content)

@app.route('/<string:page_name>/')
def render_content(page_name):
    menu = updateMenu()
    theme = updateTheme()
    if not os.path.isfile("content/%s.json" % page_name):
        abort(404)
    file = open("content/%s.json" % page_name, "r")
    json_data = json.loads(file.read())
    content = json_data['content']
    return render_template('%s/temp.html' % theme, theme = theme, menu = menu, title = page_name, content = content)

@app.errorhandler(404)
def page_not_found(error):
    theme = updateTheme()
    return render_template('%s/page_not_found.html' % theme), 404

if __name__ == "__main__":
    app.run()
