from time import sleep
import getch
import RPi.GPIO as gpio 
gpio.cleanup()

def take_move_decision2(base_esq, base_dir, pot_max): 
    
    pot_esq = abs(pot_max/(base_esq+1))
    pot_dir = abs(pot_max/(base_dir+1))
    
    print(f'Potencia Esq: {pot_esq} | Potencia Dir: {pot_dir}')
    
    if pot_esq < 30:
        pot_esq = 0
    elif pot_esq < 45:
        pot_esq = 45
        
    if pot_dir < 30:
        pot_dir = 0 
    elif pot_dir < 45:
        pot_dir = 45
        
    if (not pot_esq) and (not pot_dir): 
        return pot_max, pot_max
    
    return pot_esq, pot_dir

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
    '''
    Movimenta o veiculo para frente; 
    (sleep(sec), pot_esq(de 0 a 100),  pot_dir(de 0 a 100))
    '''
        
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

