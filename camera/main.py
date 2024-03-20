# from picamera2 import Picamera2
import numpy as np
import cv2 as cv
import time

def init_camera(cam_size):
    # Captura a imagem da camera e salva em um arquivo tipo jpg
    picam2 = Picamera2()
    camera_config = picam2.create_still_configuration(main={"size": (cam_size)}, lores={"size": (cam_size)}, display="lores")
    picam2.configure(camera_config)
    return picam2

def take_photo(picam2):
    # Captura a imagem da camera e salva em um arquivo tipo jpg
    picam2.start()
    path = "/home/perry/temp/project/photos/frame.jpg"
    picam2.capture_file(path)
    return path
    
def count_pixels(image, largura, altura, margem):
    
    height = int(image.shape[0])
    width = int(image.shape[1])
    
    # ROI - Área de interesse:
    x, y =  margem, height//2
    x2, y2 =  width - largura - margem, height//2
    
    total = largura * altura
    roi = image[y:y+altura, x:x+largura]
    roi2 = image[y2:y2+altura, x2:x2+largura]
    #square1 = (--------------white--------------,--------------black--------------)
    squareR = (np.sum(roi == 255) * 100 // total, np.sum(roi == 0) * 100 // total)
    squareL = (np.sum(roi2 == 255) * 100 // total, np.sum(roi2 == 0) * 100 // total)
    
    return squareR, squareL

def apply_threshold_and_count(img_path, largura, altura, margem):
    # Opencv le a imagem jpg em escala de cinza salva no raspberry 
    frame = cv.imread(img_path, cv.IMREAD_GRAYSCALE)
    result, threshold = cv.threshold(frame, 50, 255, cv.THRESH_BINARY)
    if result:
        
        squareR, squareL = count_pixels(threshold, largura, altura, margem)
        
        # Pode ser removido 
        new_path ="/home/perry/temp/project/photos/filtered.png"
        cv.imwrite(new_path, threshold)
        # ateh aqui
        
        return squareR, squareL, new_path
    
    return False, False, False

def print_square_info(squareR, squareL):
    print('SquareR: Brancos:', squareR[0], '| Pretos:', squareR[1])
    print('SquareL: Brancos:', squareL[0], '| Pretos:', squareL[1])
    
def print_time_spent(times):
    for t in range(len(times)-1):
        print(f'tempo[{t}+1] - tempo[{t}] = {times[t+1]-times[t]}')
    print(f'Total time spent = {times[len(times)-1]-times[0]}')

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

if __name__ == '__main__':
    original = cv.imread('./image.png', cv.IMREAD_GRAYSCALE)
    result, threshold = cv.threshold(original, 50, 255, cv.THRESH_BINARY)
    
    h, w = threshold.shape

    y = h//2
    
    alt_roi = int(20) # setavel 
    largura_roi = int(20) # setavel 
    dist_da_linha = int(10) # setavel 
    half_alt_roi = int(alt_roi/2)
    half_largura_roi = int(largura_roi/2)
    total = alt_roi * w
    
    roi = np.round(np.sum(threshold[y-half_alt_roi:y+half_alt_roi, :], axis=0) / (alt_roi * 255))
    count = (np.sum(roi == 1) , np.sum(roi == 0))
    
    margem_esq, margem_dir = index_maior_sequencia_zeros(roi)
    margem_esq -= half_largura_roi
    margem_dir += half_largura_roi
    
    final = cv.rectangle(original, (margem_esq-largura_roi,y-dist_da_linha), (margem_esq, y+dist_da_linha), (0, 0, 0), 1)
    final = cv.rectangle(original, (margem_dir+largura_roi,y-dist_da_linha), (margem_dir, y+dist_da_linha), (0, 0, 0), 1)
    
    cv.imshow('Image-captured', original)
    key = cv.waitKey()
    cv.destroyAllWindows()
    
    print(roi)
    print(count)
    