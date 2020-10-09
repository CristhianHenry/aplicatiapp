from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import os
from werkzeug.utils import secure_filename

# inicializacion
app = Flask(__name__)

# Carpeta de subida
app.config['UPLOAD_FOLDER'] = './src/Archivos PDF'

# Conectando con MYSQL
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Supe1404tori'
app.config['MYSQL_DB'] = 'flaskcontacts'
mysql = MySQL(app)

# configuracion
app.secret_key = "mysecretkey"

@app.route('/test')
def test():
    return "Home Page"

@app.route('/test/about/')
def about_test():
    return "About Page"

# Routes to Render Something
@app.route('/')
def home():
    return render_template("home.html")

# routes
@app.route('/about',strict_slashes=False)
def about():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    cur.close()
    return render_template('about.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':

        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        Documento = request.files['Documento']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contacts (fullname, email, phone, Documento) VALUES (%s,%s,%s,%s)", (fullname, email, phone,Documento))
        mysql.connection.commit()
        # obtenemos el archivo del input "archivo"
        f = request.files['Documento']
        filename = secure_filename(f.filename)
        # Guardamos el archivo en el directorio "Archivos PDF"
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Retornamos una respuesta satisfactoria
        flash('Contacto agregado con éxito')

        return redirect(url_for('about'))

#Editar contactos
@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-contact.html', contact = data[0])

#Actualizar contactos
@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts
            SET fullname = %s,
                email = %s,
                phone = %s,
    
            WHERE id = %s
        """, (fullname, email, phone, id))
        flash('Contacto agregado con éxito')
        mysql.connection.commit()
        return redirect(url_for('about'))

#Eliminar contactos
@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contacto agregado con éxito')
    return redirect(url_for('about'))


# iniciando la aplicacion 
if __name__ == "__main__":
    app.run(port=3200, debug=True)
