from imagem import encontrar_linha, threshold_colorido, vetor_central, posicionar_mira_9x9
from direcionamento import maximizacao, mapas_de_calor
from movimentacao import init_motores, frente, decisao_de_movimento
from raspi_camera import init_camera, tirar_foto
from time import time 
import cv2 as cv
import numpy as np

if __name__ == '__main__':

    decorrido_segundos = [time()]

    print('Hello Pi 3!')
    cam_size=(640, 480) # define por padrao o tamanho da camera
    tamanho = 30 # Definir o tamanho dos segmentos da mira
    camera = init_camera(cam_size=cam_size) # inicia a camera pelo modulo do raspi
    
    ###
    pwm_esq, pwm_dir = init_motores()
    ###

    c = 5

    pesos, soma_max = mapas_de_calor(3)
    pesos_uni = np.array(pesos)
    pesos_uni = pesos_uni.flatten()
    pesos_color = pesos_uni.transpose

    decorrido_segundos.append(time()-decorrido_segundos[-1])
    try: 
        while True:
            parcial_segundos = [time()]
            img_path = tirar_foto(picam2=camera)
            gray_frame = cv.imread(img_path, cv.IMREAD_GRAYSCALE)            
            new_path ="/home/perry/project/images/gray-frame.png"
            cv.imwrite(new_path, gray_frame)
            parcial_segundos.append(time() - parcial_segundos[-1]) # Tirar foto e armazena
            
            tempo = time()
            # Tratamento frame  P&B => Blur => Threshold
            _, treated_frame = cv.threshold(cv.blur(gray_frame, (10, 10)), 100, 255, cv.THRESH_BINARY) 
            framethres = threshold_colorido(treated_frame)
            framethres = framethres
            new_path ="/home/perry/project/images/treated-frame.png"
            cv.imwrite(new_path, treated_frame)
            vetor_centro = vetor_central(treated_frame, cam_size[1], cam_size[0])
            centro_mira = encontrar_linha(vetor_centro)
            framecolorido = threshold_colorido(treated_frame)
            aim_result = np.transpose(posicionar_mira_9x9(cam_size[0]//2, cam_size[1]//2+(tamanho*2), tamanho, treated_frame, framecolorido, pesos_color))
            soma, somaesquerda, somadireita = maximizacao(aim_result, pesos_uni)
            finalimage = cv.addWeighted(framecolorido, 0.5, framethres, 0.5, 0)
            finalimage = cv.putText(finalimage, ('soma: ' + str(soma)),                 (20,  40), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv.LINE_AA) 
            finalimage = cv.putText(finalimage, ('somaesquerda: ' + str(somaesquerda)), (20,  80), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv.LINE_AA) 
            finalimage = cv.putText(finalimage, ('somadireita: ' + str(somadireita)),   (20, 120), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv.LINE_AA) 
            new_path ="/home/perry/project/images/aimmed-frame.png"
            cv.imwrite(new_path, finalimage)
            print(aim_result)
            print(f"soma esq = {somaesquerda}\nsoma dir = {somadireita}")
            parcial_segundos.append(time() - tempo) # Tratar e contar a imagem
            
            tempo = time()
            pot_esq, pot_dir = decisao_de_movimento(base_esq=somaesquerda, base_dir=somadireita, pot_max=50, pot_min=40, soma_max=soma_max)
            frente(pwm_esq=pwm_esq, pot_esq=pot_esq, pwm_dir=pwm_dir, pot_dir=pot_dir)
            parcial_segundos.append(time() - tempo) # Avalia a decisao e ajusta o motor 

            decorrido_segundos.append(parcial_segundos[1:])
    except KeyboardInterrupt:
        print('--------- PARCIAIS DE TEMPO ---------')
        decorrido_segundos.pop(0) 
        print(f'Tempo para inicilizar as paradas = {decorrido_segundos[0]}')
        i = 0
        for iteracao in decorrido_segundos[1:]:
            print(f'----> Itercao: {i}')
            print(f'Tirar foto e armazenar: {iteracao[0]}')
            print(f'Tratar e contar a imagem: {iteracao[1]}')
            print(f'Avalia a decisao e ajusta o motor : {iteracao[2]}')
            print(f'Tempo total da iteracao: {np.sum(iteracao)}')
            i+=1

