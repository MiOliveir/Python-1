def toDolar(var, dest): 

     

    if dest == "EUR": 

        return var*0.92901 

    elif dest == "GBP": 

        return var*0.79689 

    elif dest == "JPY": 

        return var*152.982 

    elif dest == "BRL": 

        return var*5.07054    
    else: 
        return "Inválido"
     

def toEuro(var, dest):  

    if dest == "USD": 

        return var*1.07619 

    elif dest == "GBP": 

        return var*0.85767 

    elif dest == "JPY": 

        return var*164.647 

    elif dest == "BRL": 

        return var*5.45685 
    else: 
        return "Inválido"
 

def toLibra(var, dest):  

    if dest == "EUR": 

        return var*1.16564 

    elif dest == "USD": 

        return var*1.25461 

    elif dest == "JPY": 

        return var*191.94 

    elif dest == "BRL": 

        return var*6.36154  
    else: 
        return "Inválido"
    

def toIene(var, dest):  

    if dest == "EUR": 

        return var*0.00654 

    elif dest == "GBP": 

        return var*0.00521 

    elif dest == "USD": 

        return var*0.00654 

    elif dest == "BRL": 

        return var*0.03314  
    else: 
        return "Inválido"
 

def toReal(var, dest):  

    if dest == "EUR": 

        return var*0.18305 

    elif dest == "GBP": 

        return var*0.15702 

    elif dest == "JPY": 

        return var*30.1439 

    elif dest == "USD": 

        return var*0.19704                  
    else: 
        return "Inválido"
def main(): 

    while True: 

        print("\n Conversor de moedas\n1.Dólar\n2.Euro\n3.Libra Esterlina\n4.Iene Japonês\n5.Real Brasileiro\n6.Sair") 
 
        escolha = input("Escolha uma das moeda para converter (1-6):") 

        if escolha in ["1", "2", "3", "4", "5"]: 

            valor = float(input("Digite o valor a ser convertido: ")) 

            destino = input("Digite a moeda de destino (): ").upper() 

            if escolha == "1": 

                print(f"Valor convertido: {toDolar(valor, destino)}") 

            elif escolha == "2": 

                print(f"Valor convertido: {toEuro(valor, destino)}") 

            elif escolha == "3": 

                print(f"Valor convertido: {toLibra(valor, destino)}") 

            elif escolha == "4": 

                print(f"Valor convertido: {toIene(valor, destino)}") 

            elif escolha == "5": 

                print(f"Valor convertido: {toReal(valor, destino)}")                 

        elif escolha == "6": 

            print("Fim do programa") 

            break         

        else: 

            print("inválido") 
main() 

 