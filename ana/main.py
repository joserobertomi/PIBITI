import cv2
from imagem import encontrar_linha, threshold_colorido
from direcionamento import vetor_central, posicionar_mira

captura = cv2.VideoCapture(0)
tamanho = 100 # Definir o tamanho dos segmentos da mira

while (1):
    ret, frame = captura.read()
    h, w, _ = frame.shape

    # Tratamento frame  P&B => Blur => Threshold
    _, frame = cv2.threshold(cv2.blur(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (10, 10)), 100, 255, cv2.THRESH_BINARY) 
    
    vetor_centro = vetor_central(frame, h, w)
    centro_mira = encontrar_linha(vetor_centro)

    frame = threshold_colorido(frame)
    frame = posicionar_mira(frame, centro_mira, tamanho, h)

    # Aumentar a janela de debug
    cv2.namedWindow('Visao', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Visao', frame.shape[1] * 2, frame.shape[0] * 2)
    cv2.imshow('Visao', frame)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

captura.release()
cv2.destroyAllWindows()