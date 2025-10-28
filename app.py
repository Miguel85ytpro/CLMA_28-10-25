from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'vladimirxd'

usuarios = []

@app.route('/')
def index():
    usuario = session.get('usuario')
    return render_template('index.html', usuario=usuario)

@app.route('/registro', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        repetir_correo = request.form['repetir_correo']
        contrasena = request.form['contrasena']
        genero = request.form['genero']

        if correo != repetir_correo:
            flash("Los correos no coinciden.")
            return redirect(url_for('register'))

        for u in usuarios:
            if u['correo'] == correo:
                flash("El correo ya está registrado.")
                return redirect(url_for('register'))

        usuarios.append({
            'nombre': nombre,
            'apellido': apellido,
            'correo': correo,
            'contrasena': contrasena,
            'genero': genero
        })

        flash("Registro exitoso. Ahora puedes iniciar sesión.")
        return redirect(url_for('login'))

    usuario = session.get('usuario')
    return render_template('registro.html', usuario=usuario)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contrasena']

        for u in usuarios:
            if u['correo'] == correo and u['contrasena'] == contrasena:
                session['usuario'] = u['nombre']
                flash(f"Bienvenido, {u['nombre']}")
                return redirect(url_for('index'))

        flash("Correo o contraseña incorrectos.")
        return redirect(url_for('login'))

    return render_template('inicio.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash("Has cerrado sesión correctamente.")
    return redirect(url_for('index'))

@app.route('/index')
def home():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
