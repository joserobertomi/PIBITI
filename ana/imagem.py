import numpy
import cv2

def encontrar_linha(vetor): # Recebe os pixels na linha central do vídeo e retorna a coordenada do centro da linha
    inicio = -1
    final = -1
    maior_intervalo = 0
    inicio_atual = -1
    intervalo_atual = 0

    for i, num in enumerate(vetor):
        if num == 0:
            if inicio_atual == -1:
                inicio_atual = i
            intervalo_atual += 1
        else:
            if intervalo_atual > maior_intervalo:
                maior_intervalo = intervalo_atual
                inicio = inicio_atual
                final = i - 1
            inicio_atual = -1
            intervalo_atual = 0

    if intervalo_atual > maior_intervalo:
        inicio = inicio_atual
        final = len(vetor) - 1

    centro_mira = (int(final - inicio) //2 ) + inicio

    return centro_mira

def threshold_colorido(frame):
    canal_extra = numpy.where(frame == 255, 255, 0).astype(numpy.uint8)
    frame = cv2.merge((frame, canal_extra, canal_extra))
    return frame

def vetor_central(frame, h, w): # Retona um vetor com o valor das cores na linha central do video
    vetor = []

    for item in range(w):
        pixel = frame[(h // 2), item]
        vetor.append(pixel)

    vetor = numpy.array(vetor)
    return vetor

def posicionar_mira(frame, centro_mira, tamanho, h): # Mira 3x3
    area = tamanho * tamanho
    x, y = (centro_mira - tamanho + tamanho // 2), (h // 2 - tamanho + tamanho // 2)
    quadrados = tamanho // 3
    rois = [[x                  , y, quadrados],
            [x + quadrados      , y, quadrados],
            [x + quadrados * 2  , y, quadrados],
                
            [x                  , y + quadrados, quadrados],
            [x + quadrados      , y + quadrados, quadrados],
            [x + quadrados * 2  , y + quadrados, quadrados],
                
            [x                  , y + quadrados * 2, quadrados],
            [x + quadrados      , y + quadrados * 2, quadrados],
            [x + quadrados * 2  , y + quadrados * 2, quadrados]]
    
    rgb_quadrados = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    for index, roi in enumerate(rois, start = 0): 
        x, y, largura = roi[0], roi[1], roi[2]
        roi = frame[y:y+quadrados, x:x+quadrados]
        pb = numpy.sum(roi == 0)
        if pb <= area * 0.15:
            pb = 0
        else:
            pb = 1
        rgb_quadrados[index] = pb
        frame = cv2.putText(frame, str(pb), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1, cv2.LINE_AA) 
        frame = cv2.rectangle(frame, (x, y), (x + largura, y + largura), (255, 0, 255), 2) 
    return frame

def posicionar_mira_9x9(centro_x, centro_y, tamanho_roi, imagem, framecolorido): # Mira 9x9 
    area = tamanho_roi * tamanho_roi
    rgb_quadrados = []
    for i in range(-4, 5): 
        linha = []  
        for j in range(-4, 5):
            x1, y1 = centro_x + i * tamanho_roi, centro_y + j * tamanho_roi
            x2, y2 = x1 + tamanho_roi, y1 + tamanho_roi
            
            roi = imagem[y1:y2, x1:x2]
            pb = numpy.sum(roi == 0)
            if pb <= area * 0.15:
                pb = 0
            else:
                pb = 1
            linha.append(pb) 

            framecolorido = cv2.putText(framecolorido, str(pb), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1, cv2.LINE_AA) 
            framecolorido = cv2.rectangle(framecolorido, (x1, y1), (x2, y2), (255, 0, 255), 2) 
        rgb_quadrados.append(linha)  

    rgb_quadrados = numpy.array(rgb_quadrados).reshape((9, 9))
    return rgb_quadrados
