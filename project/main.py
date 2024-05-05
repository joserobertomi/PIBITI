from time import time, sleep
from imagem import encontrar_linha, threshold_colorido
from direcionamento import vetor_central, posicionar_mira
from movimentacao import parar, frente
from raspi_camera import init_camera, take_photo

cam_size=(640, 480)
tamanho = tamanho = 100 # Definir o tamanho dos segmentos da mira


if __name__ == '__main__':

    cam_size=(640, 480)
    altura_roi = 20
    largura_roi= 20
    dist_linha=10

    camera = init_camera(cam_size=cam_size)
    time1 = time()
    
    img_path = take_photo(picam2=camera)
    time2 = time()    
    
    lim_roi = define_roi(altura_roi, largura_roi, dist_linha, img_path)
        
    while True:
                
        print('eh o loop cowboy')
        
        squareL, squareR = apply_threshold_and_count(img_path, altura_roi, largura_roi, dist_linha, lim_roi)
        time3 = time()
    
        if squareL[0] > 0.80 and squareR[0] > 0.80: # se branco maior que 80%  
            # frente(tempo, pote, potd)
            print('frente!')
            frente(0.8, 40, 40)
        elif squareL[0] < 0.25 and squareR[0] < 0.25: # se branco menor que 25% nos dois blocos
            print('parado!')
            parar(0.8)
        elif squareL[0] < 0.50 :
            print('vira p esquerda!')
            frente(0.8, 0, 40)
        elif squareR[0] < 0.50:
            print('vira p direita!')
            frente(0.8, 40, 0)
        else:
            print('nao to entendendo!')
            frente(0.8, 40, 40)
        
        img_path = take_photo(picam2=camera)
        
        print_square_info(squareR, squareL)
        #print_time_spent(times=[time0, time1, time2, time3])
        
        
           