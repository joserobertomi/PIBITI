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
