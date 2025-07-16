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
    # Viktigaste komponenterna
    id = db.Column(db.Integer, primary_key=True)                  # ID
    name = db.Column(db.String(100), nullable=False)              # Namn på Öl
    brewery = db.Column(db.String(100), nullable=False)            # Bryggeri - ursprung
    competition = db.Column(db.String(100), nullable=False)       # Tävlingsevenemang

    # Info som kan vara kul (men inte nödvändig)
    sign = db.Column(db.String(100), nullable=True)               # Vem som Bidrog med Ölen
    score = db.Column(db.Float, nullable=True)                    # Betyg (kanske 1-10)
    comment = db.Column(db.Text, nullable=True)                   # Kommentar (hur lång som hellst)

# Databasen skapas
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    beers = Beer.query.all()

    grouped_beers = defaultdict(lambda: defaultdict(list))
    for beer in beers:
        grouped_beers[beer.competition][beer.sign].append(beer)
    # Listor kommer att behöva sorteras!


    # grouped_beers är en dict med key = sign, value = lista med beers
    return render_template('index.html', beers=beers, grouped_beers=grouped_beers)

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
