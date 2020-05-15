#!/usr/bin/env python3
from flask import Flask

app = Flask(__name__)

@app.route("/")
def inicio():
    return "Hola mundo!"

@app.route('/predecir', methods=['POST'])
def generar():
   #return render_template("index.html",autor1 = {"nombre":"Walter","apellido":"Mendoza"},autor2 = {"nombre":"Byron","apellido":"Lopez"},mensaje=('','',''))
    print('LLEGO a generar!!!!!!!!!!!!!!!!!')
    params = request.form
    print(request)
    print(params)
    global _coeficientes
    _coeficientes = iniciar(int(params['frecuencia']),int(params['tipo']))
    
    print("RESP:::::",_coeficientes)
    return create_html_table(_coeficientes)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
