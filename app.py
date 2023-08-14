from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
database = SQLAlchemy(app=app)

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
    packageList = Packages.query.all()
    return render_template('home.html', packageList=packageList)

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
        return redirect(url_for('admin'))

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