from Tarjeta import Tarjeta
from Transacciones import Transacciones
from Operaciones import Operaciones
import json

#Clase cliente
class Cliente():
    
    #ID univoco para cada cliente, que arranca en 10000
    idIncremental = 10001

    #Constructor de la clase
    def __init__(self,nombre,apellido,dni,tipo):
        #Numero de cliente
        self.numero = self.idIncremental
        Cliente.idIncremental += 1

        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.tipo = tipo
        self.cuentas = []  #Tiene que ser un enumerado CORREGIR
        self.transacciones = []
        self.tarjetaS = []
        
        # ------------------- RESTRICCIONES --------------------

        #Restricciones de operaciones que estar presentes en las demas clases y seran modificadas
        
        #Cantidad de tarjetas de debito que puede tener
        self.cant_tarjetas_debito = None

        #Cantidad tarjetas credito
        self.cant_tarjetas_credito = None

        #Cantidad caja de ahorro en pesos/dolares
        self.cant_caja_ahorro = None

        #Cantidad retiros sin comisiones
        self.cant_retiros_sin_comisiones = "Ilimitado" #Black y Gold

        #Limite diario retiro x cajero
        self.limite_diario = 10000

        #Limites de pago
        self.limite_un_pago = None
        self.limite_cuotas = None

        #Comisiones
        self.comision_transferencia_saliente = 0
        self.comision_transferencia_entrante = 0

    #Generar reporte
    def generar_reporte(self):
        reporte = {
            "numero": self.numero,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "dni": self.dni,
            "tipo": self.tipo,
            "transacciones": []
        }
        for transaccion in self.transacciones:
            reporte["transacciones"].append({
                "estado": "transaccion.estado",
                "tipo": transaccion.tipo,
                "cuentaNumero": transaccion.cuentaNumero,
                "permitidoActualParaTransaccion": transaccion.permitidoActualParaTransaccion,
                "monto": transaccion.monto,
                "fecha": transaccion.fecha,
                "numero": transaccion.numero
            })

        return json.dumps(reporte, indent=2) #Transformo la salida en formato JSON

    #Metodo que agrega una transaccion
    def agregarTransaccion(self,transaccion):
        self.transacciones.append(transaccion)

    #Metodo que me dice la cantidad de tarjetas de credito/debito que tiene el cliente
    def cantTarjetas(self,tipoTarjeta):
        cantidad = 0
        for tarjetaCliente in self.tarjetaS:
            if tarjetaCliente.getTipo() == tipoTarjeta:
                cantidad += 1
        return cantidad


    #Metodo que agrega una tarjeta a el cliente
    def agregarTarjeta(self,tipoTarjeta,empresaTarjeta):
        #Creo la tarjeta
        tarjetaAgregar = Tarjeta(self.nombre + " " + self.apellido,tipoTarjeta,empresaTarjeta)
        #Compruebo las cantidad 
        cantDebito = self.cantTarjetas("Debito")
        cantCredito = self.cantTarjetas("Credito")
        #Me fijo si no paso los limites estipulados
        if not (cantDebito < self.cant_tarjetas_debito or cantCredito < self.cant_tarjetas_credito):
            print('No se puede agregar la tarjeta de credito/debito, ya es el limite')
        else:
            self.tarjetaS.append(tarjetaAgregar) #Agrego la tarjeta

    #Metodo que vincula una cuenta a el cliente
    def agregarCuenta(self,cuenta):
        self.cuentas.append(cuenta)

    # ------------ GETTERS -----------------

    #Todas las transacciones hechas por el cliente
    def getTransacciones(self):
        return self.transacciones
    
    #Cantidad de transsaciones hechas por el cliente
    def getCantTrasacciones(self):
        return len(self.transacciones)
    
    #Get con todas las tarjetas
    def getTarjetas(self):
        text = ''
        for i in self.tarjetaS:
            text += str(i) + "\n"
        return text

#Clases que heredan de Cliente
class Classic(Cliente):

    #Constructor
    def __init__(self, nombre, apellido, dni):
        super().__init__(nombre, apellido, dni,"CLASSIC")

        #------------- RESTRICCIONES -------------------
        self.cant_tarjetas_debito = 1
        self.cant_tarjetas_credito = 0
        self.cant_caja_ahorro_pesos = 1
        self.cant_caja_ahorro_dolares = 1
        self.cant_retiros_sin_comisiones = 5
        self.limite_diario = 10000
        self.comision_transferencia_entrante = 0,5
        self.comision_transferencia_saliente = 0,1

        #------------- METODOS ----------------

class Gold(Cliente):

    def __init__(self, nombre, apellido, dni):
        super().__init__(nombre, apellido, dni,"GOLD")

        #------------- RESTRICCIONES -------------------
        self.cant_tarjetas_debito = 1
        self.cant_tarjetas_credito = 5
        self.cant_caja_ahorro = 2 #pesos y dolares
        self.cant_cuenta_corriente = 1 #Agregada 
        self.limite_un_pago = 150000
        self.limite_cuotas = 100000
        self.limite_diario = 20000
        self.comision_transferencia_entrante = 0,1
        self.comision_transferencia_saliente = 0,5

class Black(Cliente):

     def __init__(self, nombre, apellido, dni):
        super().__init__(nombre, apellido, dni,"BLACK")

            #------------- RESTRICCIONES -------------------
        self.cant_tarjetas_debito = 5
        self.cant_tarjetas_credito = 10
        self.cant_caja_ahorro = 5 #pesos y dolares
        self.cant_cuenta_corriente = 3 #Agregada 
        self.limite_un_pago = 500000
        self.limite_cuotas = 600000
        self.limite_diario = 100000


# Funciones solicitadas

def calcular_monto_total(precio_dolar, monto):
    impuesto_pais = 0.25 #Actual argentina
    ganancias = 0.35
    monto_sin_impuestos = precio_dolar * monto
    impuesto_total = monto_sin_impuestos * (impuesto_pais + ganancias)
    monto_total = monto_sin_impuestos + impuesto_total
    return monto_total

def descontar_comision(monto, comision_porcentaje):
    comision = (comision_porcentaje / 100) * monto
    monto_descontado = monto - comision
    return monto_descontado

def calcular_monto_plazo_fijo(monto_plazo_fijo, interes):
    monto_final = monto_plazo_fijo + (monto_plazo_fijo * interes)
    return monto_final


#Pruebas

paco = Classic('Paco','Alcor',12345678)
valen = Gold('Valentino','Cambria',12345678)
seba = Gold('Sebastian','Nor',8754321)

print(paco)
print(valen)
print(seba)

paco.agregarTransaccion(Transacciones(Operaciones.RETIRO_EFECTIVO_CAJERO_AUTOMATICO.value,190,9000,1000,"10/10/2022 16:00:55",1))

print(paco.generar_reporte())

#Test limites de tarjetas
paco.agregarTarjeta("Debito","VISA")
paco.agregarTarjeta("Credito","VISA")
print(paco.getTarjetas())