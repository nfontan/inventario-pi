from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventario.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de la base de datos
class Articulo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, default=1)
    descripcion = db.Column(db.String(200))
    caja = db.Column(db.String(50), nullable=False)

# Crear la base de datos
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    busqueda = request.args.get('busqueda', '')
    filtro_caja = request.args.get('caja', '')
    
    query = Articulo.query
    
    if filtro_caja:
        items = query.filter_by(caja=filtro_caja).all()
    elif busqueda:
        search_format = f"%{busqueda}%"
        items = query.filter(
            (Articulo.nombre.like(search_format)) | 
            (Articulo.descripcion.like(search_format)) | 
            (Articulo.caja.like(search_format))
        ).all()
    else:
        items = query.all()
        
    return render_template('index.html', items=items, busqueda=busqueda, filtro_caja=filtro_caja)

@app.route('/agregar', methods=['POST'])
def agregar():
    nuevo = Articulo(
        nombre=request.form['nombre'],
        cantidad=request.form['cantidad'] or 1,
        descripcion=request.form['descripcion'],
        caja=request.form['caja']
    )
    db.session.add(nuevo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    item = Articulo.query.get_or_404(id)
    if request.method == 'POST':
        item.nombre = request.form['nombre']
        item.cantidad = request.form['cantidad']
        item.descripcion = request.form['descripcion']
        item.caja = request.form['caja']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('editar.html', item=item)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    item = Articulo.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # host='0.0.0.0' permite que entres desde otros dispositivos usando la IP de la Pi
    app.run(host='0.0.0.0', port=5000, debug=True)
