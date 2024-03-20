from time import time, sleep
global time0 
time0 = time()
import RPi.GPIO as gpio
import getch
from picamera2 import Picamera2
import numpy as np
import cv2 as cv


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

def define_roi(alt_roi, lar_roi, dist_linha, imagem): 

    h, w = imagem.shape

    y = h//2

    alt_roi = int(alt_roi) # setavel 
    lar_roi = int(lar_roi) # setavel 
    dist_linha = int(dist_linha) # setavel 
    half_alt_roi = int(alt_roi/2)
    half_lar_roi = int(lar_roi/2)
    total_roi = lar_roi*alt_roi

    roi_line = np.round(np.sum(imagem[y-half_alt_roi:y+half_alt_roi, :], axis=0) / (alt_roi * 255))
    count_full_line = (np.sum(roi_line == 1) , np.sum(roi_line == 0))

    margem_esq, margem_dir = index_maior_sequencia_zeros(roi_line)
    margem_esq -= dist_linha
    margem_dir += dist_linha

    # REMOVABLE
    cv.rectangle(imagem, (margem_esq-lar_roi,y-half_alt_roi), (margem_esq, y+half_alt_roi), (0, 0, 0), 1)
    cv.rectangle(imagem, (margem_dir+lar_roi,y-half_alt_roi), (margem_dir, y+half_alt_roi), (0, 0, 0), 1)
    # REMOVABLE
    
    # JUMP OF CAT
    roi_esq = imagem[margem_esq-lar_roi:margem_esq, y-half_alt_roi:y+half_alt_roi] / 255
    roi_dir = imagem[margem_dir:margem_dir+lar_roi, y-half_alt_roi:y+half_alt_roi] / 255
    count_roi_esq = (np.sum(roi_esq == 1) , np.sum(roi_esq == 0))
    count_roi_dir = (np.sum(roi_dir == 1) , np.sum(roi_dir == 0))
    #count_roi_esq = (((np.sum(roi_esq == 1)/total_roi) , (np.sum(roi_esq == 0)/total_roi)))
    #count_roi_dir = (((np.sum(roi_dir == 1)/total_roi) , (np.sum(roi_dir == 0)/total_roi)))
    # JUMP OF CAT

    cv.imshow('Image-captured', imagem)
    cv.waitKey()
    cv.destroyAllWindows()

    print(roi_line)
    print(count_full_line)
    print(roi_dir)
    print(roi_esq)
    
    return count_roi_esq, count_roi_dir


def init(pot_esq, pot_dir):    
    
    gpio.setmode(gpio.BOARD)
    
    gpio.setup(11, gpio.OUT, initial=gpio.LOW) # controle motor esquerdo
    gpio.setup(13, gpio.OUT, initial=gpio.LOW) # controle motor esquerdo
    
    gpio.setup(16, gpio.OUT, initial=gpio.LOW) # controle motor esquerdo
    gpio.setup(18, gpio.OUT, initial=gpio.LOW) # controle motor esquerdo
    
    gpio.setup(33, gpio.OUT) # pwm motor esquerdo
    gpio.setup(35, gpio.OUT) # pwm motor direito 
    
    # To create a PWM instance: p = GPIO.PWM(channel, frequency)
    pwm_esq = gpio.PWM(33, 100)
    pwm_dir = gpio.PWM(35, 100)
    
    # To start a pwm: p.start(dc)   
    # Where dc is the duty cycle (0.0 <= dc <= 100.0)
    pwm_esq.start(pot_esq)
    pwm_dir.start(pot_dir)
    
    return pwm_esq, pwm_dir


def parar(sec):
    gpio.setmode(gpio.BOARD)
    
    gpio.setup(11, gpio.OUT) # controle motor esquerdo
    gpio.setup(13, gpio.OUT) # controle motor esquerdo
    
    gpio.setup(16, gpio.OUT) # controle motor esquerdo
    gpio.setup(18, gpio.OUT) # controle motor esquerdo
    
    gpio.setup(33, gpio.OUT) # pwm motor esquerdo
    gpio.setup(35, gpio.OUT) # pwm motor direito 
    
    # To create a PWM instance: p = GPIO.PWM(channel, frequency)
    pwm_esq = gpio.PWM(33, 1000)
    pwm_dir = gpio.PWM(35, 1000)
    
    # To start a pwm: p.start(dc)   
    # Where dc is the duty cycle (0.0 <= dc <= 100.0)
    pwm_esq.start(0)
    pwm_dir.start(0)
    
    gpio.output(11, gpio.LOW)
    gpio.output(13, gpio.LOW)
    gpio.output(16, gpio.LOW)
    gpio.output(18, gpio.LOW)
    
    sleep(sec)
    
    pwm_esq.stop()
    pwm_dir.stop()

    gpio.cleanup()


def frente(sec, pot_esq, pot_dir): 
        
    gpio.setmode(gpio.BOARD)
    
    gpio.setup(11, gpio.OUT) # controle motor esquerdo
    gpio.setup(13, gpio.OUT) # controle motor esquerdo
    
    gpio.setup(16, gpio.OUT) # controle motor esquerdo
    gpio.setup(18, gpio.OUT) # controle motor esquerdo
    
    gpio.setup(33, gpio.OUT) # pwm motor esquerdo
    gpio.setup(35, gpio.OUT) # pwm motor direito 
    
    # To create a PWM instance: p = GPIO.PWM(channel, frequency)
    pwm_esq = gpio.PWM(33, 1000)
    pwm_dir = gpio.PWM(35, 1000)
    
    # To start a pwm: p.start(dc)   
    # Where dc is the duty cycle (0.0 <= dc <= 100.0)
    pwm_esq.start(pot_esq)
    pwm_dir.start(pot_dir)
    
    gpio.output(11, gpio.HIGH)
    gpio.output(13, gpio.LOW)
    gpio.output(16, gpio.LOW)
    gpio.output(18, gpio.HIGH)
    
    sleep(sec)
    
    pwm_esq.stop()
    pwm_dir.stop()

    gpio.cleanup()


def re(sec, pot_esq, pot_dir): 
    
    gpio.setmode(gpio.BOARD)
    
    gpio.setup(11, gpio.OUT) # controle motor esquerdo
    gpio.setup(13, gpio.OUT) # controle motor esquerdo
    
    gpio.setup(16, gpio.OUT) # controle motor esquerdo
    gpio.setup(18, gpio.OUT) # controle motor esquerdo
    
    gpio.setup(33, gpio.OUT) # pwm motor esquerdo
    gpio.setup(35, gpio.OUT) # pwm motor direito 
    
    # To create a PWM instance: p = GPIO.PWM(channel, frequency)
    pwm_esq = gpio.PWM(33, 1000)
    pwm_dir = gpio.PWM(35, 1000)
    
    # To start a pwm: p.start(dc)   
    # Where dc is the duty cycle (0.0 <= dc <= 100.0)
    pwm_esq.start(pot_esq)
    pwm_dir.start(pot_dir)
    
    gpio.output(11, gpio.LOW)
    gpio.output(13, gpio.HIGH)
    gpio.output(16, gpio.HIGH)
    gpio.output(18, gpio.LOW)
    
    sleep(sec)
    
    pwm_esq.stop()
    pwm_dir.stop()

    gpio.cleanup()


def giro_antih(sec, pot_esq, pot_dir): 
    
    gpio.setmode(gpio.BOARD)
    
    gpio.setup(11, gpio.OUT) # controle motor esquerdo
    gpio.setup(13, gpio.OUT) # controle motor esquerdo
    
    gpio.setup(16, gpio.OUT) # controle motor esquerdo
    gpio.setup(18, gpio.OUT) # controle motor esquerdo
    
    gpio.setup(33, gpio.OUT) # pwm motor esquerdo
    gpio.setup(35, gpio.OUT) # pwm motor direito 
    
    # To create a PWM instance: p = GPIO.PWM(channel, frequency)
    pwm_esq = gpio.PWM(33, 1000)
    pwm_dir = gpio.PWM(35, 1000)
    
    # To start a pwm: p.start(dc)   
    # Where dc is the duty cycle (0.0 <= dc <= 100.0)
    pwm_esq.start(pot_esq)
    pwm_dir.start(pot_dir)
    
    gpio.output(11, gpio.HIGH)
    gpio.output(13, gpio.LOW)
    gpio.output(16, gpio.HIGH)
    gpio.output(18, gpio.LOW)
    
    sleep(sec)
    
    pwm_esq.stop()
    pwm_dir.stop()

    gpio.cleanup()

    
def giro_h(sec, pot_esq, pot_dir): 
    gpio.setmode(gpio.BOARD)
    
    gpio.setup(11, gpio.OUT) # controle motor esquerdo
    gpio.setup(13, gpio.OUT) # controle motor esquerdo
    
    gpio.setup(16, gpio.OUT) # controle motor esquerdo
    gpio.setup(18, gpio.OUT) # controle motor esquerdo
    
    gpio.setup(33, gpio.OUT) # pwm motor esquerdo
    gpio.setup(35, gpio.OUT) # pwm motor direito 
    
    # To create a PWM instance: p = GPIO.PWM(channel, frequency)
    pwm_esq = gpio.PWM(33, 1000)
    pwm_dir = gpio.PWM(35, 1000)
    
    # To start a pwm: p.start(dc)   
    # Where dc is the duty cycle (0.0 <= dc <= 100.0)
    pwm_esq.start(pot_esq)
    pwm_dir.start(pot_dir)
    
    gpio.output(11, gpio.LOW)
    gpio.output(13, gpio.HIGH)
    gpio.output(16, gpio.LOW)
    gpio.output(18, gpio.HIGH)
    
    sleep(sec)
    
    pwm_esq.stop()
    pwm_dir.stop()

    gpio.cleanup()

    
def parab_esquerda(sec, pot_esq, pot_dir): # OKOK
    gpio.setmode(gpio.BOARD)
    
    gpio.setup(11, gpio.OUT) # controle motor esquerdo
    gpio.setup(13, gpio.OUT) # controle motor esquerdo
    
    gpio.setup(16, gpio.OUT) # controle motor esquerdo
    gpio.setup(18, gpio.OUT) # controle motor esquerdo
    
    gpio.setup(33, gpio.OUT) # pwm motor esquerdo
    gpio.setup(35, gpio.OUT) # pwm motor direito 
    
    # To create a PWM instance: p = GPIO.PWM(channel, frequency)
    pwm_esq = gpio.PWM(33, 1000)
    pwm_dir = gpio.PWM(35, 1000)
    
    # To start a pwm: p.start(dc)   
    # Where dc is the duty cycle (0.0 <= dc <= 100.0)
    pwm_esq.start(pot_esq)
    pwm_dir.start(pot_dir)
    
    gpio.output(11, gpio.HIGH)
    gpio.output(13, gpio.LOW)
    gpio.output(16, gpio.LOW)
    gpio.output(18, gpio.LOW)
    
    sleep(sec)
    
    pwm_esq.stop()
    pwm_dir.stop()

    gpio.cleanup()

    
def parab_direita(sec, pot_esq, pot_dir): 
    gpio.setmode(gpio.BOARD)
    
    gpio.setup(11, gpio.OUT) # controle motor esquerdo
    gpio.setup(13, gpio.OUT) # controle motor esquerdo
    
    gpio.setup(16, gpio.OUT) # controle motor esquerdo
    gpio.setup(18, gpio.OUT) # controle motor esquerdo
    
    gpio.setup(33, gpio.OUT) # pwm motor esquerdo
    gpio.setup(35, gpio.OUT) # pwm motor direito 
    
    # To create a PWM instance: p = GPIO.PWM(channel, frequency)
    pwm_esq = gpio.PWM(33, 1000)
    pwm_dir = gpio.PWM(35, 1000)
    
    # To start a pwm: p.start(dc)   
    # Where dc is the duty cycle (0.0 <= dc <= 100.0)
    pwm_esq.start(pot_esq)
    pwm_dir.start(pot_dir)
    
    gpio.output(11, gpio.LOW)
    gpio.output(13, gpio.LOW)
    gpio.output(16, gpio.LOW)
    gpio.output(18, gpio.HIGH)
    
    sleep(sec)
    
    pwm_esq.stop()
    pwm_dir.stop()

    gpio.cleanup()

            
def controle_pelo_computador():    
    seconds = 0.1
    parar(seconds)
    a = get_single_char()
    c = 0
    while a != 'x' :
        c+=1
        
        if c >=2:
            c = 0
            parar(0)
            a = get_single_char()
        
        if a is not None: 
            if a == "w":
                print("Frente")
                frente(seconds, 100, 100)
                #time.sleep(seconds+2)
            elif a == "s":
                print("Re")
                re(seconds, 100, 100)
                #time.sleep(seconds+2)
            elif a == "d":    
                print("Giro horario")
                giro_h(seconds, 33, 33)
                #time.sleep(seconds+2)
            elif a == "a":
                print("Giro anti-horario")
                giro_antih(seconds, 33, 33)
                #time.sleep(seconds+2)
            elif a == "q":    
                print("Parabola esquerda")
                parab_esquerda(seconds, 33, 33)
            elif a == "e":   
                print("Parabola direita")
                parab_direita(seconds, 33, 33)

    print("Precionou 'x', saindo do modo de controle")

def get_single_char():
    try:
        char = getch.getch()
        return char
    except KeyboardInterrupt:
        return None

if __name__ == '__main__':

    camera = init_camera(cam_size=(640, 480))
    time1 = time()
    
    while True:
            
        #cam_size=(width, height)
        path = take_photo(picam2=camera)
        time2 = time()    
        
        squareR, squareL, new_path = apply_threshold_and_count(img_path=path, largura=50, altura=50, margem=50)
        time3 = time()
        
        # se preto menor que 50%  
        if squareL[0] > 50 and squareR[0] > 50  :
            # frente(tempo, pote, potd)
            frente(0.8, 40, 40)
        
        print_square_info(squareR, squareL)
        print_time_spent(times=[time0, time1, time2, time3])
        
    print('End with sucess')
    
    
    