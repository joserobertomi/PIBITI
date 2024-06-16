from time import sleep
import RPi.GPIO as gpio 
gpio.cleanup()

def init_motores():

    gpio.cleanup()
    gpio.setmode(gpio.BOARD)

    gpio.setup(11, gpio.OUT) # controle motor esquerdo
    gpio.setup(13, gpio.OUT) # controle motor esquerdo

    gpio.setup(16, gpio.OUT) # controle motor esquerdo
    gpio.setup(18, gpio.OUT) # controle motor esquerdo

    gpio.setup(33, gpio.OUT) # pwm motor esquerdo
    gpio.setup(35, gpio.OUT) # pwm motor direito 

    gpio.output(11, gpio.HIGH)
    gpio.output(13, gpio.LOW)
    gpio.output(16, gpio.LOW)
    gpio.output(18, gpio.HIGH)

    # To create a PWM instance: p = GPIO.PWM(channel, frequency)
    return gpio.PWM(33, 1000).start(0), gpio.PWM(35, 1000).start(0)

def frente(sec, pot_esq, pot_dir, motores):
    '''
    Movimenta o veiculo para frente; 
    (sleep(sec), pot_esq(de 0 a 100),  pot_dir(de 0 a 100))
    '''
    
    pwm_esq, pwm_dir = motores

    # To start a pwm: p.start(dc)   
    # Where dc is the duty cycle (0.0 <= dc <= 100.0)
    pwm_esq.start(pot_esq)
    pwm_dir.start(pot_dir)


def decisao_de_movimento(base_esq, base_dir, pot_max): 
    
    print(f'Base Esq: {base_esq} | Base Dir: {base_dir}')
    
    pot_esq = (base_dir/132*(pot_max-40)) + 40
    pot_dir = (base_esq/132*(pot_max-40)) + 40
    
    print(f'Potencia Esq: {pot_esq} | Potencia Dir: {pot_dir}')
    
    return pot_esq, pot_dir