def vcedula(texto):
    nocero = texto.strip("0")
    cedula = int(nocero,0)
    verificador = cedula%10
    numero = cedula//10
    suma = 0
    while (numero > 0):
        posimpar = numero%10
        numero   = numero//10
        posimpar = 2*posimpar
        if (posimpar  > 9):
            posimpar = posimpar-9
        pospar = numero%10
        numero = numero//10
        suma = suma + posimpar + pospar
    decenasup = suma//10 + 1
    calculado = decenasup*10 - suma
    if (calculado  >= 10):
        calculado = calculado - 10
    if (calculado == verificador):
        validado = True
    else:
        validado = False
        
    return validado
print('validación: ', vcedula('0401645221'))