import random
from datetime import datetime, timedelta

class Tarjeta:
    #Constructor clase tarjeta
    def __init__(self, titular,tipo,empresa):
        self.numero = self.generar_numero_tarjeta()
        self.titular = titular
        self.vencimiento = self.generar_fecha_vencimiento()
        self.saldo = 100000
        self.tipo = tipo
        self.empresa = empresa

    #Metodo que genera de forma aleatoria los 16 digitos de una tarjeta
    @staticmethod
    def generar_numero_tarjeta():
        numero = ''.join(str(random.randint(0, 9)) for _ in range(16))
        return numero

    # Metodo que genera una fecha de vencimiento aleatoria dentro de los próximos 5 años
    @staticmethod
    def generar_fecha_vencimiento():
        hoy = datetime.now()
        vencimiento = hoy + timedelta(days=random.randint(1, 1825))  # 5 años en días
        return vencimiento.strftime("%m/%y")
    
    #Getter Tarjeta
    def getTarjeta(self):
        numTarjeta = ''
        contador = 0
        #Obtengo la tarjeta con espacios cada 4 numeros
        for i in range(len(self.numero)):
            if (contador == 4):
                numTarjeta = numTarjeta + '-'
                contador = 1
            else:
                contador += 1
            numTarjeta = numTarjeta + self.numero[i]

        return numTarjeta

""" test tarjeta:
mi_tarjeta = Tarjeta("Juan Pérez","DEBITO","AGUA")

print(f"Número de tarjeta: {mi_tarjeta.getTarjeta()}")
print(f"Fecha de vencimiento: {mi_tarjeta.vencimiento}")
print(mi_tarjeta)"""
