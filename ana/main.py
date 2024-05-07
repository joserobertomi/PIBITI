import cv2
import time
from imagem import encontrar_linha, threshold_colorido, vetor_central, posicionar_mira, posicionar_mira_9x9
from direcionamento import maximizacao

captura = cv2.VideoCapture(0)
tamanho = 20 # Definir o tamanho dos segmentos da mira

while (1):
    ret, frame = captura.read()
    h, w, _ = frame.shape

    # Tratamento frame  P&B => Blur => Threshold
    _, frame = cv2.threshold(cv2.blur(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (10, 10)), 100, 255, cv2.THRESH_BINARY) 
    
    vetor_centro = vetor_central(frame, h, w)
    centro_mira = encontrar_linha(vetor_centro)

    framecolorido = threshold_colorido(frame)

    matriz = posicionar_mira_9x9(w // 2, h // 2, tamanho, frame, framecolorido)
    soma, somaesquerda, somadireita = maximizacao(matriz)
    
    framecolorido = cv2.putText(framecolorido, ('soma: ' + str(soma)),                 (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1, cv2.LINE_AA) 
    framecolorido = cv2.putText(framecolorido, ('somaesquerda: ' + str(somaesquerda)), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1, cv2.LINE_AA) 
    framecolorido = cv2.putText(framecolorido, ('somadireita: ' + str(somadireita)),   (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1, cv2.LINE_AA) 

    # Aumentar a janela de debug
    cv2.namedWindow('Visao', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Visao', framecolorido.shape[1] * 2, framecolorido.shape[0] * 2)
    cv2.imshow('Visao', framecolorido)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

captura.release()
cv2.destroyAllWindows()