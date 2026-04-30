from flask import Flask, render_template, request, redirect, url_for, jsonify
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

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    busqueda = request.args.get('busqueda', '')
    filtro_caja = request.args.get('caja', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int) # Configurable

    query = Articulo.query
    
    if filtro_caja:
        query = query.filter_by(caja=filtro_caja)
    elif busqueda:
        search = f"%{busqueda}%"
        query = query.filter(
            (Articulo.nombre.like(search)) | 
            (Articulo.descripcion.like(search)) | 
            (Articulo.caja.like(search))
        )
    
    pagination = query.order_by(Articulo.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    items = pagination.items
        
    return render_template('index.html', 
                           items=items, 
                           pagination=pagination, 
                           busqueda=busqueda, 
                           filtro_caja=filtro_caja,
                           per_page=per_page)

@app.route('/api/cajas')
def get_cajas():
    try:
        cajas_raw = db.session.query(Articulo.caja).distinct().all()
        lista_cajas = [str(c[0]) for c in cajas_raw if c[0]]
        return jsonify(lista_cajas)
    except Exception as e:
        return jsonify([]), 500

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
    app.run(host='0.0.0.0', port=5000, debug=True)
