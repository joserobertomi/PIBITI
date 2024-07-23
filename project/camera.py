import cv2
import numpy as np
import math
from skimage.transform import (hough_line, hough_line_peaks)

def localizaPontos(frame, largura, altura):
    # breakpoint()
    posicaoPixelsBrancos = np.where(frame == 255)
    # 'inicio' é o início da reta no topo da imagem
    # 'fim' é o fim da reta na parte inferior da imagem
    inicioReta_Esq = [posicaoPixelsBrancos[0][0], posicaoPixelsBrancos[1][0]] # [coordenada na vertical, coordenada na horizontal]
    inicioReta_Dir = [posicaoPixelsBrancos[0][1], posicaoPixelsBrancos[1][1]] # [coordenada na vertical, coordenada na horizontal]
    fimReta_Esq =    [posicaoPixelsBrancos[0][-2], posicaoPixelsBrancos[1][-2]] # [coordenada na vertical, coordenada na horizontal]
    fimReta_Dir =    [posicaoPixelsBrancos[0][-1], posicaoPixelsBrancos[1][-1]] # [coordenada na vertical, coordenada na horizontal]
    inicioReta_Meio = [inicioReta_Esq[0], inicioReta_Esq[1] + (inicioReta_Dir[1] - inicioReta_Esq[1])/2] # [coordenada na vertical, coordenada na horizontal]
    fimReta_Meio = [fimReta_Esq[0], fimReta_Esq[1] + (fimReta_Dir[1] - fimReta_Esq[1])/2] # [coordenada na vertical, coordenada na horizontal]
    return [inicioReta_Esq, inicioReta_Meio, inicioReta_Dir], [fimReta_Esq, fimReta_Meio, fimReta_Dir]

def calculaAnguloReta(frame):
    # Perform Hough Transformation to detect lines
    hspace, angles, distances = hough_line(frame)
    
    # Find angle
    angle=[]
    for _, a , distances in zip(*hough_line_peaks(hspace, angles, distances)):
        angle.append(a)
    
    # Obtain angle for each line
    angles = [a*180/np.pi for a in angle]
    return angles

vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
while(True):
    ret, frame = vid.read()
    assert frame is not None, "a imagem nao pode ser obtida" ##VERIFICA SE A IMAGEM PODE SER CAPTURADA --> tirar_foto()

    # Converte para escala de cinza
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # converte para escala de cinza --> gray_frame = cv.imread(img_path, cv.IMREAD_GRAYSCALE)

    # Pré-processa a imagem (blur, erosão, limiarização)
    frame = cv2.blur(frame, (10, 10)) # Aplica um blur na imagem --> _, treated_frame = cv.threshold(cv.blur(gray_frame, (10, 10)), 100, 255, cv.THRESH_BINARY)
    frame = cv2.erode(frame, None, iterations = 10) #aplica 10 iteracoes de erosao 

    # frame = cv2.adaptiveThreshold(frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    _, frame = cv2.threshold(frame, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) # aplica limiarizacao binaria e o algoritmo de otsu 
    frame_altura, frame_largura = frame.shape

    # Aplica detecção de borda
    frame2 = cv2.Canny(image = frame, threshold1 = 100, threshold2 = 200) # NOVO PASSO --> deteccao de borda 
    
    # Detecta o início e o fim da reta na imagem, além de calcular o ponto médio do início e do fim da reta
    inicioReta, fimReta = localizaPontos(frame2, frame_largura, frame_altura) # NOVO PASSO --> define as posicoes em X e Y dos pontos de interesse 
    
    # NOVO PASSO: Desenha "na mao" uma imagem onde tem apenas uma reta no meio da faixa vista pela câmera
    frame3 = np.zeros((frame_altura, frame_largura), np.uint8)
    inicioReta_Meio = tuple(np.round(inicioReta[1]).astype(np.uint8))
    fimReta_Meio =   tuple(np.round(fimReta[1]).astype(np.uint8))
    frame3 = cv2.line(frame3, inicioReta_Meio, fimReta_Meio, (255, 255, 255), 5)
    
    # Calcula a inclinação da reta
    angulos2 = calculaAnguloReta(frame2) # nessa imagem nao vao ter multiplos angulos? conferir a imagem que mandei para a ana 
    angulos3 = calculaAnguloReta(frame3) # talvez calcular o angulo na mao seria mais barato em termos computacionais? 

    frame_colorido = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB) #transforma a imagem de duas diemnsoes em 3 para poder exibir informacoes

    frame_colorido2 = cv2.cvtColor(frame2, cv2.COLOR_GRAY2RGB) #EXIBE INFO
    frame_colorido2 = cv2.putText(frame_colorido2, ('angulos2: ' + "{:.2f}".format(angulos2[0])),           (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA) #EXIBE INFO

    frame_colorido3 = cv2.cvtColor(frame3, cv2.COLOR_GRAY2RGB) #EXIBE INFO
    frame_colorido3 = cv2.putText(frame_colorido3, ('angulos3: ' + "{:.2f}".format(angulos3[0])),  (20,  40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA) #EXIBE INFO
    frame_colorido3 = cv2.putText(frame_colorido3, ('inicioReta_Meio: ' + str(inicioReta[1])),     (20,  80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA) #EXIBE INFO
    frame_colorido3 = cv2.putText(frame_colorido3, ('fimReta_Meio: ' + str(fimReta[1])),           (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA) #EXIBE INFO
    
    cv2.namedWindow('frame_colorido', cv2.WINDOW_NORMAL)
    cv2.imshow('frame_colorido', frame_colorido)
    cv2.resizeWindow('frame_colorido', 640, 480)

    cv2.namedWindow('frame_colorido2', cv2.WINDOW_NORMAL)
    cv2.imshow('frame_colorido2', frame_colorido2)
    cv2.resizeWindow('frame_colorido2', 640, 480)

    cv2.namedWindow('frame_colorido3', cv2.WINDOW_NORMAL)
    cv2.imshow('frame_colorido3', frame_colorido3)
    cv2.resizeWindow('frame_colorido3', 640, 480)

    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
cv2.destroyAllWindows()
vid.release()
