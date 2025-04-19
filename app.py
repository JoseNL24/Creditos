from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from database import db, Credito
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///creditos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '12345'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    creditos = Credito.query.order_by(Credito.id.desc()).all()
    return render_template('index.html', creditos=creditos)

@app.route('/creditos/nuevo', methods=['GET', 'POST'])
def nuevo_credito():
    if request.method == 'POST':
        try:
            if not all(key in request.form for key in ['cliente', 'monto', 'tasa_interes', 'plazo', 'fecha_otorgamiento']):
                flash('Todos los campos son requeridos', 'error')
                return redirect(url_for('nuevo_credito'))
            
            nuevo_credito = Credito(
                cliente=request.form['cliente'],
                monto=float(request.form['monto']),
                tasa_interes=float(request.form['tasa_interes']),
                plazo=int(request.form['plazo']),
                fecha_otorgamiento=request.form['fecha_otorgamiento']
            )
            
            db.session.add(nuevo_credito)
            db.session.commit()
            flash('Crédito agregado exitosamente', 'success')
            return redirect(url_for('index'))
        except ValueError as e:
            flash('Error en los datos: ' + str(e), 'error')
        except Exception as e:
            flash('Error al agregar el crédito: ' + str(e), 'error')

    return render_template('agregar_editar.html', credito=None)

@app.route('/creditos/<int:id>/editar', methods=['GET', 'POST'])
def editar_credito(id):
    credito = Credito.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            credito.cliente = request.form['cliente']
            credito.monto = float(request.form['monto'])
            credito.tasa_interes = float(request.form['tasa_interes'])
            credito.plazo = int(request.form['plazo'])
            credito.fecha_otorgamiento = request.form['fecha_otorgamiento']
            
            db.session.commit()
            flash('Crédito actualizado exitosamente', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash('Error al actualizar: ' + str(e), 'error')
    
    return render_template('agregar_editar.html', credito=credito)

@app.route('/creditos/<int:id>/eliminar', methods=['POST'])
def eliminar_credito(id):
    credito = Credito.query.get_or_404(id)
    try:
        db.session.delete(credito)
        db.session.commit()
        flash('Crédito eliminado exitosamente', 'success')
    except Exception as e:
        flash('Error al eliminar: ' + str(e), 'error')
    return redirect(url_for('index'))

@app.route('/api/creditos')
def api_creditos():
    creditos = Credito.query.all()
    return jsonify([credito.to_dict() for credito in creditos])

@app.route('/grafica')
def mostrar_grafica():
    creditos = Credito.query.all()
    
    if not creditos:
        return render_template('grafica.html', plot_url=None)
    
    clientes = [credito.cliente for credito in creditos]
    montos = [credito.monto for credito in creditos]
    
    plt.figure(figsize=(10, 6))
    plt.bar(clientes, montos)
    plt.xlabel('Clientes')
    plt.ylabel('Monto del Crédito')
    plt.title('Créditos Otorgados por Cliente')
    plt.xticks(rotation=45)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    return render_template('grafica.html', plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)