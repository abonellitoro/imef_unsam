import numpy as np
from mallado import mallador


def arma_sistema_sparse(ndim, nnod, nelem, nod_x_el, conect):
    naux = nnod
    ad = np.zeros((naux))
    ia = np.zeros((naux + 1), dtype=int)  # nº de números nulos acumlados por fila
    icx = np.zeros((naux), dtype=int)

    # calculo la cantidad de valores no nulos
    nonull = nod_x_el ** 2 * nelem - (nelem - 1) - nnodos
    an = np.zeros((nonull + 1))

    # calculo la cantidad de valores no nulos
    nonull = nod_x_el ** 2 * nelem - (nelem - 1) - nnodos

    nodes = np.unique(conect)
    print(conect)
    ia[0] = 1
    idxs = []
    rows = []
    ja = []
    for node in nodes:
        # print('Nodo: ', node)
        result = np.where(conect == node)
        row = result[0]
        col = result[1]
        idx = list(zip(row, col))

        icx[node] = len(idx)
        rows.append(row)
        idxs.append(idx)

        # En esta línea obtengo con qué nodos está conectado el nodo que estoy analizando y saco los repetidos
        aux = np.unique(conect[rows[node]])
        # print(result)

        # En esta linea le saco el nodo que estoy estudiando ya que no es de interés y después ordeno los vecinos
        neighbor_nodes = np.sort(np.delete(aux, np.where(aux == node)))
        ja.append(neighbor_nodes.tolist())

    # Me quedó expresado en forma de listas de listas, lo "aplano"
    ja = [item for sublist in ja for item in sublist]
    icx_aux = np.insert(icx, 0, 1)
    ia = np.cumsum(icx_aux)

    return ad, an, ia, ja, icx


def arma_matriz_completa(ad, an, ia, ja, icx, ndim, nnod):
    k = np.zeros((nnod, nnod))

    for n in range(nnod):
        k[n, n] = ad[n]
        aux_ia = ia - 1
        ja_values = ja[aux_ia[n]:aux_ia[n + 1]]
        an_values = an[aux_ia[n]: aux_ia[n + 1]]
        k[n, ja_values] = an_values

    return k


if __name__ == '__main__':

    ndim = 1
    nod_x_elem = 2
    nelementos = 4
    nnodos = (nod_x_elem - 1) * nelementos + 1
    L = 4.0
    H_k = 8.0
    T0 = 50.0
    T_L = 10.0

    coorx, conectividad, temp_fija, valor_temp_fija = mallador(nnodos, nelementos, nod_x_elem, L, T0, T_L)

    ad, an, ia, ja, icx = arma_sistema_sparse(ndim, nnodos, nelementos, nod_x_elem, conectividad)

    # VALORES DE EJEMPLO
    ad[0] = 1
    ad[1:nnodos - 1] = 2
    ad[nnodos - 1] = 1

    an[:-1] = -1

    # Matriz K como deberia ser, para referencia del resultado del ejercicio
    # SOLO PARA ELEMENTOS DE 2 NODOS
    k_aux = np.zeros((nnodos, nnodos))
    k_aux[0][0] = 1
    k_aux[0][1] = -1
    k_aux[nnodos - 1][nnodos - 2] = -1
    k_aux[nnodos - 1][nnodos - 1] = 1
    for i in range(nnodos - 2):
        k_aux[i + 1][i] = -1
        k_aux[i + 1][i + 1] = 2
        k_aux[i + 1][i + 2] = -1

    k = arma_matriz_completa(ad, an, ia, ja, icx, ndim, nnodos)

    print('Cantidad de nodos: \n{}'.format(nnodos))
    print('Dimension de la diagonal: \n{}'.format(len(ad)))

    print('\nCantidad de no nulos(+1): \n{}'.format(ia[-1]))
    print('Dimension de los valores no nulos fuera de la diagonal: \n{}'.format(len(an)))

    print('\nColumnas de no nulos: \n{}'.format(ja))
    print('Cantidad de no nulos por fila: \n{}'.format(icx))

    print('\nMatriz de rigidez teórica K: \n{}'.format(k_aux))

    print('\nMatriz de rigidez armada K: \n{}'.format(k))

    # print('\nIA: \n{}'.format(ia))
    # print('\nAN: \n{}'.format(an))
