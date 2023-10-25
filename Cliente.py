from Tarjeta import Tarjeta

numeroCliente = 10000

class Cliente():
    
    def __init__(self,nombre,apellido,dni,tipo):
        #while self.numero != None:
            #numeroCliente += 1

        self.numero = numeroCliente
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.tipo = tipo
        self.transacciones = []
        
        self.tarjetaDebito = []

    def __str__(self):
        #return(f'numero: {self.numero}')
        return(f'numero: {self.numero} , nombre: {self.nombre} , apellido: {self.apellido} ,dni: {self.dni} , tipo: {self.tipo} , transacciones:{self.transacciones}')

    def retiro_efectivo_cajero_automatico(self):
        pass

    def retiro_efectivo_por_caja(self):
        pass

    def compra_en_cuotas_tarjeta_credito_(self):
        pass

    def compra_tarjeta_credito_(self):
        pass

    def alta_tarjeta_credito_(self):
        pass

    def alta_tarjeta_debido(self):
        pass

    def alta_chequera(self):
        pass

    def alta_cuenta_cte_(self):
        pass

    def alta_caja_de_ahorro_(self):
        pass

    def alta_cuenta_de_inversion(self):
        pass

    def compra_dolar(self):
        pass

    def venta_dolar(self):
        pass

    def transferencia_enviada_(self):
        pass

    def transferencia_recibida_(self):
        pass

class Classic(Cliente):

    def __init__(self, nombre, apellido, dni):
        super().__init__(nombre, apellido, dni,"CLASSIC")
        if len(self.tarjetaDebito) > 1:
            print('No se pueden tener mas de 1 tarjeta')
        else:
            self.tarjetaDebito = Tarjeta('DEBITO',self.nombre + " " + self.apellido) 


class Gold(Cliente):

    def __init__(self, nombre, apellido, dni):
        super().__init__(nombre, apellido, dni,"GOLD")
        if len(self.tarjetaDebito) > 1:
            print('No se pueden tener mas de 1 tarjeta')
        else:
            self.tarjetaDebito = Tarjeta('DEBITO',self.nombre + " " + self.apellido) 

class Black(Cliente):

     def __init__(self, nombre, apellido, dni):
        super().__init__(nombre, apellido, dni,"BLACK")
        if len(self.tarjetaDebito) > 5:
            print('No se pueden tener mas de 5 tarjeta')
        else:
            self.tarjetaDebito = Tarjeta('DEBITO',self.nombre + " " + self.apellido) 


paco = Classic('Paco','Alcor',12345678)
valen = Gold('Valentino','Cambria',12345678)
seba = Gold('Sebastian','Nor',8754321)

print(paco)
print(valen)
print(seba)