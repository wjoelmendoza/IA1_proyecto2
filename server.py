#!/usr/bin/env python3
from flask import Flask, render_template, url_for, request

app = Flask(__name__)

autor1 = {
    "nombre": "Walter",
    "apellido": "Mendoza"
}

autor2 = {
    "nombre": "Byron",
    "apellido": "López"
}

@app.route("/")
def inicio():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
