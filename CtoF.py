def CtoF(x): 
    return (x*1.8)+32 
def FtoC(F): 
    return (F-32)*5/9 
def main(): 
    while True: 
        print("\nConversor de Temperatura: \n1. C -> F \n2. F -> C\n3. Sair ") 
        escolha = input("Escolha uma opção (1/2/3)") 
        if escolha == "1": 
            celsius = float(input("Digite a temperatura em célcius:", )) 
            print("Temepratura em Fahrenhit:",CtoF(celsius)) 
        elif escolha == "2": 
            F = float(input("Digite a tempetatura em Fahrenhit")) 
            print("Temepratura em Celsius:", FtoC(F)) 
        elif escolha == "3": 
            print("Saindo do programa") 
            break 
        else: 
            print("Opção inválida") 

main() 

 

 