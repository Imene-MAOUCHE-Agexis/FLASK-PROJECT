from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/pybook'  # Ajout du mot de passe (si nécessaire)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

# Initialisation de l'extension SQLAlchemy
db = SQLAlchemy(app)

# Modèle de données (exemple)
class Contact(db.Model):
    contact_id = db.Column(db.Integer, primary_key=True)
    prenom = db.Column(db.String(50), nullable=False)
    nom = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telephone = db.Column(db.String(20))
    adresse = db.Column(db.String(200))

# Route principale
@app.route('/accueil')
def hello():
    return render_template("index.html")


# Route for displaying contacts
@app.route('/contacts')
def contacts():
    contacts = Contact.query.all()
    return render_template("contacts.html", contacts=contacts)

# Route for adding a contact
@app.route('/add_contact', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        prenom = request.form['prenom']
        nom = request.form['nom']
        email = request.form['email']
        telephone = request.form['telephone']
        adresse = request.form['adresse']

        new_contact = Contact(prenom=prenom, nom=nom, email=email, telephone=telephone, adresse=adresse)
        
        try:
            db.session.add(new_contact)
            db.session.commit()
            return redirect(url_for('contacts'))
        except Exception as e:
            db.session.rollback()
            print(f"Error adding contact: {e}")
    
    return render_template('add_contact.html')






@app.route('/edit_contact')
def edit_contact():
    # Your code for adding a contact goes here
    return render_template('edit_contact.html')





@app.route('/delete_contact', methods=['DELETE'])
def delete_contact():
    # Your code for adding a contact goes here
    return render_template('delete_contact.html')



if __name__ == "__main__":
    with app.app_context():  # Ajout du contexte d'application
        # Création des tables dans la base de données 
        db.create_all()

    app.run(debug=True, port=5000)
