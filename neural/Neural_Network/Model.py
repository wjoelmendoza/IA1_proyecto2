import numpy as np


class NN_Model:

    def __init__(self, train_set, layers, alpha=0.3, iterations=30000, lambd=0, keep_prob=1,paras=None,flag=True):
        self.data = train_set
        self.alpha = alpha
        self.max_iteration = iterations
        self.lambd = lambd
        self.kp = keep_prob
        # Se inicializan los pesos
        if flag ==True:
            self.parametros = self.Inicializar(layers)
        else:
            self.parametros = paras


    def Inicializar(self, layers):
        parametros = {}
        L = len(layers)
        for l in range(1, L):
            parametros['W'+str(l)] = np.random.randn(layers[l], layers[l-1]) / np.sqrt(layers[l-1])
            parametros['b'+str(l)] = np.zeros((layers[l], 1))
        return parametros

    def training(self, show_cost=False):
        self.bitacora = []
        for i in range(0, self.max_iteration):
            y_hat, temp = self.propagacion_adelante(self.data)
            cost = self.cost_function(y_hat)
            gradientes = self.propagacion_atras(temp)
            self.actualizar_parametros(gradientes)
            if i % 50 == 0:
                self.bitacora.append(cost)
                if show_cost:
                    print('Iteracion No.', i, 'Costo:', cost, sep=' ')
        return self.parametros


    def propagacion_adelante(self, dataSet):
        # Se extraen las entradas
        X = dataSet.x

        # Extraemos los pesos
        W1 = self.parametros["W1"]
        b1 = self.parametros["b1"]
        W2 = self.parametros["W2"]
        b2 = self.parametros["b2"]
        W3 = self.parametros["W3"]
        b3 = self.parametros["b3"]
        W4 = self.parametros["W4"]
        b4 = self.parametros["b4"]

        # ------ Primera capa
        Z1 = np.dot(W1, X) + b1
        A1 = self.activation_function('relu', Z1)

        D1 = np.random.rand(A1.shape[0], A1.shape[1])
        D1 = (D1 < self.kp).astype(int)
        A1 *= D1
        A1 /= self.kp

        # ------ Segunda capa
        Z2 = np.dot(W2, A1) + b2
        A2 = self.activation_function('relu', Z2)

        D2 = np.random.rand(A2.shape[0], A1.shape[1])
        D2 = (D2 < self.kp).astype(int)
        A2 *= D2
        A2 /= self.kp

        # ------ Tercera capa
        Z3 = np.dot(W3, A2) + b3
        A3 = self.activation_function('relu', Z3)

        D3 = np.random.rand(A3.shape[0], A2.shape[1])
        D3 = (D3 < self.kp).astype(int)
        A3 *= D3
        A3 /= self.kp


        # ------ Cuarta capa
        Z4 = np.dot(W4, A3) + b4
        A4 = self.activation_function('sigmoide', Z4)

        temp = (Z1, A1, D1, Z2, A2, D2, Z3, A3,D3,Z4,A4)
        return A4, temp

    def propagacion_atras(self, temp):
        # Se obtienen los datos
        m = self.data.m
        Y = self.data.y
        X = self.data.x
        W1 = self.parametros["W1"]
        W2 = self.parametros["W2"]
        W3 = self.parametros["W3"]
        W4 = self.parametros["W4"]
        (Z1, A1, D1, Z2, A2, D2, Z3, A3,D3,Z4,A4) = temp

        # Derivadas parciales de la cuarta capa
        dZ4 = A4 - Y
        dW4 = (1 / m) * np.dot(dZ4, A3.T) + (self.lambd / m) * W4
        db4 = (1 / m) * np.sum(dZ4, axis=1, keepdims=True)

        # Derivadas parciales de la tercera capa
        dA3 = np.dot(W4.T, dZ4)
        dA3 *= D3
        dA3 /= self.kp
        dZ3 = np.multiply(dA3, np.int64(A3 > 0))
        dW3 = 1. / m * np.dot(dZ3, A2.T) + (self.lambd / m) * W3
        db3 = 1. / m * np.sum(dZ3, axis=1, keepdims=True)


        # Derivadas parciales de la segunda capa
        dA2 = np.dot(W3.T, dZ3)
        dA2 *= D2
        dA2 /= self.kp
        dZ2 = np.multiply(dA2, np.int64(A2 > 0))
        dW2 = 1. / m * np.dot(dZ2, A1.T) + (self.lambd / m) * W2
        db2 = 1. / m * np.sum(dZ2, axis=1, keepdims=True)

        # Derivadas parciales de la primera capa
        dA1 = np.dot(W2.T, dZ2)
        dA1 *= D1
        dA1 /= self.kp
        dZ1 = np.multiply(dA1, np.int64(A1 > 0))
        dW1 = 1./m * np.dot(dZ1, X.T) + (self.lambd / m) * W1
        db1 = 1./m * np.sum(dZ1, axis=1, keepdims = True)

        gradientes = {"dZ4": dZ4, "dW4": dW4, "db4": db4,
                     "dA3": dA3, "dZ3": dZ3, "dW3": dW3, "db3": db3,
                     "dA2": dA2, "dZ2": dZ2, "dW2": dW2, "db2": db2,
                     "dA1": dA1, "dZ1": dZ1, "dW1": dW1, "db1": db1}

        return gradientes

    def actualizar_parametros(self, grad):
        # Se obtiene la cantidad de pesos
        L = len(self.parametros) // 2
        for k in range(L):
            self.parametros["W" + str(k + 1)] -= self.alpha * grad["dW" + str(k + 1)]
            self.parametros["b" + str(k + 1)] -= self.alpha * grad["db" + str(k + 1)]

    def cost_function(self, y_hat):
        # Se obtienen los datos
        Y = self.data.y
        m = self.data.m
       
        # Se hacen los calculos
        temp = np.multiply(-np.log(y_hat), Y) + np.multiply(-np.log(1 - y_hat), 1 - Y)
        result = (1 / m) * np.nansum(temp)
        # Se agrega la regularizacion L2
        if self.lambd > 0:
            L = len(self.parametros) // 2
            suma = 0
            for i in range(L):
                suma += np.sum(np.square(self.parametros["W" + str(i + 1)]))
            result += (self.lambd/(2*m)) * suma
        return result

    def predict(self, dataSet):
        # Se obtienen los datos
        m = dataSet.m
        Y = dataSet.y
        p = np.zeros((1, m), dtype= np.int)
        # Propagacion hacia adelante
        y_hat, temp = self.propagacion_adelante(dataSet)
        # Convertir probabilidad
        for i in range(0, m):
            p[0, i] = 1 if y_hat[0, i] > 0.5 else 0
        exactitud = np.mean((p[0, :] == Y[0, ]))
        print("Exactitud: " + str(exactitud))
        return exactitud,y_hat


    def activation_function(self, name, x):
        result = 0
        if name == 'sigmoide':
            result = 1/(1 + np.exp(-x))
        elif name == 'tanh':
            result = np.tanh(x)
        elif name == 'relu':
            result = np.maximum(0, x)
        return result