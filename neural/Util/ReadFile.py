import scipy.io

def get_dataFile():
    print("------------------GET-DATAFILE---------------")
    data = scipy.io.loadmat('datasets/data.mat')
    print(data)
    train_X = data['X'].T
    train_Y = data['y'].T
    val_X = data['Xval'].T
    val_Y = data['yval'].T
    return train_X, train_Y, val_X, val_Y
