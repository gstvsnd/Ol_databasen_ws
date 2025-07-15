from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from collections import defaultdict
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
    sign = db.Column(db.String(100), nullable=True)
    # Hur gör man om man vill lägga till kolumn?

# Databasen skapas
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    beers = Beer.query.all()

    comp_grouped_beers = defaultdict(list)
    sign_grouped_beers = defaultdict(list) 
    # Listor kommer att behöva sorteras!
    
    for beer in beers:
        comp_grouped_beers[beer.competition].append(beer)
        sign_grouped_beers[beer.sign].append(beer)

    # grouped_beers är en dict med key = sign, value = lista med beers
    return render_template('index.html', beers=beers, comp_grouped_beers=comp_grouped_beers, sign_grouped_beers=sign_grouped_beers)

@app.route('/add_beer', methods=['POST'])
def add_beer():
    name = request.form['name'].strip()
    brewery = request.form['brewery'].strip()
    competition = request.form['competition'].strip()
    sign = request.form['sign'].strip()

    # Dubblettkontroll
    existing = Beer.query.filter_by(name=name, brewery=brewery, competition=competition).first()
    if existing:
        return "Denna öl är redan registrerad för tävlingen!", 400 # 400 betyder att det gick fel (200 = Bra)

    new_beer = Beer(name=name, brewery=brewery, competition=competition, sign=sign)
    db.session.add(new_beer)
    db.session.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
