import numpy

def mapas_de_calor(numero):
    if numero == 1:
        pesos = [[-2, -1, 0, 0,	 0,	 0,	 0,	  1,   2],
                [-2, -1, 0, 0,	 0,	 0,	 0,	  1,   2],
                [-3, -2, 1, 0,	 0,	 0,	 1,	  2,   3],
                [-4, -3, 2, 1,	 0,	 1,	 2,	  3,   4],
                [-4, -3, 2, 1,	 0,	 1,	 2,	  3,   4],
                [ 4,  3, 2, 1,	-1,	-1,	-2,	 -3,  -4],
                [ 8,  6, 4, 2,	-2,	-2,	-4,	 -6,  -8],
                [12,  9, 6, 3,	-3,	-3,	-6,	 -9, -12],
                [16, 12, 8, 4,	-4,	-4,	-8,	-12, -16]]
    
    elif numero == 2:
        pesos = [[ 16,  12,  8,  4, 0, -4, -8, -12, -16,],
                [ 12,   9,  6,  3, 0, -3, -6,  -9, -12,],
                [  8,   6,  4,  2, 0, -2, -4,  -6,  -8,],
                [  4,   3,  2,  1, 0, -1, -2,  -3,  -4,],
                [  0,   0,  0,  0, 0,  0,  0,   0,   0,],
                [ -4,  -3, -2, -1, 0,  1,  2,   3,   4,],
                [ -8,  -6, -4, -2, 0,  2,  4,   6,   8,],
                [-12,  -9, -6, -3, 0,  3,  6,   9,  12,],
                [-16, -12, -8, -4, 0,  4,  8,  12,  16,]]
    
    elif numero == 3:
        pesos = [[-4, -3, -2, -1, 0, 1, 2, 3, 4],
                [-4, -3, -2, -1, 0, 1, 2, 3, 4],
                [-4, -3, -2, -1, 0, 1, 2, 3, 4],
                [-4, -3, -2, -1, 0, 1, 2, 3, 4],
                [-4, -3, -2, -1, 0, 1, 2, 3, 4],
                [-4, -3, -2, -1, 0, 1, 2, 3, 4],
                [-4, -3, -2, -1, 0, 1, 2, 3, 4],
                [-4, -3, -2, -1, 0, 1, 2, 3, 4],
                [-4, -3, -2, -1, 0, 1, 2, 3, 4]]
        
    else: 
        print('Não há mapa para o número fornecido')

    return pesos


def maximizacao(matriz, pesos): # Soma ponderada
    soma = 0
    somaesquerda = 0
    somadireita = 0

    pesos = numpy.array(pesos).reshape((9, 9))

    matrizesquerda = matriz[:, :4]
    matrizdireita  = matriz[:, 5:]

    pesosesquerda = pesos[:, :4]
    pesosdireita  = pesos[:, 5:]

    if len(matriz) != len(pesos) or len(matriz[0]) != len(pesos[0]):
        raise ValueError("As dimensões da matriz e dos pesos devem ser iguais.")
    
    else:
        for i in range(len(matriz)):
            for j in range(len(matriz[0])):
                soma += matriz[i][j] * pesos[i][j]

        for i in range(len(matrizesquerda)):
            for j in range(len(matrizesquerda[0])):
                somaesquerda += matrizesquerda[i][j] * pesosesquerda[i][j]
                
        for i in range(len(matrizdireita)):
            for j in range(len(matrizdireita[0])):
                somadireita += matrizdireita[i][j] * pesosdireita[i][j]

    return soma, somaesquerda, somadireita