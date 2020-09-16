import numpy as np
import matplotlib.pyplot as plt

def mallado(nnod, nelem, nod_x_elem, L, T0, T_L):

    coorx = np.linspace(0,L, nnod)
    conectividad = np.zeros((nelem, nod_x_elem))

    for i in range(conectividad.shape[0]):
        conectividad[i, 0] = i * (nod_x_elem - 1) + 1
        conectividad[i, 1] = (i + 1) * (nod_x_elem - 1) + 1
        conectividad[i, 2:] = np.arange(conectividad[i, 0] + 1, conectividad[i, 1])

    conectividad = conectividad.astype(int)

    valor_temp_fija = [0]*(nnod+1)
    valor_temp_fija[0], valor_temp_fija[-1] = T0, T_L
    temp_fija = np.arange(1, nnod+1)
    return coorx, conectividad, temp_fija, valor_temp_fija


# KU = f + Q


if __name__ == '__main__':

    ndim = 1
    nod_x_elem = 5 # 3; # 4; # 5;
    nelementos = 6  # 5; # 6;
    nnodos = (nod_x_elem - 1) * nelementos + 1
    L = 4.0
    H_k = 8.0
    T0 = 50.0
    T_L = 10.0

    temperatura = np.zeros((nnodos))

    coorx, conectividad, temp_fija, valor_temp_fija = mallado(nnodos, nelementos, nod_x_elem, L, T0, T_L)

    for i in range(nnodos):
        if (temp_fija[i] == 1):
            temperatura[i] = valor_temp_fija[i]
        else:
                temperatura[i] = (H_k / 2.0) * coorx[i] * (L - coorx[i]) - ((T0 - T_L) / L) * \
                                 coorx[i] + T0

    for i in range(nelementos):
        print('Elemento {}: {}'.format(i, conectividad[i]))
    print('Temperaturas en los nodos: \n{}'.format(temperatura))

    fig, ax = plt.subplots()
    ax.plot(coorx, temperatura, '-o')

    plt.show()



