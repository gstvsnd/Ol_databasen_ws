from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, instance_relative_config=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'beercomp.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Skapa modell för Beer
class Beer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    brewery = db.Column(db.String(100), nullable=False)
    competition = db.Column(db.String(100), nullable=False)

# Se till att instance-mappen finns
os.makedirs(app.instance_path, exist_ok=True)

# Skapa databasen och tabellerna om de inte finns
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    beers = Beer.query.all()  # Hämta alla öl från databasen
    return render_template('index.html', beers=beers)

@app.route('/add', methods=['POST'])
def add_beer():
    name = request.form['name']
    brewery = request.form['brewery']
    competition = request.form['competition']

    new_beer = Beer(name=name, brewery=brewery, competition=competition)
    db.session.add(new_beer)
    db.session.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
