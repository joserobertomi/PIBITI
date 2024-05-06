def print_aim_result(result):
    print(f'-------------------\n|  {result[0]}  |  {result[1]}  |  {result[2]}  |\n|  {result[3]}  |  {result[4]}  |  {result[5]}  |\n|  {result[6]}  |  {result[7]}  |  {result[8]}  |\n-------------------')
    
    
def take_move_decision(base, potencia_max): 
    if not (base[2]+base[6]+base[0]+base[8]):
        return potencia_max*0.75, potencia_max*0.75
    elif base[2]+base[6]+base[0]+base[8] == 1:
        return ((base[2]+base[6])/3)*potencia_max+potencia_max/3, ((base[0]+base[8])/3)*potencia_max+potencia_max/3
        
    return ((base[2]+base[6])/6)*potencia_max, ((base[0]+base[8])/6)*potencia_max


print(take_move_decision([0,0,0,0,0,0,0,0,0], 100))
print(take_move_decision([0,1,0,0,1,0,0,1,0], 100))
print(take_move_decision([1,1,0,0,1,0,0,1,1], 100))
print(take_move_decision([0,1,1,0,1,0,1,1,0], 100))
print(take_move_decision([0,1,0,0,1,0,0,1,1], 100))
print(take_move_decision([0,1,1,0,1,0,0,1,0], 100))