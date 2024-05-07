from imagem import encontrar_linha, threshold_colorido
from direcionamento import vetor_central, posicionar_mira
from movimentacao import parar, frente
from raspi_camera import init_camera, take_photo
from aux_functions import print_aim_result, take_move_decision
import cv2 as cv

if __name__ == '__main__':

    print('Hello Pi 3!')
    cam_size=(640, 480) # define por padrao o tamanho da camera
    tamanho = 100 # Definir o tamanho dos segmentos da mira
    camera = init_camera(cam_size=cam_size) # inicia a camera pelo modulo do raspi
    
    c = 5

    while True:
        img_path = take_photo(picam2=camera)
        gray_frame = cv.imread(img_path, cv.IMREAD_GRAYSCALE)
        
        new_path ="/home/perry/project/images/gray-frame.png"
        cv.imwrite(new_path, gray_frame)
        
        # Tratamento frame  P&B => Blur => Threshold
        _, treated_frame = cv.threshold(cv.blur(gray_frame, (10, 10)), 100, 255, cv.THRESH_BINARY) 
        
        new_path ="/home/perry/project/images/treated-frame.png"
        cv.imwrite(new_path, treated_frame)
        
        vetor_centro = vetor_central(treated_frame, cam_size[1], cam_size[0])
        centro_mira = encontrar_linha(vetor_centro)

        aimmed_frame, aim_result = posicionar_mira(threshold_colorido(treated_frame), centro_mira, tamanho, cam_size[1])

        new_path ="/home/perry/project/images/aimmed-frame.png"
        cv.imwrite(new_path, aimmed_frame)
                
        #print_aim_result(aim_result)
        
        pot_e, pot_d = take_move_decision(aim_result, 80)
        print(f'Potencia Esq: {pot_e} | Potencia Dir: {pot_d}')
        frente(0.2,pot_e, pot_d)
        parar(1)
        
        c-=1 
        if not c: 
            break
        
        
    print('Done, arrombado!')
        
        
           