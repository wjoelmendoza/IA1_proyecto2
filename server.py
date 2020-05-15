#!/usr/bin/env python3
from flask import Flask, render_template, url_for, request
from Main import predecir
app = Flask(__name__)

autor1 = {
    "nombre": "Walter",
    "apellido": "Mendoza"
}

autor2 = {
    "nombre": "Byron",
    "apellido": "López"
}

@app.route("/", methods=['GET', 'POST'])
def inicio():
    resultado = None
    if request.method == 'POST':
        gen = request.form['genero']
        edad = request.form['edad']
        anno = request.form['anno']
        depto = request.form['depto']
        muni = request.form['mun']
        print(gen, edad, anno, depto, muni, sep=',')
        # ejecutar analisis
        resultado =  predecir(int(gen),int(edad),int(anno),depto,muni)
        print(resultado)
        


    return render_template("index.html", resultado=resultado)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
