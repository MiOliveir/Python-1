import os 

import math 

 

 

def adicao(x, y): 

    return x + y 

 

 

def subtracao(x, y): 

    return x - y 

 

 

def multiplicacao(x, y): 

    return x * y 

 

 

def divisao(x, y): 

    if y == 0: 

        return "Erro! Divisão por zero não é permitida." 

    else: 

        return x / y 

 

 

def raizq(x): 

    return math.sqrt(x) 

 

 

def quadr(x): 

    return x**2 

 

 

def triplo(x): 

    return x*3 

 

 

def metade(x): 

    return x/2 

 

 

def exp(x, y): 

    res = 1 

    for i in range(y): 

        res = res*x 

    return res 

 

 

def posi(x): 

    return "Positivo" if x > 0 else "Negativo" 

 

 

def inte(x): 

    return "inteiro" if isinstance(x, int) else "não é inteiro" 

 

 

def verifica(x): 

    i = 0 

    while x > 5: 

        i = i + 1 

        x = float(input("Opção invalida, o número deve ser de 0-5 ")) 

        if i == 3: 

            exit()            

             

                     

           

 

while True: 

    os.system('clear') 

    print("1 +\n2 -\n3 x\n4 / \n5 raizq\n6 quadrado\n7 triplo\n8 metade\n9 exp (x^2)\nP Posi?\nI Inteiro?\nx - SAIR") 

 

    print("\n") 

 

    opcao = input("Digite sua opção (1-9 I/P/X ): ") 

 

    if opcao.upper() == "X": 

        print("O programa vai terminar") 

        exit() 

 

    elif opcao == "1" or opcao == "2" or opcao == "3" or opcao == "4" or opcao == "9": 

 

        num1 = float(input("Digite o primeiro número: ")) 

        num2 = float(input("Digite o segundo número: ")) 

 

        verifica(num1) 

        verifica(num2) 

 

        if opcao == '1': 

            print("Resultado:", adicao(num1, num2)) 

        elif opcao == '2': 

            print("Resultado:", subtracao(num1, num2)) 

        elif opcao == '3': 

            print("Resultado:", multiplicacao(num1, num2)) 

        elif opcao == '4': 

            print("Resultado:", divisao(num1, num2)) 

        elif opcao == "9": 

            print("O número Elevado a 2 é", exp(num1, num2)) 

        else: 

            print("Opção inválida") 

 

        X = input("Prima ENTER para continuar.") 

 

    else: 

        num1 = float(input("Digite o primeiro número: ")) 

 

        if opcao == "5": 

 

            print("Resultado:", raizq(num1)) 

 

        elif opcao == "6": 

 

            print("Resultado:", quadr(num1)) 

 

        elif opcao == "7": 

 

            print("Resultado:", triplo(num1)) 

 

        elif opcao == "8": 

 

            print("Resultado:", metade(num1)) 

 

        elif opcao.upper() == "P": 

 

            print("O número é", posi(num1)) 

 

        elif opcao.upper() == "I": 

 

            try: 

                num1 = int(num1) 

                print("INTEiRO") 

            except: 

                print("NO INTEIRO") 

        else: 

            print("Opção inválida") 

 

        X = input("Prima ENTER para continuar.") 

 

 