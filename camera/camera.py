import numpy as np
import cv2 as cv

def index_maior_sequencia_zeros(lista):
    maior_sequencia = 0
    indice_inicio = -1
    indice_fim = -1
    sequencia_atual = 0
    indice_atual = -1

    for i, num in enumerate(lista):
        if num == 0:
            if sequencia_atual == 0:
                indice_atual = i
            sequencia_atual += 1
        else:
            if sequencia_atual > maior_sequencia:
                maior_sequencia = sequencia_atual
                indice_inicio = indice_atual
                indice_fim = i - 1
            sequencia_atual = 0

    if sequencia_atual > maior_sequencia:
        maior_sequencia = sequencia_atual
        indice_inicio = indice_atual
        indice_fim = len(lista) - 1

    return indice_inicio, indice_fim

def define_roi(alt_roi, lar_roi, dist_linha, imagem): 

    h, w = imagem.shape

    y = h//2

    alt_roi = int(alt_roi) # setavel 
    lar_roi = int(lar_roi) # setavel 
    dist_linha = int(dist_linha) # setavel 
    half_alt_roi = int(alt_roi/2)
    half_lar_roi = int(lar_roi/2)
    total_roi = lar_roi*alt_roi

    roi_line = np.round(np.sum(imagem[y-half_alt_roi:y+half_alt_roi, :], axis=0) / (alt_roi * 255))
    count_full_line = (np.sum(roi_line == 1) , np.sum(roi_line == 0))

    margem_esq, margem_dir = index_maior_sequencia_zeros(roi_line)
    margem_esq -= dist_linha
    margem_dir += dist_linha

    # REMOVABLE
    cv.rectangle(original, (margem_esq-lar_roi,y-half_alt_roi), (margem_esq, y+half_alt_roi), (0, 0, 0), 1)
    cv.rectangle(original, (margem_dir+lar_roi,y-half_alt_roi), (margem_dir, y+half_alt_roi), (0, 0, 0), 1)
    # REMOVABLE
    
    # JUMP OF CAT
    roi_esq = imagem[margem_esq-lar_roi:margem_esq, y-half_alt_roi:y+half_alt_roi] / 255
    roi_dir = imagem[margem_dir:margem_dir+lar_roi, y-half_alt_roi:y+half_alt_roi] / 255
    count_roi_esq = (np.sum(roi_esq == 1) , np.sum(roi_esq == 0))
    count_roi_dir = (np.sum(roi_dir == 1) , np.sum(roi_dir == 0))
    #count_roi_esq = (((np.sum(roi_esq == 1)/total_roi) , (np.sum(roi_esq == 0)/total_roi)))
    #count_roi_dir = (((np.sum(roi_dir == 1)/total_roi) , (np.sum(roi_dir == 0)/total_roi)))
    # JUMP OF CAT

    cv.imshow('Image-captured', original)
    cv.waitKey()
    cv.destroyAllWindows()

    print(roi_line)
    print(count_full_line)
    print(roi_dir)
    print(roi_esq)
    
    return count_roi_esq, count_roi_dir


original = cv.imread('./image.png', cv.IMREAD_GRAYSCALE)
result, threshold = cv.threshold(original, 50, 255, cv.THRESH_BINARY)
count_roi_esq, count_roi_dir = define_roi(20, 20, 5, threshold)
print(count_roi_esq, count_roi_dir)
