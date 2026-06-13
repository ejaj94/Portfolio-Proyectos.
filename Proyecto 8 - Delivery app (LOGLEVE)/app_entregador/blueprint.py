import os
import json
from datetime import datetime
from flask import Blueprint, render_template, request, current_app, redirect, url_for, send_from_directory, abort, session
import functools
from werkzeug.utils import secure_filename

from .models import db, Rider
from .services.document_verifier import verify_documents

bp = Blueprint('app_entregador', __name__, url_prefix='/entregador', template_folder='templates')

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf"}

def _allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def login_required(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        if session.get('app_entregador_admin'):
            return fn(*args, **kwargs)
        return redirect(url_for('app_entregador.admin_login', next=request.path))
    return wrapper


@bp.route('/register', methods=['GET'])
def register_form():
    return redirect(url_for('apps_view_blueprint.courier_register'))


@bp.route('/register', methods=['POST'])
def register_rider():
    name = request.form.get('name', '')
    plate = request.form.get('plate', '')
    saved = {}
    upload_dir = current_app.config.get('APP_ENTREGADOR_UPLOADS')
    for key in ('id_doc', 'vehicle_insurance', 'driver_license'):
        f = request.files.get(key)
        if f and f.filename and _allowed(f.filename):
            filename = secure_filename(f"{datetime.utcnow().timestamp()}_{f.filename}")
            dest = os.path.join(upload_dir, filename)
            f.save(dest)
            saved[key] = filename

    result = verify_documents({k: os.path.join(upload_dir, v) for k, v in saved.items()})
    status = 'approved' if all(v['status'] == 'valid' for v in result.values()) else 'rejected'

    rider = Rider(
        name=name, 
        plate=plate, 
        id_doc_path=saved.get('id_doc'), 
        insurance_path=saved.get('vehicle_insurance'), 
        license_path=saved.get('driver_license'), 
        status=status, 
        result_json=json.dumps(result), 
        created_at=datetime.utcnow()
    )
    db.session.add(rider)
    db.session.commit()

    return render_template('rider_status.html', name=name, plate=plate, result=result, status=status, rider=rider)


@bp.route('/uploads/<path:filename>')
@login_required
def uploaded_file(filename):
    upload_dir = current_app.config.get('APP_ENTREGADOR_UPLOADS')
    if '..' in filename or filename.startswith('/'):
        abort(404)
    return send_from_directory(upload_dir, filename)


# Rutas de Administración
@bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        pwd = request.form.get('password', '')
        admin_pwd = current_app.config.get('APP_ADMIN_PASSWORD') or os.environ.get('APP_ADMIN_PASSWORD')
        if pwd and admin_pwd and pwd == admin_pwd:
            session['app_entregador_admin'] = True
            next_url = request.args.get('next') or url_for('app_entregador.admin_list')
            return redirect(next_url)
        error = 'Credenciales incorrectas'
    return render_template('admin_login.html', error=error)


@bp.route('/admin/logout')
def admin_logout():
    session.pop('app_entregador_admin', None)
    return redirect(url_for('app_entregador.register_form'))


@bp.route('/admin', methods=['GET'])
@login_required
def admin_list():
    riders = Rider.query.order_by(Rider.created_at.desc()).all()
    for r in riders:
        try:
            r._parsed = json.loads(r.result_json or '{}')
        except Exception:
            r._parsed = {}
    return render_template('admin_list.html', riders=riders)


@bp.route('/admin/approve/<int:rider_id>', methods=['POST'])
@login_required
def admin_approve(rider_id: int):
    r = db.session.get(Rider, rider_id) or abort(404)
    r.status = 'approved'
    db.session.commit()
    return redirect(url_for('app_entregador.admin_list'))


@bp.route('/admin/reject/<int:rider_id>', methods=['POST'])
@login_required
def admin_reject(rider_id: int):
    r = db.session.get(Rider, rider_id) or abort(404)
    r.status = 'rejected'
    db.session.commit()
    return redirect(url_for('app_entregador.admin_list'))


def init_app(app):
    # Configuración del directorio de subidas
    uploads = os.path.join(os.path.dirname(__file__), 'uploads')
    os.makedirs(uploads, exist_ok=True)
    app.config.setdefault('APP_ENTREGADOR_UPLOADS', uploads)
    
    # Configuración segura de la base de datos relacional para repartidores
    if not app.config.get('SQLALCHEMY_DATABASE_URI'):
        default_db = os.path.join(os.path.dirname(__file__), 'app_entregador.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{default_db}"
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    
    # Inicialización limpia sin colisiones de extensiones
    if 'sqlalchemy' not in app.extensions:
        db.init_app(app)
        with app.app_context():
            db.create_all()
            
    app.register_blueprint(bp)
