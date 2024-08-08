from LFR_Demo import script
from sys import exit
from time import time 
import cv2 as cv
import numpy as np
from time import sleep 

if __name__ == '__main__':

    demo = False
    if demo: 
        script([150,490])
        exit()
    move = False 

    from movimentacao import init_motores, frente, giro_antih, giro_h, parado
    from raspi_camera import init_camera, tirar_foto

    decorrido_segundos = [time()]
    print('Hello Pi 3!')
    cam_size=(640, 480) # define por padrao o tamanho da camera
    pontos = [150, 490]
    camera = init_camera(cam_size=cam_size) # inicia a camera pelo modulo do raspi
    pwm_esq, pwm_dir = init_motores()

    decorrido_segundos.append(time()-decorrido_segundos[-1])
    count = 0
    try: 
        while True:

            #Captura de imagem 
            parcial_segundos = [time()]
            img_path = tirar_foto(picam2=camera)
            gray_frame = cv.imread(img_path, cv.IMREAD_GRAYSCALE)            
            new_path ="/home/perry/project/images/gray-frame.png"
            cv.imwrite(new_path, gray_frame)
            parcial_segundos.append(time() - parcial_segundos[-1]) # Tirar foto e armazena
            
            # Tratamento do frame
            tempo = time()
            treated_frame = cv.blur(gray_frame, (10, 10))
            #_, treated_frame = cv.threshold(treated_frame, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
            _,treated_frame = cv.threshold(treated_frame,75,255,cv.THRESH_BINARY)
            treated_frame = cv.erode(treated_frame, None, iterations = 10)
            low_b = np.uint8([5])
            high_b = np.uint8([0])
            mask = cv.inRange(treated_frame, high_b, low_b)
            contours, hierarchy = cv.findContours(mask, 1, cv.CHAIN_APPROX_NONE)
            new_path = str("/home/perry/project/images/treated-frame" + str(count) + ".png")
            cv.imwrite(new_path, treated_frame)
            parcial_segundos.append(time() - tempo) # Tratar e contar a imagem
            
            if len(contours) > 0 :
                c = max(contours, key=cv.contourArea)
                M = cv.moments(c)
                if M["m00"] != 0 :
                    print(M)
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    print("CX : "+str(cx)+"  CY : "+str(cy))
                    if cx >= pontos[1] :
                        print("Horario")
                        if move:
                            giro_h(pwm_esq=pwm_esq, pot_esq=50, pwm_dir=pwm_dir, pot_dir=0)
                    if cx < pontos[1] and cx > pontos[0] :
                        print("On Track!")
                        if move: 
                            frente(pwm_esq=pwm_esq, pot_esq=50, pwm_dir=pwm_dir, pot_dir=50)
                    if cx <= pontos[0] :
                        print("Antihorario ")
                        if move : 
                            giro_antih(pwm_esq=pwm_esq, pot_esq=0, pwm_dir=pwm_dir, pot_dir=50)
                    cv.circle(treated_frame, (cx,cy), 5, (255,255,255), -1)
                    cv.imwrite(new_path, treated_frame)
            else :
                print("I don't see the line")
            sleep(0.1)
            parado(pwm_esq, pwm_dir)
            tempo = time()
            #pot_esq, pot_dir = decisao_de_movimento(base_esq=somaesquerda, base_dir=somadireita, pot_max=50, pot_min=40, soma_max=soma_max)
            #frente(pwm_esq=pwm_esq, pot_esq=pot_esq, pwm_dir=pwm_dir, pot_dir=pot_dir)
            parcial_segundos.append(time() - tempo) # Avalia a decisao e ajusta o motor 

            decorrido_segundos.append(parcial_segundos[1:])
    
    except KeyboardInterrupt:
        exit()
        print('--------- PARCIAIS DE TEMPO ---------')
        flag = input('o que printar')
        if (flag == 'n'):
            exit()
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

