from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import random
import json
from flask_cors import CORS
import time
from flask_migrate import Migrate

app = Flask(__name__)
cors = CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite"
database = SQLAlchemy(app=app)
migrate = Migrate(app, database)

class Packages(database.Model):    
    id = database.Column(database.String, primary_key=True)
    title = database.Column(database.String, unique=True, nullable=False)
    slug = database.Column(database.String, unique=False, nullable=False)
    makkahHotel = database.Column(database.String, nullable=True)
    madinaHotel = database.Column(database.String, nullable=True)
    makkahDuration = database.Column(database.Integer, nullable=True)
    madinaDuration = database.Column(database.Integer, nullable=True)
    duration = database.Column(database.Integer, nullable=True)
    price = database.Column(database.Integer, nullable=True)

with app.app_context():
    database.create_all()

def generate_id():
    with app.app_context():
        id = str(random.randint(111111,999999))
        idInDB = Packages.query.filter_by(id=id).first()
        if idInDB == None:
            return id
        else:
            generate_id()

@app.route('/api/pkgs')
def api_pkgs():
    pkgListFromDB = Packages.query.all()
    packageList = []
    for pkg in pkgListFromDB:
        obj = {
            'title' : pkg.title,
            'slug' : pkg.slug,
            'makkahHotel' : pkg.makkahHotel, 
            'madinaHotel' : pkg.madinaHotel,
            'makkahDuration' : pkg.makkahDuration,
            'madinaDuration' : pkg.madinaDuration,
            'duration' : pkg.duration,
            'price' : pkg.price
        } 
        packageList.append(obj)
    return {"list" : packageList}

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
        makkahHotel = request.form.get('makkahHotel')
        madinaHotel = request.form.get('madinaHotel')
        makkahDuration = request.form.get('makkahDuration')
        madinaDuration = request.form.get('madinaDuration')
        duration = request.form.get('duration')
        price = request.form.get('price')
        slug = title.replace(" ", "-")
        new_pkg = Packages(
            id = generate_id(),
            title=title,
            duration=duration,
            makkahHotel=makkahHotel,
            madinaHotel=madinaHotel,
            makkahDuration=makkahDuration,
            madinaDuration=madinaDuration,
            price=price,
            slug=slug)
        try:
            database.session.add(new_pkg)
            database.session.commit()
            return redirect(url_for('admin'))
        except Exception as e:
            redirect_url = '/admin'
            interval = 10
            e = "oops! an error occured"
            return render_template('error.html', redirect_url=redirect_url, interval=interval, error=e)

@app.route('/admin/edit-package/<string:id>', methods=['GET', 'POST'])
def edit_package(id):
    selected_pkg = Packages.query.filter_by(id=id).first()
    if request.method == 'GET':
        return render_template('admin/edit-package.html', pkg=selected_pkg)
    elif request.method == 'POST':
        try:
            title = request.form.get('title')
            duration = request.form.get('duration')
            makkahDuration = request.form.get('makkahDuration')
            madinaDuration = request.form.get('madinaDuration')
            makkahHotel = request.form.get('makkahHotel')
            madinaHotel = request.form.get('madinaHotel')
            price = request.form.get('price')
            modified_slug = title.replace(" ", "-")

            selected_pkg.title = title
            selected_pkg.slug = modified_slug
            selected_pkg.duration = duration
            selected_pkg.price = price
            selected_pkg.makkahDuration = makkahDuration
            selected_pkg.madinaDuration = madinaDuration
            selected_pkg.makkahHotel = makkahHotel
            selected_pkg.madinaHotel = madinaHotel

            selected_pkg.database.session.commit()
            return redirect(url_for('admin'))
        except Exception as e:
            return redirect(url_for('admin'))
        

@app.route('/admin/delete-package/<string:id>')
def del_package(id):
    pkg = Packages.query.filter_by(id=id).first()
    msg = "Package deleted successfully"
    try:
        database.session.delete(pkg)
        database.session.commit()
        return redirect(url_for('admin'))
    except Exception as error:
        return redirect(url_for('admin'))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)