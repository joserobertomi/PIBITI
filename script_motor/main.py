import RPi.GPIO as gpio
import time
import getch

def init():    
    gpio.setmode(gpio.BCM)
    gpio.setup(17, gpio.OUT)
    gpio.setup(22, gpio.OUT)
    gpio.setup(23, gpio.OUT)
    gpio.setup(24, gpio.OUT)
    
def frente(sec): # OKOK
    init()
    gpio.output(17, True)
    gpio.output(22, False)
    gpio.output(23, True)
    gpio.output(24, False)
    time.sleep(sec)
    gpio.cleanup() 
    
def re(sec): #PauPau
    init()
    gpio.output(17, False)
    gpio.output(22, True)
    gpio.output(23, False)
    gpio.output(24, True)
    time.sleep(sec)
    gpio.cleanup()
    
def giro_antih(sec): # OKOK
    init()
    gpio.output(17, False)
    gpio.output(22, True)
    gpio.output(23, True)
    gpio.output(24, False)
    time.sleep(sec)
    gpio.cleanup()
    
def giro_h(sec): # PauPau
    init()
    gpio.output(17, True)
    gpio.output(22, False)
    gpio.output(23, False)
    gpio.output(24, True)
    time.sleep(sec)
    gpio.cleanup()
    
def parab_esquerda(sec): # OKOK
    init()
    gpio.output(17, False)
    gpio.output(22, False)
    gpio.output(23, True)
    gpio.output(24, False)
    time.sleep(sec)
    gpio.cleanup()
    
def parab_direita(sec): #OKOK
    init()
    gpio.output(17, True)
    gpio.output(22, False)
    gpio.output(23, False)
    gpio.output(24, False)
    time.sleep(sec)
    gpio.cleanup()
    
    
def manuntencao(sec): 
    init()
    gpio.output(17, False)
    gpio.output(22, False)
    gpio.output(23, True)
    gpio.output(24, True)
    time.sleep(sec)
    gpio.cleanup()

   
def teste(seconds):    
    print('Hello World')  
    time.sleep(seconds)
    
    print("Frente")
    frente(seconds)
    #time.sleep(seconds+2)
    
    print("Re")
    re(seconds)
    #time.sleep(seconds+2)
    
    print("Giro horario")
    giro_h(seconds)
    #time.sleep(seconds+2)
    
    print("Giro anti-horario")
    giro_antih(seconds)
    #time.sleep(seconds+2)
    
    print("Parabola esquerda")
    parab_esquerda(seconds)
    #time.sleep(seconds+2)
    
    print("Parabola direita")
    parab_direita(seconds)
    #time.sleep(seconds+2)

def comando(seconds): 
    print('Hello World') 
    time.sleep(seconds)
    
    c = 20
    while c > 0 :
        a = input(str('Comando: ')) 
        if a == "f":
            print("Frente")
            frente(seconds)
            #time.sleep(seconds+2)
        elif a == "r":
            print("Re")
            re(seconds)
            #time.sleep(seconds+2)
        elif a == "gh":    
            print("Giro horario")
            giro_h(seconds)
            #time.sleep(seconds+2)
        elif a == "ga":
            print("Giro anti-horario")
            giro_antih(seconds)
            #time.sleep(seconds+2)
        elif a == "pe":    
            print("Parabola esquerda")
            parab_esquerda(seconds)
            #time.sleep(seconds+2)
        elif a == "pd":   
            print("Parabola direita")
            parab_direita(seconds)
            #time.sleep(seconds+2)
        else: 
            print("Comando invalido")
            
def controle_pelo_computador():    
    seconds = 0.025
    a = ''
    while a != 'x' :
        a = get_single_char()
        print()
        if a is not None: 
            if a == "w":
                #print("Frente")
                frente(seconds)
                #time.sleep(seconds+2)
            elif a == "s":
                #print("Re")
                re(seconds)
                #time.sleep(seconds+2)
            elif a == "d":    
                #print("Giro horario")
                giro_h(seconds)
                #time.sleep(seconds+2)
            elif a == "a":
                #print("Giro anti-horario")
                giro_antih(seconds)
                #time.sleep(seconds+2)
            elif a == "q":    
                #print("Parabola esquerda")
                parab_esquerda(seconds)
                #time.sleep(seconds+2)
            elif a == "e":   
                #print("Parabola direita")
                parab_direita(seconds)
                #time.sleep(seconds+2)
            #else: 
                #print("Comando invalido")
    print("Precionou 'x', saindo do modo de controle")

def get_single_char():
    try:
        char = getch.getch()
        return char
    except KeyboardInterrupt:
        return None

if __name__ == '__main__':
    controle_pelo_computador()
    print('Arreguei')
    