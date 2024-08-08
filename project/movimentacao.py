from time import sleep
import RPi.GPIO as gpio 

def init_motores():

    gpio.cleanup()
    gpio.setmode(gpio.BOARD)

    gpio.setup(11, gpio.OUT) # controle motor esquerdo
    gpio.setup(13, gpio.OUT) # controle motor esquerdo

    gpio.setup(16, gpio.OUT) # controle motor esquerdo
    gpio.setup(18, gpio.OUT) # controle motor esquerdo

    gpio.setup(33, gpio.OUT) # pwm motor esquerdo
    gpio.setup(35, gpio.OUT) # pwm motor direito 

    pwm_esq = gpio.PWM(33, 1000)
    pwm_dir = gpio.PWM(35, 1000)
    
    return pwm_esq, pwm_dir

def frente(pwm_esq, pot_esq, pwm_dir, pot_dir):
    pwm_esq.stop()
    pwm_dir.stop()

    gpio.output(11, gpio.HIGH)
    gpio.output(13, gpio.LOW)
    gpio.output(16, gpio.LOW)
    gpio.output(18, gpio.HIGH)

    pwm_esq.start(pot_esq)
    pwm_dir.start(pot_dir)


def giro_h(pwm_esq, pot_esq, pwm_dir, pot_dir):
    pwm_esq.stop()
    pwm_dir.stop()
    
    gpio.output(11, gpio.HIGH)
    gpio.output(13, gpio.LOW)
    gpio.output(16, gpio.HIGH)
    gpio.output(18, gpio.LOW)
    
    pwm_esq.start(pot_esq)
    pwm_dir.start(pot_dir)

    
def giro_antih(pwm_esq, pot_esq, pwm_dir, pot_dir):
    pwm_esq.stop()
    pwm_dir.stop()
    
    gpio.output(11, gpio.LOW)
    gpio.output(13, gpio.HIGH)
    gpio.output(16, gpio.LOW)
    gpio.output(18, gpio.HIGH)
    
    pwm_esq.start(pot_esq)
    pwm_dir.start(pot_dir)


def parado(pwm_esq, pwm_dir):
    pwm_esq.stop()
    pwm_dir.stop()


def decisao_de_movimento(base_esq, base_dir, pot_max, pot_min, soma_max): 

    if not (base_esq + base_dir):
        return 0, 0
    
    print(f'Base Esq: {base_esq} | Base Dir: {base_dir}')
    
    pot_esq = (base_dir/soma_max*(pot_max-pot_min)) + pot_min
    pot_dir = (base_esq/soma_max*(pot_max-pot_min)) + pot_min
    
    print(f'Potencia Esq: {pot_esq} | Potencia Dir: {pot_dir}')
    
    return pot_esq, pot_dir

