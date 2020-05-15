from neural.Util.ReadFile import get_dataFile
from neural.Util import Plotter
from neural.Neural_Network.Data import Data
from neural.Neural_Network.Model import NN_Model
from neural.Util.utils import get_Dataset
import numpy as np
import codecs, json 
#-----------------------------
from random import randint, random, uniform
#----------------
ONLY_SHOW = False
ENTRENO = False
#----------------------------
_hiperparametros = [
    [0.00001,0.00005,0.0001,0.0003,0.001,0.005,0.01,0.05,0.1,0.5],
    [0,0.01,0.05,0.1,0.5,1,1.5,2,5,7],
    #[500,750,1250,1500,2000,4000,7500,15000,20000,25000],
    [100,100,100,100,100,100,99,100,100,100],
    [1,0.97,0.095,0.9,0.85,0.75,0.65,0.5,0.3,0.1],
    
]
#---------------
_generacion = 0
_numpoblacion = 15
_maximas_generaciones = 5
##############################################


def poblacion_inicial():
    #print("Entre a poblacion_inicial().........")
    global _hiperparametros
    return ([
        _hiperparametros[0][randint(0,9)],
        _hiperparametros[1][randint(0,9)],
        _hiperparametros[2][randint(0,9)],
        _hiperparametros[3][randint(0,9)]
    ],0,{})

def poblacion(n):
    print("Entre a poblacion().........")
    pob = []
    for i in range(n):
        v = poblacion_inicial()
        pob.append(v)

    return pob

def get_fitness_poblacion(pob):
    # va a retornar una lista de tuplas con los hiperparametros y el fitenes
    listica = []
    for p in pob:
        print("INDIVIDUO::",p)
        print("HIPERPARAMETROS::",p[0])
        validacion,pesos = Entrenar_red(p)
        listica.append((p,validacion,pesos))
    return listica
def takeSecond(elem):
    #print("Entre a takeSecond().........")
    return elem[1]

def seleccionar(m_pob):

    print("seleccionar().........")
    return s_torneo(m_pob)


def s_torneo(m_pob):
    print("Entre a s_torneo().........")
    t = len(m_pob)

    if t < 16:
        return s_mejores(m_pob)

    limite = t // 4
    lim = limite
    i = 0
    selec = []

    while i < 4:
        x = 0
        v = []

        while x < lim:
            v.append(m_pob[x])

        x += 1
        lim += limite

        s = s_mejores(v)

        selec = selec + s

        if lim > t:
            break

    return selec

def s_mejores(m_pob):
    select = []
    print("Entre a s_mejores().........")
    v_calidad = get_fitness_poblacion(m_pob[0])
    #print("Vector de calidad:",v_calidad)
    #v_calidad = mejor_solucion(lfits)
    v_calidad.sort(reverse=False, key=takeSecond)
    #print("(2)Vector de calidad:",v_calidad)
    t = len(m_pob)
  
    m = t // 2
    for i in range(m):
        #act = v_calidad[i]
        #v = v_calidad[i]
        select.append(v_calidad[i])

    return select   


#EMPAREJAMIENTO ALEATORIO...
def emparejar(padres):
    print("Entre a emparejar().........")
    print("Padres: ",padres)
    global _numpoblacion
    hijos = []
    tampadres = len(padres)
    for i in range(_numpoblacion - tampadres):
        index1 = randint(0,tampadres-1)
        index2 = randint(0,tampadres-1)
        #print("alv: ",index1,index2)
        while(index1 == index2):
            
            index2 = randint(0,tampadres-1)

        h1 = cruzar(padres[index1], padres[index2])
        h1 = mutar(h1)
        hijos.append(h1)
        
    
    for hijo in hijos:
        padres.append(hijo)

    return padres

def cruzar(v1, v2):
    #print("Entre a cruzar().........")
    vn = []

    if random() > .5:
        vn.append(v1[0])
    else:
        vn.append(v2[0])

    if random() > .5:
        vn.append(v1[1])
    else:
        vn.append(v2[1])

    if random() > .5:
        vn.append(v1[2])
    else:
        vn.append(v2[2])
    
    if random() > .5:
        vn.append(v1[3])
    else:
        vn.append(v2[3])


    return vn

def mutar(hijo):
    print("Entre a mutar().........")
    print(hijo)
    pos = randint(0,3)
    valrand = 0
    if pos == 2:
        valrand = randint(0,9)
    else:
        valrand = uniform(0,9)
        valrand = round(valrand,4)
    hijo[pos] = valrand
    return hijo

def criterio(p0):
    print("Entre a criterio().........")
    global _generacion
    global _maximas_generaciones
    if _generacion <= _maximas_generaciones:
        return None
    return p0 

def Entrenar_red(p0):#return exactitud,pesos
    # Cargando conjunto de datos
    parametros = p0[0]
    print("*******************************************EN ENTRENAR RED***********************************************************")
    print("parametros::",parametros)
    train_X,val_X,test_X,train_Y,val_Y,test_Y = get_Dataset()
    global ONLY_SHOW
    if ONLY_SHOW:
        Plotter.plot_field_data(train_X, train_Y)
        # Plotter.plot_field_data(val_X, val_Y)
        print("Entradas de entrenamiento:", train_X.shape, sep=' ')
        print(train_X)
        print("Salidas de entrenamiento:", train_Y.shape, sep=' ')
        print(train_Y)
        print("Entradas de validacion:", val_X.shape, sep=' ')
        print(val_X)
        print("Salidas de validacion:", val_Y.shape, sep=' ')
        print(val_Y)
        exit()

    # Definir los conjuntos de datos
    print("!!!!!!!!!!!!!!!!!!!!!!CREACION DE DATOS!!!!!!!!!!!!!!!!!!!")
    train_set = Data(train_X, train_Y)
    #print("train_X.shape::",train_X.shape)
    #print("train_Y.shape::",train_Y.shape)
    #print(train_Y)
    val_set = Data(val_X, val_Y)
    #print("....")
    #print("val_X.shape()::",val_X.shape)
    #print("val_Y.shape()::",val_Y.shape)
    #print(val_Y)
    #print("....")
    test_set = Data(test_X, test_Y)
    #print("val_X.shape()::",test_X.shape)
    #print("val_Y.shape()::",test_Y.shape)
    #print(test_Y)

    print("!!!!!!!!!!!!!!!!!!!!!!CREACION DE DATOS!!!!!!!!!!!!!!!!!!!")
    # Se define las dimensiones de las capas
    capas1 = [train_set.n, 6,6,6,1]

    # Se define el modelo
    nn1 = NN_Model(train_set, capas1, alpha=parametros[0], iterations=parametros[2], lambd=parametros[1], keep_prob=parametros[3])
    #nn2 = NN_Model(train_set, capas1, alpha=0.3, iterations=50000, lambd=0.7, keep_prob=1)

    # Se entrena el modelo
    pesos = nn1.training(True)
    #Se guardan los pesos
    #print("-----------PESOS------------")
    #print(pesos)
    #print("------------PESOS----------")
    #nn2.training(True)

    # Se analiza el entrenamiento
    #Plotter.show_Model([nn1])
    #Plotter.show_Model([nn1, nn2])
    print('Entrenamiento Modelo 1')
    nn1.predict(train_set)
    print('Validacion Modelo 1')
    exactitud,y_hat =  nn1.predict(val_set)
    print('Pruebas Modelo 1')
    nn1.predict(test_set)
    return exactitud,pesos
def predecir(datos):#return y_hat
    # Cargando conjunto de datos
    train_X,val_X,test_X,train_Y,val_Y,test_Y = get_Dataset()
     # Definir los conjuntos de datos
    print("!!!!!!!!!!!!!!!!!!!!!!CREACION DE DATOS!!!!!!!!!!!!!!!!!!!")
    train_set = Data(train_X, train_Y)
    print("train_X.shape::",train_X.shape)
    print("train_Y.shape::",train_Y.shape)
    print(train_Y)
    val_set = Data(val_X, val_Y)
    print("....")
    print("val_X.shape()::",val_X.shape)
    print("val_Y.shape()::",val_Y.shape)
    print(val_Y)
    print("....")
    test_set = Data(test_X, test_Y)
    print("val_X.shape()::",test_X.shape)
    print("val_Y.shape()::",test_Y.shape)
    print(test_Y)

    print("!!!!!!!!!!!!!!!!!!!!!!CREACION DE DATOS!!!!!!!!!!!!!!!!!!!")
    #LEO EL JSON
    obj_text = codecs.open('temporales/pesos.json', 'r', encoding='utf-8').read()
    pesos = json.loads(obj_text)
    #lw1 = pesos['W1'].tolist()
    lw1 = np.array(pesos['W1'])
    lb1 = np.array(pesos['b1'])
    lw2 = np.array(pesos['W2'])
    lb2 = np.array(pesos['b2'])
    lw3 = np.array(pesos['W3'])
    lb3 = np.array(pesos['b3'])
    lw4 = np.array(pesos['W4'])
    lb4 = np.array(pesos['b4'])
    newpesos = {
        'W1':lw1,
        'b1':lb1,
        'W2':lw2,
        'b2':lb2,
        'W3':lw3,
        'b3':lb3,
        'W4':lw4,
        'b4':lb4,
    } 
    capas1 = [train_set.n, 6,6,6,1]   
    # Se define el modelo
    nn1 = NN_Model(None, capas1, alpha=0.3, iterations=1000, lambd=0, keep_prob=1,paras=newpesos,flag=ENTRENO)
    #nn2 = NN_Model(train_set, capas1, alpha=0.3, iterations=50000, lambd=0.7, keep_prob=1)

    print('Entrenamiento Modelo 1')
    nn1.predict(train_set)
    print('Validacion Modelo 1')
    nn1.predict(val_set)
    print('Pruebas Modelo 1')
    exactitud,y_hat = nn1.predict(test_set)
    return y_hat

def main():
    #df = get_Dataset()
    #print(df)
    print("Entre a main().........")
    global _generacion
    global _numpoblacion
    
    
    p0 = poblacion(_numpoblacion)
    print(p0)
    fin = criterio(p0)
    _generacion = 1
    while(fin == None):
        padres = seleccionar(p0)
        p0 = emparejar(padres)
        #print("Termino de emparejar")
        fin = criterio(p0)
        _generacion += 1

    print("!!!!!!!!!!!!!!!!!!!!!!!!!-------------RESULTADOS FINALES DEL GENETICO-------------!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(fin)
    print(_generacion)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@Procederia a guardar los parameros de::@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print(fin[0])
    '''
    lw1 = pesos['W1'].tolist()
    lb1 = pesos['b1'].tolist()
    lw2 = pesos['W2'].tolist()
    lb2 = pesos['b2'].tolist()
    lw3 = pesos['W3'].tolist()
    lb3 = pesos['b3'].tolist()
    lw4 = pesos['W4'].tolist()
    lb4 = pesos['b4'].tolist()
    newpesos = {
        'W1':lw1,
        'b1':lb1,
        'W2':lw2,
        'b2':lb2,
        'W3':lw3,
        'b3':lb3,
        'W4':lw4,
        'b4':lb4,
    } 
    #b = pesos.tolist() # nested lists with same data, indices
    file_path = "temporales/pesos.json" ## your path variable
    json.dump(newpesos, codecs.open(file_path, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4) ### this saves the array in .json format
    '''
    #escribir_en_bitacora(flag_finalizacion,flag_seleccion,file_name,_generacion,fin)
    return fin

if __name__ == "__main__":
    main()
