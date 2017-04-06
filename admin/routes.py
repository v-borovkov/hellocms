'''
   Copyright 2017 Volodymyr Borovkov

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''

from flask import Blueprint, render_template, abort, url_for, session, redirect, request
import os.path
import sys
import json
from passlib.hash import pbkdf2_sha256
from slugify import slugify
from werkzeug.utils import secure_filename
from flask import send_from_directory
from PIL import Image

admin_blueprint = Blueprint('admin', __name__,
                            template_folder='templates',
                            static_folder='static')

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
IMAGE_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

"""
Dashboard
"""
@admin_blueprint.route('/')
def admin_dash():
    if 'username' in session:
        path = 'content'
        num_files = len([f for f in os.listdir(path)if os.path.isfile(os.path.join(path, f))])
        upath = 'users'
        num_ufiles = len([f for f in os.listdir(upath)if os.path.isfile(os.path.join(upath, f))])
        mpath = 'static/media'
        num_mfiles = len([f for f in os.listdir(mpath)if os.path.isfile(os.path.join(mpath, f))])
        return render_template('admin.html', num_page = num_files, num_users = num_ufiles, num_media = num_mfiles, user = session['username'])
    return redirect(url_for('admin.login'))

"""
Login Form
"""
@admin_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('admin.admin_dash'))
    if request.method == 'POST':
        if not os.path.isfile("users/%s.json" % request.form['username']):
            error = "Wrong username or password, please try again."
            return render_template("login.html", error=error)
        file = open("users/%s.json" % request.form['username'], "r+")
        json_data = json.loads(file.read())
        password = json_data['password']
        if pbkdf2_sha256.verify(request.form['password'], password):
            session['username'] = request.form['username']
            return redirect(url_for('admin.admin_dash'))
        else:
            error = "Wrong username or password, please try again."
            return render_template("login.html", error=error)
    return render_template("login.html")

@admin_blueprint.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


"""
Pages
"""
@admin_blueprint.route('/pages')
def admin_pages():
    if 'username' in session:
        path = 'content'
        files = [f for f in os.listdir(path)if os.path.isfile(os.path.join(path, f))]
        return render_template('admin_pages.html', name = files, user = session['username'])
    return redirect(url_for('admin.login'))

@admin_blueprint.route('/newpage', methods=['GET', 'POST'])
def admin_newpage():
    if 'username' in session:
        if request.method == 'POST':
            page_name = request.form['title']
            file = open("content/%s.json" % page_name, "a")
            file.write(json.dumps({"author": "", "title": "%s" % page_name, "content": "", "widgets": [], "date": "", "slug": ""}))
            return redirect(url_for('admin.admin_pages'))
        return render_template('admin_newpage.html', user = session['username'])
    return redirect(url_for('admin.login'))

@admin_blueprint.route('/pages/<string:page_name>/', methods=['GET', 'POST'])
def admin_pagedetail(page_name):
    if 'username' in session:
        if not os.path.isfile("content/%s.json" % page_name):
            abort(404)
        file = open("content/%s.json" % page_name, "r+")
        json_data = json.loads(file.read())
        title = json_data['title']
        slug = json_data['slug']
        content = json_data['content']
        file.close()
        if request.method == 'POST':
            json_data['content'] = request.form['content']
            json_data['title'] = request.form['title']
            slugpage = slugify(request.form['title'])
            json_data['slug'] = slugpage
            os.rename("content/%s.json" % page_name, "content/%s.json" % slugpage)
            file = open("content/%s.json" % slugpage, "w+")
            file.write(json.dumps(json_data))
            return redirect(url_for('admin.admin_pagedetail', page_name = slugpage))
        return render_template('admin_pagedetail.html', page_name = page_name, title = title, slug = slug, content = content, user = session['username'])
    return redirect(url_for('admin.login'))

@admin_blueprint.route('/pages/delete/<string:page_name>/', methods=['GET', 'POST'])
def admin_pages_delete(page_name):
    if 'username' in session:
        os.remove("content/%s.json" % page_name)
        return redirect(url_for('admin.admin_pages'))
    return redirect(url_for('admin.login'))

"""
Menu
"""
@admin_blueprint.route('/menu', methods=['GET', 'POST'])
def admin_menu():
    if 'username' in session:
        file = open("menu.json", "r")
        json_data = json.loads(file.read())
        title = json_data['menu']
        path = 'content'
        files = [f for f in os.listdir(path)if os.path.isfile(os.path.join(path, f))]
        if request.method == 'POST':
            file = open("menu.json", "w+")
            #test = [x for x in [request.form.getlist['title']]]
            json_data['menu'] = request.form.getlist('title')
            #print test
            file.write(json.dumps(json_data))
            return redirect(url_for('admin.admin_menu'))
        return render_template('admin_menu.html', files = files, name = title, user = session['username'])
    return redirect(url_for('admin.login'))

"""
Media
"""
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def image_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in IMAGE_EXTENSIONS

@admin_blueprint.route('/media', methods=['GET', 'POST'])
def admin_media():
    if 'username' in session:
        path = 'static/media'
        files = [f for f in os.listdir(path)if os.path.isfile(os.path.join(path, f))]
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join("static/media/", filename))
                if image_file(file.filename):
                    thumb = Image.open("static/media/%s" % filename)
                    thumb = thumb.resize((128,128))
                    thumb.save("static/media/thumb/%s" % filename)
                return redirect(url_for('admin.uploaded_file',
                                        filename=filename))
        return render_template('admin_media.html',  name = files, user = session['username'])
    return redirect(url_for('admin.login'))

@admin_blueprint.route('/uploads/<filename>')
def uploaded_file(filename):
    if 'username' in session:
        name = "../../static/media/%s" % filename
        return render_template('admin_mediadetail.html',  name = name, user = session['username'])
    return redirect(url_for('admin.login'))

@admin_blueprint.route('/media/delete/<string:media_name>/', methods=['GET', 'POST'])
def admin_media_delete(media_name):
    if 'username' in session:
        os.remove("static/media/%s" % media_name)
        if os.path.isfile("static/media/thumb/%s" % media_name):
            os.remove("static/media/thumb/%s" % media_name)
        return redirect(url_for('admin.admin_media'))
    return redirect(url_for('admin.login'))

"""
Plugins
"""

"""
Themes
"""

"""
Users
"""
@admin_blueprint.route('/users')
def admin_users():
    if 'username' in session:
        path = 'users'
        files = [f for f in os.listdir(path)if os.path.isfile(os.path.join(path, f))]
        return render_template('admin_users.html', name = files, user = session['username'])
    return redirect(url_for('admin.login'))

@admin_blueprint.route('/newuser', methods=['GET', 'POST'])
def admin_newuser():
    if 'username' in session:
        if request.method == 'POST':
            user_name = request.form['username']
            user_password = pbkdf2_sha256.hash(request.form['password'])
            file = open("users/%s.json" % user_name, "a")
            file.write(json.dumps({"username": "%s" % user_name, "password": "%s" % user_password}))
            return redirect(url_for('admin.admin_users'))
        return render_template('admin_newuser.html', user = session['username'])
    return redirect(url_for('admin.login'))

@admin_blueprint.route('/users/<string:user_name>/', methods=['GET', 'POST'])
def admin_userdetail(user_name):
    if 'username' in session:
        if not os.path.isfile("users/%s.json" % user_name):
            abort(404)
        file = open("users/%s.json" % user_name, "r+")
        json_data = json.loads(file.read())
        username = json_data['username']
        #content = json_data['content']
        if request.method == 'POST':
            #json_data['content'] = request.form['content']
            json_data['username'] = request.form['username']
            file = open("users/%s.json" % user_name, "w+")
            file.write(json.dumps(json_data))
            return redirect(url_for('admin.admin_userdetail', user_name = user_name))
        return render_template('admin_userdetail.html', username = username, user = session['username'])
    return redirect(url_for('admin.login'))

@admin_blueprint.route('/users/delete/<string:user_name>/', methods=['GET', 'POST'])
def admin_users_delete(user_name):
    if 'username' in session:
        os.remove("users/%s.json" % user_name)
        return redirect(url_for('admin.admin_users'))
    return redirect(url_for('admin.login'))

"""
Settings
"""
@admin_blueprint.route('/settings', methods=['GET', 'POST'])
def admin_settings():
    if 'username' in session:
        path = 'content'
        path2 = 'themes'
        themes = [f for f in os.listdir(path2)if os.path.isdir(os.path.join(path2, f))]
        files = [f for f in os.listdir(path)if os.path.isfile(os.path.join(path, f))]
        file = open("config.json", "r+")
        json_data = json.loads(file.read())
        currentTheme = json_data['theme']
        currentStartpage = json_data['startpage']
        if request.method == 'POST':
            file = open("config.json", "w+")
            #print currentStartpage
            if request.form.get("startpage", False):
                json_data['startpage'] = request.form['startpage']
            else:
                json_data['startpage'] = currentStartpage
            if request.form.get("theme", False):
                json_data['theme'] = request.form['theme']
            else:
                json_data['theme'] = currentTheme
            file.write(json.dumps(json_data))
            return redirect(url_for('admin.admin_settings'))
        return render_template('admin_settings.html', page_name = files, themes = themes, current_theme = currentTheme, current_startpage = currentStartpage, user = session['username'])
    return redirect(url_for('admin.login'))
