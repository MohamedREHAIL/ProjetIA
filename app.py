from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
 
    entreprise = request.form['entreprise']
    entretiens = request.form['entretiens']
  

    return render_template('confirmation.html', entreprise=entreprise, entretiens=entretiens)

if __name__ == '__main__':
    app.run(debug=True)
