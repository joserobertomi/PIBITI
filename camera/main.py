import numpy as np
import cv2 as cv
import time

def contar_pixels(area, total):
    brancos = np.sum(area == 255) * 100 // total
    pretos = np.sum(area == 0) * 100 // total
    return pretos, brancos

def capturar_video(cap, x, y, largura, altura, x2, y2):
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        retval, threshold = cv.threshold(gray, 50, 255, cv.THRESH_BINARY)

        total = largura * altura
        roi = threshold[y:y+altura, x:x+largura]
        roi2 = threshold[y2:y2+altura, x2:x2+largura]

        pretos, brancos = contar_pixels(roi, total)
        pretos2, brancos2 = contar_pixels(roi2, total)

        threshold = cv.rectangle(threshold, (x, y), (x+largura, y+altura), (255, 0, 255), 1) 
        threshold = cv.putText(threshold, ('P:' + str(pretos) + '% B:' + str(brancos) + "%"), (x, y + altura + 10), cv.FONT_HERSHEY_SIMPLEX , 0.3, (255, 0, 255), 1, cv.LINE_AA) 

        threshold = cv.rectangle(threshold, (x2, y2), (x2+largura, y2+altura), (255, 0, 255), 1) 
        threshold = cv.putText(threshold, ('P:' + str(pretos2) + '% B:' + str(brancos2) + "%"), (x2, y2 + altura + 10), cv.FONT_HERSHEY_SIMPLEX , 0.3, (255, 0, 255), 1, cv.LINE_AA) 

        cv.imshow('frame', threshold)
        if cv.waitKey(1) == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    cap = cv.VideoCapture(0)

    # Dimenções:
    width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))  
    print("Altura do video: " + str(height) + " Largura do video: " + str(width))

    # ROI - Área de interesse:
    largura, altura, margem = 50, 50, 50
    x, y =  margem, height//2
    x2, y2 =  width - largura - margem, height//2

    capturar_video(cap, x, y, largura, altura, x2, y2)