from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Credito(db.Model):
    __tablename__ = 'creditos'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cliente = db.Column(db.String(100), nullable=False)
    monto = db.Column(db.Float, nullable=False)
    tasa_interes = db.Column(db.Float, nullable=False)
    plazo = db.Column(db.Integer, nullable=False)
    fecha_otorgamiento = db.Column(db.String(10), nullable=False)
    
    def __repr__(self):
        return f'<Credito {self.cliente} - ${self.monto}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'cliente': self.cliente,
            'monto': self.monto,
            'tasa_interes': self.tasa_interes,
            'plazo': self.plazo,
            'fecha_otorgamiento': self.fecha_otorgamiento
        }