from imagem import encontrar_linha, threshold_colorido, vetor_central, posicionar_mira_9x9
from direcionamento import maximizacao, mapas_de_calor
from movimentacao import parar, frente
from raspi_camera import init_camera, take_photo
from aux_functions import take_move_decision2
import cv2 as cv
import numpy as np
    

if __name__ == '__main__':

    print('Hello Pi 3!')
    cam_size=(640, 480) # define por padrao o tamanho da camera
    tamanho = 20 # Definir o tamanho dos segmentos da mira
    camera = init_camera(cam_size=cam_size) # inicia a camera pelo modulo do raspi
    
    c = 5
    
    pesos = mapas_de_calor(1)
    pesos_uni = np.transpose(pesos)
    pesos_uni = pesos_uni.flatten()

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
        
        framecolorido = threshold_colorido(treated_frame)
        aim_result = np.transpose(posicionar_mira_9x9(cam_size[0]//2, cam_size[1]//2, tamanho, treated_frame, framecolorido))
        soma, somaesquerda, somadireita = maximizacao(aim_result, pesos_uni)
        treated_frame = threshold_colorido(treated_frame)
    
        finalimage = cv.addWeighted(framecolorido, 0.5, treated_frame, 0.5, 0)
    
        finalimage = cv.putText(finalimage, ('soma: ' + str(soma)),                 (20,  40), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv.LINE_AA) 
        finalimage = cv.putText(finalimage, ('somaesquerda: ' + str(somaesquerda)), (20,  80), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv.LINE_AA) 
        finalimage = cv.putText(finalimage, ('somadireita: ' + str(somadireita)),   (20, 120), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv.LINE_AA) 

        new_path ="/home/perry/project/images/aimmed-frame.png"
        cv.imwrite(new_path, finalimage)
                
        #print_aim_result(aim_result)
        print("aq ok")
        print(aim_result)
        print(f"soma esq = {somaesquerda}\nsoma dir = {somadireita}")
        
        pot_e, pot_d = take_move_decision2(base_esq=somaesquerda, base_dir=somadireita, pot_max=80)
        print(f'Potencia Esq: {pot_e} | Potencia Dir: {pot_d}')
        frente(0.2,pot_e, pot_d)
        parar(1)
        
        #c-=1 
        #if not c: 
        #    break
            
        #break
        
        
    print('Done, arrombado!')
        
        
           