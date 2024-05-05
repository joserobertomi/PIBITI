import numpy as np

def print_aim_result(result):
    print(f'-------------------\n|  {result[0]}  |  {result[1]}  |  {result[2]}  |\n|  {result[3]}  |  {result[4]}  |  {result[5]}  |\n|  {result[6]}  |  {result[7]}  |  {result[8]}  |\n-------------------')
    
    
def take_move_decision(base): 
    a = np.array([(base[0], base[1], base[2]), (base[3], base[4], base[5]), (base[6], base[7], base[8])])
    if np.sum(a[:,1]) == 3:
        stt = 'Tenho uma reta'
        a[:,0] = a[:,0] * (-1)
        print(a) 