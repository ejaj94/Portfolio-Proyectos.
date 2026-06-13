import os
import time
from datetime import datetime, timedelta

from models import db, Rider

def clean_uploads(app, days: int = 30):
    uploads = app.config.get('UPLOAD_FOLDER')
    cutoff = datetime.utcnow() - timedelta(days=days)
    removed = []
    with app.app_context():
        for r in Rider.query.all():
            for attr in ('id_doc_path', 'insurance_path', 'license_path'):
                fn = getattr(r, attr)
                if not fn:
                    continue
                path = os.path.join(uploads, fn)
                try:
                    if os.path.exists(path):
                        mtime = datetime.utcfromtimestamp(os.path.getmtime(path))
                        if mtime < cutoff:
                            os.remove(path)
                            removed.append(path)
                except Exception:
                    continue
    return removed

if __name__ == '__main__':
    # script para ejecutar manualmente
    from app import create_app
    app = create_app()
    removed = clean_uploads(app, days=30)
    print('Removed files:')
    for p in removed:
        print('-', p)
