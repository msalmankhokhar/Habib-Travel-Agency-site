from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
import os
import random

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
database = SQLAlchemy(app=app)

imageslist = os.listdir('static\img\coverpics')

class Packages(database.Model):
    title = database.Column(database.Text, unique=True, nullable=False)
    slug = database.Column(database.String, primary_key=True)
    room = database.Column(database.String, nullable=True)
    duration = database.Column(database.Integer, nullable=True)
    price = database.Column(database.Integer, nullable=True)

with app.app_context():
    database.create_all()

@app.route('/')
def home():
    random_image = random.choice(imageslist)
    packageList = Packages.query.all()
    return render_template('home.html', packageList=packageList, coverimage_filename=random_image, animation_duration=1000)

@app.route('/admin')
def admin():
    packageList = Packages.query.all()
    return render_template('admin/home.html', packageList=packageList)

@app.route('/admin/add-new-package', methods=['GET', 'POST'])
def add_new_package():
    if request.method == 'GET':
        packageList = Packages.query.all()
        return render_template('admin/addpkg.html')
    elif request.method == 'POST':
        title = request.form.get('title')
        room = request.form.get('room')
        duration = request.form.get('duration')
        price = request.form.get('price')
        slug = title.replace(" ", "-")
        new_pkg = Packages(title=title, duration=duration, room=room, price=price, slug=slug)
        try:
            database.session.add(new_pkg)
            database.session.commit()
            return redirect(url_for('admin'))
        except Exception as e:
            redirect_url = '/admin'
            interval = 10
            e = "oops! an error occured"
            return render_template('error.html', redirect_url=redirect_url, interval=interval, error=e)

@app.route('/admin/edit-package/<string:slug>', methods=['GET', 'POST'])
def edit_package(slug):
    selected_pkg = Packages.query.filter_by(slug=slug).first()
    if request.method == 'GET':
        return render_template('admin/edit-package.html', pkg=selected_pkg)
    elif request.method == 'POST':
        try:
            title = request.form.get('title')
            room = request.form.get('room')
            duration = request.form.get('duration')
            price = request.form.get('price')
            modified_slug = title.replace(" ", "-")
            selected_pkg.title = title
            selected_pkg.slug = modified_slug
            selected_pkg.room =room
            selected_pkg.duration = duration
            selected_pkg.price = price
            database.session.commit()
            return redirect(url_for('admin'))
        except Exception as e:
            redirect_url = '/admin'
            interval = 10
            e = "oops! an error occured"
            return render_template('error.html', redirect_url=redirect_url, interval=interval, error=e)
        

@app.route('/admin/delete-package/<string:slug>')
def del_package(slug):
    pkg = Packages.query.filter_by(slug=slug).first()
    msg = "Package deleted successfully"
    try:
        database.session.delete(pkg)
        database.session.commit()
        return redirect(url_for('admin'))
    except Exception as error:
        return redirect(url_for('admin'))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)