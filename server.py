#!/usr/bin/env python3
from flask import Flask, request, url_for, render_template,jsonify
from neural.Util.utils import get_Dataset,generar_json_deps_mun

app = Flask(__name__)
@app.route("/")
def inicio():
    global infodeps
    depss = []
    for key, value in infodeps.items():
        depss.append((key,value['nombre']))
    return render_template("index.html",autor1 = {"nombre":"Byron","apellido":"Lopez"},deps=depss)
@app.route('/getmunis', methods=['POST'])
def getmunis():
    global infodeps
    respmunis = []
    resp = ''
    params = request.form
    print(params)
    id_dep = params['departamento'].encode('utf-8')
    id_dep = int(id_dep)
    dep = infodeps[id_dep]
    lmunis = dep['munis']
    for key, value in lmunis.items():
        respmunis.append((key,value['nombre']))
    for mu in respmunis:
        resp += '<option value="'+ str(mu[0])+'">'+mu[1]+'</option>'

    return resp

@app.route('/predecir', methods=['POST'])
def generar():
   #return render_template("index.html",autor1 = {"nombre":"Walter","apellido":"Mendoza"},autor2 = {"nombre":"Byron","apellido":"Lopez"},mensaje=('','',''))
    '''
    print('LLEGO a generar!!!!!!!!!!!!!!!!!')
    params = request.form
    print(request)
    print(params)
    global _coeficientes
    _coeficientes = iniciar(int(params['frecuencia']),int(params['tipo']))
    
    print("RESP:::::",_coeficientes)
    return create_html_table(_coeficientes)
    '''
    return "ffff"

if __name__ == "__main__":
    infodeps = {}
    infodeps = generar_json_deps_mun()
    #print(infodeps)
    app.run(host="0.0.0.0", port=8080, debug=True)
