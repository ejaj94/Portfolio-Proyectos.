from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class Rider(db.Model):
    __tablename__ = 'riders'  # Definición explícita del nombre de la tabla

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    plate = db.Column(db.String(50), nullable=True)
    id_doc_path = db.Column(db.String(500), nullable=True)
    insurance_path = db.Column(db.String(500), nullable=True)
    license_path = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(50), nullable=True)
    result_json = db.Column(db.Text, nullable=True)
    
    # Solución moderna compatible con zonas horarias
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Rider {self.id} {self.name} {self.status}>"
