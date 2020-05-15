import datetime
import pandas as pd
from math import radians, cos, sin, asin, sqrt
from numpy import genfromtxt
import codecs, json


def load_file1():
    return pd.read_csv(
        'temporales/Dataset.csv',
        dtype= {'Estado':'object','Genero':'object','Edad':'int64','Anio':'int64','cod_depto':'int64','cod_muni':'int64','nombre':'object','municipio':'object'}
        )
def load_file2():
    return pd.read_csv(
        'temporales/Municipios.csv',
        dtype= {'Depto':'int64','Muni':'int64','lat':'float64','lon':'float64'}
        )

def generar_json_deps_mun():
    departamentos = {}
    datos1 = load_file1()
    for index, row in datos1.iterrows():
        cod_depto = row['cod_depto']
        nombre =  row['nombre']
        cod_muni = row['cod_muni']
        muni = row['municipio']
        if  cod_depto in departamentos:
            ##ya esta
            dep = departamentos[cod_depto]
            lmunis = dep['munis']
            if cod_muni in lmunis:
                pass
            else:
                #NO ESTA EL MUNICIPIO
                lmunis[cod_muni] = {'nombre':muni}
        else:
            lmunis = {}
            lmunis[cod_muni] = {'nombre':muni}
            departamentos[cod_depto] = {'nombre':nombre,'munis':lmunis}

    return departamentos

def make_client_Dataset(genero,edad,anio,dep,mun):
    print("----------MAKE_CLIENT_DATASET--------------------")
    #TENGO QUE TRATAR LOS DATOS!!!!
    #HABRO LOS MINIMOS Y MAXIMOS.....
    obj_text = codecs.open('temporales/escalamiento.json', 'r', encoding='utf-8').read()
    datos = json.loads(obj_text)
    #######---distancia
    distancia = 0
    datos2 = load_file2()
    for index2,row2 in datos2.iterrows():
        if dep == row2['Depto'] and mun == row2['Muni']:
            lat2 = row2['Lat']
            lat3 = row2['Lon']
            distancia = haversine(14.589246,-90.551449,lat2,lat3)
            break
    realdist = (distancia - datos['mindist']) /(datos['maxdist']-datos['mindist'] )
            
    #---------------
    #####--------anio
    realanio = (anio-datos['minanio'])/(datos['maxanio']-datos['minanio'])
    ###--------------------
    ####---------edad
    realedad = (edad - datos['minedad'])/(datos['maxedad']- datos['minedad'])
    ##------------
    data = list(zip([0],[realdist],[genero],[realedad],[realanio])) 
    cols = ['Estado','Distancia','Genero','Edad','Anio']
    df = pd.DataFrame(data,columns=cols)
    Y = df['Estado']
    X = df[['Distancia','Genero','Edad','Anio']]
    train_X = X.to_numpy()
    train_Y = Y.to_numpy()
    return train_X.T,train_Y.T
    
def get_Dataset():
    df =  pd.read_csv(
        'temporales/mydata.csv',
        dtype= {'Distancia':'float64','Estado':'int64','Genero':'int64','Edad':'float64','Anio':'float64'}
        )
    Y = df['Estado']
    X = df[['Distancia','Genero','Edad','Anio']]
    train_X = X[0:5309].to_numpy()
    val_X = X[5309:6826].to_numpy()
    test_X = X[6826:7584].to_numpy()
    train_Y = Y[0:5309].to_numpy()
    val_Y = Y[5309:6826].to_numpy()
    test_Y = Y[6826:7584].to_numpy()
    #print("@@@@@@@@@@@@@@@@@@@@@@@@@@  X  @@@@@@@@@@@@@@@@@@@@@@@@")
    #print(X)
    #print(X.T)
    #print("@@@@@@@@@@@@@@@@@@@@@@@@@@  Y  @@@@@@@@@@@@@@@@@@@@@@@@")
    #print(Y)
    #print(Y.T)
    

    return train_X.T,val_X.T,test_X.T,train_Y.T,val_Y.T,test_Y.T
        
    #return genfromtxt('temporales/mydata.csv', delimiter=',')


    
def tratamiento_de_datos():
    datos1 = load_file1()
    datos2 = load_file2()
    #Calculo de la distancia:
    distancia = []
    for index, row in datos1.iterrows():
        for index2,row2 in datos2.iterrows():
            if row['cod_depto'] == row2['Depto'] and row['cod_muni'] == row2['Muni']:
                lat2 = row2['Lat']
                lat3 = row2['Lon']
                distancia.append(haversine(14.589246,-90.551449,lat2,lat3))
                break

    #print(datos1)
    #print(datos2)
    #df = pd.DataFrame(distancia,columns=['Distancia'])
    datos1['Distancia2'] = distancia
    #df['c1'].apply(lambda x: 0 if x == 'MASCULINO' else 1)
    
    #SE HACE EL ESCALAMIENTO
    minedad = datos1['Edad'].min()
    maxedad = datos1['Edad'].max()
    factoredad = maxedad - minedad
    minanio = datos1['Anio'].min()
    maxanio = datos1['Anio'].max()
    factoranio = maxanio - minanio
    mindist = datos1['Distancia2'].min()
    maxdist = datos1['Distancia2'].max()
    factordist = maxdist - mindist
    #--Se guardan los minimos y maximos para el escalonamiento de los valores ingresados por la pagina----------------------------------------------------------
    dict = {
        'minedad':minedad.item(),
        'maxedad':maxedad.item(),
        'minanio':minanio.item(),
        'maxanio':maxanio.item(),
        'mindist':mindist.item(),
        'maxdist':maxdist.item()
    }
    file_path = "temporales/escalamiento.json" ## your path variable
    json.dump(dict, codecs.open(file_path, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4) ### this saves the array in .json format
    
    #---------------
    listdist = []
    listedad = []
    listanio = []
    for index, row in datos1.iterrows():
       #print(index,row)
        
        listdist.append((row['Distancia2'] - mindist) / factordist)
        listedad.append((row['Edad']-minedad)/factoredad)
        listanio.append((row['Anio']- minanio)/factoranio)   
    df = pd.DataFrame(list(zip(listdist,listedad,listanio)),columns=['Distancia','Edad','Anio'])
    
    #df['Edad'] = datos1['edad']
    #df['Anio'] = datos1['Anio']
    #df = pd.DataFrame(datos1['Genero'].apply(lambda x: 0 if x == 'MASCULINO' else 1),columns=['Estado'])
    df['Genero'] = datos1['Genero'].apply(lambda x: 0 if x == 'MASCULINO' else 1)
    df['Estado'] = datos1['Estado'].apply(lambda x: 0 if x == 'Traslado' else 1)
    
    print(df)
    df.to_csv('temporales/mydata.csv')

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r


def get_fitness(file,ls):
    #print("Entre a get_fitness().........")
    df = load_file(file)
    #print(df.head())
    #print(df.index)
    #print(df.sum())#SUMA POR COLUMNA
    #print(df.cumsum())#suma acumulada
    df['M1'] = df['P1']* ls[0]
    df['M2'] = df['P2']* ls[1]
    df['M3'] = df['P3']* ls[2]
    df['NC'] = df['M1']+ df['M2'] + df['M3'] 
    df['E'] = (df['NF'] - df['NC'])**2

    #print(df.head())
    #print(df.shape[0])
    fit = df['E'].sum()/df.shape[0]
    fit = round(fit,2)
    #print('FITNES CALCULADO::',fit)
    return fit




def escribir_en_bitacora(flagcriterio,seleccion,file,generaciones,solucion):
    
    print("Entre a escribir_en_bitacora().........")
    f = open("bitacora.txt", "a")
    tiempo = datetime.datetime.now()
    strfinalizacion = 'Maximo numero de Generaciones-- '+str(flagcriterio) if flagcriterio == '1' else 'default'
    strfinalizacion = 'El mejor fitness de la poblacion-- '+str(flagcriterio) if flagcriterio == '2' else strfinalizacion
    strfinalizacion = 'El fitness promedio de la poblacion-- '+str(flagcriterio) if flagcriterio == '3' else strfinalizacion 
    
    strseleccion = 'Torneos, escojiendo el de mejor fitness' if seleccion == '1' else 'default'
    strseleccion = 'Los mejores padres(mejor fitness)' if seleccion == '2' else strseleccion
    strseleccion = 'Aleatorios' if seleccion == '3' else strseleccion
    contenido = [
        
        'Fecha de ejecución: '+tiempo.date().isoformat()+'\n',
        'Hora de ejecución: '+tiempo.time().isoformat()+'\n',
        
        'Nombre del documento de datos utilizado: ',file+'\n',
        'Criterio de finalización utilizado: ',strfinalizacion+'\n',
        'Método de selección: ',strseleccion,'\n',
        'No. Generaciones: ',str(generaciones)+'\n',
        'Mejor solucion: ',str(solucion)+'\n',
        '------------------------------\n',
        ] 
    f.writelines(contenido)
    f.close()    
def misuma(uno,dos):
    return uno + dos
if __name__ == "__main__":
        #tratamiento_de_datos()
        x,y = get_Dataset()
        
        #print(x)
        #print(x.shape)
        #print(y)
        #print(y.shape)
        #distancia = []
        #df = pd.DataFrame([{'c1':'MASCULINO', 'c2':100}, {'c1':'FEMENINO','c2':110}, {'c1':'MASCULINO','c2':120}])
        #resp = df['c1'].apply(lambda x: 0 if x == 'MASCULINO' else 1)
        #print(resp)
        '''
        for index, row in df.iterrows():
            distancia.append(misuma(row['c1'],row['c2']))
        df['suma'] = pd.array(distancia)
        print(df)
        '''

        
    