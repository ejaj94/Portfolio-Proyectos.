import os
from flask import Flask, render_template

app = Flask(__name__)

# Enforce strict anti-cache headers for instant updates
@app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    print("Iniciando QUINTA DO LAGO LUXURY DENTAL CLINIC em http://localhost:5095")
    app.run(host="0.0.0.0", port=5095, debug=False)
