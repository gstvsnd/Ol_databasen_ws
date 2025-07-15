from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, instance_relative_config=True)

# Konfigurera databasens sökväg
os.makedirs(app.instance_path, exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'beers.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modell
class Beer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    brewery = db.Column(db.String(100), nullable=False)
    competition = db.Column(db.String(100), nullable=False)

# Skapa databasen
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    beers = Beer.query.all()
    return render_template('index.html', beers=beers)

@app.route('/add_beer', methods=['POST'])
def add_beer():
    name = request.form['name'].strip()
    brewery = request.form['brewery'].strip()
    competition = request.form['competition'].strip()

    # Dubblettkontroll
    existing = Beer.query.filter_by(name=name, competition=competition).first()
    if existing:
        return "Denna öl är redan registrerad för tävlingen!", 400

    new_beer = Beer(name=name, brewery=brewery, competition=competition)
    db.session.add(new_beer)
    db.session.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
