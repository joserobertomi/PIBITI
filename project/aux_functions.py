def print_aim_result(result):
    print(f'-------------------\n|  {result[0]}  |  {result[1]}  |  {result[2]}  |\n|  {result[3]}  |  {result[4]}  |  {result[5]}  |\n|  {result[6]}  |  {result[7]}  |  {result[8]}  |\n-------------------')
    
    
def take_move_decision(base, potencia_max): 
    if not (base[2]+base[6]+base[0]+base[8]):
        if not (base[1]+base[5]+base[7]): 
            return 0, 0
        return potencia_max, potencia_max
    elif base[2]+base[6]+base[0]+base[8] == 1:
        return ((base[2]+base[6])/2)*potencia_max, ((base[0]+base[8])/2)*potencia_max
    
    return ((base[2]+base[6])/4)*potencia_max+potencia_max/2, ((base[0]+base[8])/4)*potencia_max+potencia_max/2
        
def tests():
    print(take_move_decision([0,0,0,0,0,0,0,0,0], 100))
    print_aim_result([0,0,0,0,0,0,0,0,0])
    print(take_move_decision([0,1,0,0,1,0,0,1,0], 100))
    print_aim_result([0,1,0,0,1,0,0,1,0])
    print(take_move_decision([1,1,0,0,1,0,0,1,1], 100))
    print_aim_result([1,1,0,0,1,0,0,1,1])
    print(take_move_decision([0,1,1,0,1,0,1,1,0], 100))
    print_aim_result([0,1,1,0,1,0,1,1,0])
    print(take_move_decision([0,1,0,0,1,0,0,1,1], 100))
    print_aim_result([0,1,0,0,1,0,0,1,1])
    print(take_move_decision([0,1,1,0,1,0,0,1,0], 100))
    print_aim_result([0,1,1,0,1,0,0,1,0])
    print(take_move_decision([1,1,0,0,1,0,0,1,0], 100))
    print_aim_result([1,1,0,0,1,0,0,1,0])
    print(take_move_decision([0,1,1,0,1,0,0,1,0], 100))
    print_aim_result([0,1,0,0,1,0,1,1,0])