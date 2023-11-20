
from django.core.exceptions import ValidationError

class ValidarCedulaUsurio:
       
    def validarCedula(self, value):
        if len(value) != 10:
            raise ValidationError(f"Error: La cédula ingresada tiene {len(value)} caracteres y debe tener 10") 

        nocero = value.strip("0")
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
            return value
        else:
            raise ValidationError("La cédula ingresada no es válida") 
    def __init__(self, cedula):
        self.validarCedula(cedula)
        
class setValorExtranjero:
    def __init__(self, es):
        self.es=es
    def __call__(self, value):
        if(value):
            raise ValidationError("La cédula ingresada no es válida") 
        return value
def getMeses():
    return ['Enero', 'Febrero', 'Marzo','Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']