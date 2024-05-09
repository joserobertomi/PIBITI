import cv2
import numpy
from imagem import encontrar_linha, threshold_colorido, vetor_central, posicionar_mira_9x9
from direcionamento import maximizacao, mapas_de_calor

# captura = cv2.VideoCapture('pista.mp4') # Adicionar video pré gravado
captura = cv2.VideoCapture(0) # Video da câmera
tamanho = 30 # Definir o tamanho dos segmentos da mira

pesos = mapas_de_calor(1)

pesos_uni = numpy.transpose(pesos)
pesos_uni = pesos_uni.flatten()

while (1):
    ret, frame = captura.read()
    h, w, _ = frame.shape

    # Tratamento frame  P&B => Blur => Threshold
    _, frame = cv2.threshold(cv2.blur(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (10, 10)), 100, 255, cv2.THRESH_BINARY) 
    
    framethres = threshold_colorido(frame)
    framethres = framethres

    vetor_centro = vetor_central(frame, h, w)
    centro_mira = encontrar_linha(vetor_centro)

    framecolorido = threshold_colorido(frame)
    matriz = posicionar_mira_9x9(w // 2, h // 2, tamanho, frame, framecolorido, pesos_uni)

    soma, somaesquerda, somadireita = maximizacao(matriz, pesos)
    finalimage = cv2.addWeighted(framecolorido, 0.5, framethres, 0.5, 0)

    finalimage = cv2.putText(finalimage, ('soma: ' + str(soma)),                 (20,  40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv2.LINE_AA) 
    finalimage = cv2.putText(finalimage, ('somaesquerda: ' + str(somaesquerda)), (20,  80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv2.LINE_AA) 
    finalimage = cv2.putText(finalimage, ('somadireita: ' + str(somadireita)),   (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv2.LINE_AA) 

    # Aumentar a janela de debug
    cv2.namedWindow('Visao', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Visao', finalimage.shape[1] // 2, finalimage.shape[0] // 2)
    cv2.imshow('Visao', finalimage)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

captura.release()
cv2.destroyAllWindows()