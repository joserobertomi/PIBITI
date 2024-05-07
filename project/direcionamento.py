import numpy
import cv2

def vetor_central(frame, h, w): # Retona um vetor com o valor das cores na linha central do video
    vetor = []

    for item in range(w):
        pixel = frame[(h // 2), item]
        vetor.append(pixel)

    vetor = numpy.array(vetor)
    return vetor

def posicionar_mira(frame, centro_mira, tamanho, h):
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
    return frame, rgb_quadrados