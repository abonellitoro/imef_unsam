
import numpy as np

def mallador(nnod, nelem, nod_x_elem, L, T0, T_L):

    ndim = 1
    coorx = np.zeros((nnod))
    conect = np.zeros((nelem, nod_x_elem), dtype=int)
    temp_fija = np.zeros((nnod), dtype=int)
    valor_temp_fija = np.zeros((nnod))

    
    for i in range(nnod):
        coorx[i] = (L/(nnod-1))*i

    for i in range(nelem):
        conect[i][0] = (nod_x_elem-1)*i
        conect[i][1] = (nod_x_elem-1)*(i+1)
        for j in range(nod_x_elem-2):
            conect[i][j+2] = conect[i][0]+j+1

    temp_fija[0] = 1
    temp_fija[nnod-1] = 1

    valor_temp_fija[0] = T0
    valor_temp_fija[nnod-1] = T_L

    return coorx, conect, temp_fija, valor_temp_fija





    
