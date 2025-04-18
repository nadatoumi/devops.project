from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

# Charger les taux de conversion statiques depuis un fichier JSON
def load_static_rates():
    with open('rates.json', 'r') as file:
        return json.load(file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    # Récupérer les données du formulaire
    amount = request.form['amount']
    from_currency = request.form['from']
    to_currency = request.form['to']

    # Vérifier si le taux de conversion est disponible via l'API
    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        # Si le taux de conversion de la devise cible est trouvé
        if to_currency in data['rates']:
            conversion_rate = data['rates'][to_currency]
            result = float(amount) * conversion_rate
            return render_template('index.html', result=result, to_currency=to_currency)
    
    # Si le taux de conversion n'est pas trouvé, utiliser le fichier JSON statique
    static_rates = load_static_rates()
    if to_currency in static_rates:
        conversion_rate = static_rates[to_currency]
        result = float(amount) * conversion_rate
        return render_template('index.html', result=result, to_currency=to_currency)
    
    # Si la conversion n'est pas possible (ni via l'API ni le fichier statique)
    return render_template('index.html', error="Conversion non disponible pour cette devise")

if __name__ == '__main__':
    app.run(debug=True)
