import os
from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
@app.route('/showcase')
def showcase():
    return render_template('showcase.html')

if __name__ == '__main__':
    print("[Starting Showcase Server] Host: http://127.0.0.1:8080 ...")
    app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False)
