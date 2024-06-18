import numpy
import cv2

def encontrar_linha(vetor): 
    # Recebe os pixels na linha central do vídeo e retorna a coordenada do centro da linha
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
    # Adiciona um 3° canal pra possibilitar cores
    canal_extra = numpy.where(frame == 255, 255, 0).astype(numpy.uint8)
    frame = cv2.merge((frame, canal_extra, canal_extra))
    return frame

def vetor_central(frame, h, w): 
    # Retona um vetor com o valor das cores na linha central do video
    vetor = []

    for item in range(w):
        pixel = frame[(h // 2), item]
        vetor.append(pixel)

    vetor = numpy.array(vetor)
    return vetor

def busca_cores(numero):
    # Define uma cor para cada valor no mapa de calor
    bgr = ()
    cores_array = [( 0, (108, 108, 255)),
             ( 1, (116, 140, 255)),
             ( 2, (125, 171, 255)),
             ( 3, (133, 203, 255)),
             ( 4, (153, 233, 255)),
             ( 6, (234, 221, 213)),
             ( 8, (244, 185, 172)),
             ( 9, (254, 167, 131)),
             (12, (255, 148, 90)),
             (16, (255, 181, 118))]
    
    for cor in cores_array:
        if cor[0] == abs(numero):
            bgr = cor[1]
    return bgr

def posicionar_mira_9x9(centro_x, centro_y, tamanho_roi, imagem, framecolorido, pesos): 
    # Posiciona mira 9x9 no centro da imagem 
    index = 0
    area = tamanho_roi * tamanho_roi
    rgb_quadrados = []

    for i in range(-4, 5): 
        linha = []  
        for j in range(-4, 5):
            x1, y1 = centro_x + i * tamanho_roi, centro_y + j * tamanho_roi
            x2, y2 = x1 + tamanho_roi, y1 + tamanho_roi
            
            roi = imagem[y1:y2, x1:x2]
            pb = numpy.sum(roi == 0)
            if pb <= area * 0.5:
                pb = 0
            else:
                pb = 1
            linha.append(pb) 

            # cor_array = busca_cores(pesos[index])
            index = index + 1

            #framecolorido = cv2.rectangle(framecolorido, (x1, y1), (x2, y2), cor_array, -1)
            framecolorido = cv2.putText(framecolorido, str(pb), (x1 + 5, y1 + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA) 

            if pb == 1:
                framecolorido = cv2.rectangle(framecolorido, (x1, y1), (x2, y2), (0, 0, 0), 2) 
            else:
                framecolorido = cv2.rectangle(framecolorido, (x1, y1), (x2, y2), (255, 0, 255), 1) 

        rgb_quadrados.append(linha)  

    rgb_quadrados = numpy.array(rgb_quadrados).reshape((9, 9))
    return rgb_quadrados