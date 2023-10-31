from Tarjeta import Tarjeta
from Transaccion import Transaccion
from Chequera import Chequera
from Cuenta import Cuenta
import json
from datetime import datetime

# --------------------- CLASE CLIENTE ----------------------------

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
        self.Transaccion = []
        self.tarjetaS = []
        self.chequera = []
        
        # ------------------- RESTRICCIONES --------------------

        #Restricciones de operaciones que estar presentes en las demas clases y seran modificadas
        
        #Cantidad de tarjetas de debito que puede tener
        self.cant_tarjetas_debito = None

        #Cantidad tarjetas credito
        self.cant_tarjetas_credito = None

        #Cantidad caja de ahorro en pesos/dolares
        self.cant_caja_ahorro = 0
        self.cant_cuenta_corriente = 0

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

        #Permitidos retiro caja
        self.permitido_actual = 9000

        #Chequera
        self.cant_chequera = 0

    #Generar reporte
    def generar_reporte(self):
        reporte = {
            "numero": self.numero,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "dni": self.dni,
            "tipo": self.tipo,
            "Transaccion": []
        }
        numeroTransaccion = 0
        for transaccion in self.Transaccion:
            numeroTransaccion += 1
            transaccion_data  = {
                "estado": transaccion.estado,
                "tipo": transaccion.tipo,
                "cuentaNumero": transaccion.cuentaNumero,
                "permitidoActualParaTransaccion": transaccion.permitidoActualParaTransaccion,
                "monto": transaccion.monto,
                "fecha": transaccion.fecha,
                "numero": numeroTransaccion
            }

            # Filtrar los valores que no son None
            transaccion_data = {k: v for k, v in transaccion_data.items() if v is not None}

            #Guardo la transaccion en el reporte
            reporte["Transaccion"].append(transaccion_data)

        return json.dumps(reporte, indent=3) #Transformo la salida en formato JSON

    #Metodo que agrega una transaccion
    def agregarTransaccion(self,transaccion):
        self.Transaccion.append(transaccion)

    #Metodo que me dice la cantidad de tarjetas de credito/debito que tiene el cliente
    def cantTarjetas(self,tipoTarjeta):
        cantidad = 0
        for tarjetaCliente in self.tarjetaS:
            if tarjetaCliente.getTipo() == tipoTarjeta:
                cantidad += 1
        return cantidad
    
    #Metodo que me dice la cantidad de cuentas peso o dolares que tiene el cliente
    def cantCuentas(self,tipoCuenta):
        cantidad = 0
        for cuentaCliente in self.cuentas:
            if cuentaCliente.getTipoCuenta() == tipoCuenta:
                cantidad += 1
        return cantidad

    #Metodo que agrega una tarjeta a el cliente
    def agregarTarjeta(self,tipoTarjeta,empresaTarjeta):
        #Creo la tarjeta
        tarjetaAgregar = Tarjeta(self.getTitular(),tipoTarjeta,empresaTarjeta)
        #Compruebo las cantidad 
        cantDebito = self.cantTarjetas("Debito")
        cantCredito = self.cantTarjetas("Credito")

        #Creo la transaccion
        agregarTarjetaTransaccion = Transaccion("ALTA_TARJETA_" + tipoTarjeta.upper() + "_" + empresaTarjeta.upper(),None,None,None,datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

        #Me fijo si no paso los limites estipulados
        if not (cantDebito < self.cant_tarjetas_debito and cantCredito < self.cant_tarjetas_credito):
            #Si esta fuera de los rangos permitidos muestro en pantalla y se rechaza la transaccion
            print('No se puede agregar la tarjeta de credito/debito, ya es el limite')
            agregarTarjetaTransaccion.setEstado("INVALIDO")
        else:
            #Caso contrario, el estado paso a aprobado y agrego la tarjeta
            agregarTarjetaTransaccion.setEstado("ACEPTADA")
            self.tarjetaS.append(tarjetaAgregar)

        #Cargo la transaccion
        self.agregarTransaccion(agregarTarjetaTransaccion)        

    #Metodo que crea una cuenta a el cliente
    def agregarCuenta(self,tipoCuentaAlta,tipoMoneda):
        altaCuenta = Transaccion("ALTA_" + tipoCuentaAlta + "_" + tipoMoneda, None, None, None, datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

        #Chequeo que no supere la cantidad de cuentas maximas
        #Veo si es cuenta corriente o caja de ahorro
        cantCuentasCorriente = self.cantCuentas("CUENTA_CTE")
        cantCajaAhorro = self.cantCuentas("CAJA_DE_AHORRO") 
        comparacionCuentaCorriente = (tipoCuentaAlta == "CUENTA_CTE") and (cantCuentasCorriente< self.cant_cuenta_corriente)
        comparacionCajaAhorro = (tipoCuentaAlta == "CAJA_DE_AHORRO") and (cantCajaAhorro < self.cant_caja_ahorro)
        comparacionInversion = (tipoCuentaAlta == "INVERSION" and self.tipo != "CLASSIC")


        if  not (comparacionCuentaCorriente or comparacionCajaAhorro or comparacionInversion):
                print('No se puede agregar la cuenta')
                altaCuenta.setEstado("RECHAZADA")
        else:
            #Creo que la cuenta y la vinculo
            altaCuenta.setEstado("APROBADA")
            cuentaNueva = Cuenta(tipoCuentaAlta,tipoMoneda)
            self.cuentas.append(cuentaNueva)
        
        #Cargo la transaccion
        self.agregarTransaccion(altaCuenta)
 

    #Metodo para retirar efectivo, por caja o cajero
    def retiroEfectivo(self,tipoRetiro,cuentaNumero,monto):
        #Creo la transaccion
        retirarEfectivo = Transaccion("RETIRO_EFECTIVO_" + tipoRetiro.upper(),cuentaNumero,self.permitido_actual,monto,datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

        #Me fijo que el saldo a retirar no pase al permitido
        if (monto > self.permitido_actual):
            #Rechazo transaccion
            print('El monto es mayor al permitido actual')
            retirarEfectivo.setEstado("RECHAZADA")
        else:
            #Caso contrario, el estado pasa a aprobado
            retirarEfectivo.setEstado("ACEPTADA")

        #Cargo la transaccion
        self.agregarTransaccion(retirarEfectivo)  

    #Metodo para realizar una compra por tarjeta, en cuotas o total
    def compraTarjeta(self,tipoCompra,tipoTarjeta,cuentaNumero, monto):
        #Creo la transaccion
        comprar = Transaccion("COMPRA_" + tipoCompra.upper() + "_TARJETA_" + tipoTarjeta.upper(),cuentaNumero,self.permitido_actual,monto,datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

        #Me fijo que el saldo a comprar no pase al limite de la cuenta
        if (tipoCompra == "EN_CUOTAS" and monto > self.limite_cuotas) or (monto > self.limite_un_pago):
                #Rechazo transaccion
                print('El monto es mayor al permitido actual')
                comprar.setEstado("RECHAZADA")
        else:
            #Caso contrario, el estado pasa a aprobado
            comprar.setEstado("ACEPTADA")

        #Cargo la transaccion
        self.agregarTransaccion(comprar)  

    #Metodo para crear una chequera
    def agregarChequera(self):
        #Creo la transaccion
        agregarChequera = Transaccion("ALTA_CHEQUERA",None,None,None,datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

        #Chequeo que no supere la cantidad de chequeras maxima
        if not (len(self.chequera) < self.cant_chequera):
            print('Ya se tiene el maximo de chequeras')
            agregarChequera.setEstado("RECHAZADA")
        else:
            #Creo la chequera y la agrego
            agregarChequera.setEstado("APROBADA")
            chequeraNueva = Chequera(self.getTitular())
            self.chequera.append(chequeraNueva)

        #Cargo la transaccion
        self.agregarTransaccion(agregarChequera) 
    

    def compra_dolar(self, tipoMoneda, monto, cuenta):
        dolar = 970
        cuentaPesos = self.cuentas[self.cuenta_dolar(tipoMoneda, cuenta)]
        cuentaDolar = self.cuentas[self.cuenta_dolar("DOLAR", cuenta)]
        if tipoMoneda == "DOLAR":
            print("DEBE USAR UNA CUENTA EN PESOS")
        else:
            cantidadPesos = dolar * monto
            cuentaPesos.retirar_plata(cantidadPesos)
            cuentaDolar.ingresar_plata(monto)
            print("BIEN AHI TENES DOLARES!!")
            compraDolar = Transaccion("COMPRA_DOLAR",None,None,monto,datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            self.Transaccion.append(compraDolar)
    
    def venta_dolar(self, tipoMoneda, monto, cuenta):
        dolar = 970
        cuentaPesos = self.cuentas[self.cuenta_dolar(tipoMoneda, cuenta)]
        cuentaDolar = self.cuentas[self.cuenta_dolar("DOLAR", cuenta)]
        if tipoMoneda == "PESOS":
            print("DEBE USAR UNA CUENTA EN DOLARES")
        else:
            cantidadPesos = monto * dolar
            cuentaDolar.retirar_plata(monto)
            cuentaPesos.ingresar_plata(cantidadPesos)
            print("MAL AHI TENES PESOS!!")
            ventaDolar = Transaccion("VENTA_DOLAR",None,None,monto,datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            self.Transaccion.append(ventaDolar)

    def cuenta_dolar(self, moneda, cuenta):
        encontrado = False
        i = 0
        while not(encontrado) and i<len(self.cuentas):
            cuentaTipo =  self.cuentas[i].getTipoCuenta()
            cuentaMoneda = self.cuentas[i].getTipoMoneda()
            if cuentaTipo == cuenta and cuentaMoneda == moneda:
                encontrado = True
            else:
                i += 1
        return i
    
    def transferencia_enviada(self, cuentaDestino, cuentaOrigen, monto, tipoMoneda):
        cuentaTransferencia = self.cuentas[self.cuenta_dolar(tipoMoneda, cuentaOrigen)]
        saldoTransferComision = monto * self.comision_transferencia_saliente + monto
        if cuentaTransferencia.get_saldo() >= saldoTransferComision:
            cuentaTransferencia.retirar_plata(saldoTransferComision)
            cuentaDestino.ingresar_plata(saldoTransferComision)
            transferenciaEnviada = Transaccion("TRANSFERENCIA_ENVIADA_" + tipoMoneda ,self.cuenta_dolar(tipoMoneda, cuentaOrigen),None,monto,datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            self.Transaccion.append(transferenciaEnviada)
            print("TRANSFERENCIA EXITOSA")
        else:
            print("NO HAY FONDOS SUFICIENTES")
        
    def transferencia_recibida(self, cuentaOrigen, monto, tipoMoneda):
        cuentaTransferenciaRecibida = self.cuentas[self.cuenta_dolar(tipoMoneda, cuentaOrigen)]
        saldoTransferComision = monto * self.comision_transferencia_entrante + monto
        cuentaTransferenciaRecibida.ingresar_plata(saldoTransferComision)
        transferenciaRecibida = Transaccion("TRANSFERENCIA_RECIBIDA_" + tipoMoneda ,self.cuenta_dolar(tipoMoneda, cuentaOrigen),None,monto,datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        self.Transaccion.append(transferenciaRecibida)
        print("TRANSFERENCIA EXITOSA")


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


    # ------------ GETTERS -----------------

    #Todas las Transaccion hechas por el cliente
    def getTransaccion(self):
        return self.Transaccion
    
    #Cantidad de transsaciones hechas por el cliente
    def getCantTrasacciones(self):
        return len(self.Transaccion)
    
    #Get con todas las tarjetas
    def getTarjetas(self):
        text = ''
        for i in self.tarjetaS:
            text += str(i) + "\n"
        return text

    #Get titular (Combinacion nombre + apellido)
    def getTitular(self):
        return self.nombre + " " + self.apellido
    

# ---------------------------- SUBCLASES ----------------------------
#-------------------  Clases que heredan de Cliente -----------------

class Classic(Cliente):

    #Constructor
    def __init__(self, nombre, apellido, dni):
        super().__init__(nombre, apellido, dni,"CLASSIC")

        #------------- RESTRICCIONES -------------------
        self.cant_tarjetas_debito = 1
        self.cant_tarjetas_credito = 0
        self.cant_caja_ahorro = 2
        self.cant_retiros_sin_comisiones = 5
        self.limite_diario = 10000
        self.comision_transferencia_entrante = 0,5
        self.comision_transferencia_saliente = 0,1

        #Metodo para crear solo 1 caja ahorro

class Gold(Cliente):

    def __init__(self, nombre, apellido, dni):
        super().__init__(nombre, apellido, dni,"GOLD")

        #------------- RESTRICCIONES -------------------
        self.cant_tarjetas_debito = 1
        self.cant_tarjetas_credito = 5
        self.cant_caja_ahorro = 2
        self.cant_cuenta_corriente = 1 
        self.limite_un_pago = 150000
        self.limite_cuotas = 100000
        self.limite_diario = 20000
        self.comision_transferencia_entrante = 0,1
        self.comision_transferencia_saliente = 0,5
        self.cant_chequera = 1

class Black(Cliente):

     def __init__(self, nombre, apellido, dni):
        super().__init__(nombre, apellido, dni,"BLACK")

            #------------- RESTRICCIONES -------------------
        self.cant_tarjetas_debito = 5
        self.cant_tarjetas_credito = 10
        self.cant_caja_ahorro = 5
        self.cant_cuenta_corriente = 3
        self.limite_un_pago = 500000
        self.limite_cuotas = 600000
        self.limite_diario = 100000
        self.cant_chequera = 2



#Pruebas

nicolasGaston = Black('Nicolas','Gaston',29494777)
paco = Classic('Paco','Alcor',12345678)
valen = Gold('Valentino','Cambria',12345678)

#print(paco)
#print(valen)
#print(seba)

#nicolasGaston.agregarTransaccion(Transaccion("RETIRO_EFECTIVO_CAJERO_AUTOMATICO",190,9000,1000,"10/10/2022 16:00:55"))
#nicolasGaston.agregarTransaccion(Transaccion("COMPRA_EN_CUOTAS_TARJETA_CREDITO_VISA",None,9000,750000,"10/10/2022 16:14:35"))


#Test limites de tarjetas
#paco.agregarTarjeta("Debito","VISA")
#paco.agregarTarjeta("Credito","VISA")
#print(paco.getTarjetas())

#Test retirar efectivo
nicolasGaston.retiroEfectivo("CAJERO_AUTOMATICO",190,1000)
#nicolasGaston.retiroEfectivo("CAJERO_AUTOMATICO",190,9001)

#Test agregar tarjeta
#nicolasGaston.agregarTarjeta("Debito","VISA")

#Test Compra (en cuotas/1 pago)
nicolasGaston.compraTarjeta("En_cuotas","Credito",190,750000)

#Test chequera
#nicolasGaston.agregarChequera()

#Test cuenta
#nicolasGaston.agregarCuenta("CUENTA_CTE","PESOS")
paco.agregarCuenta("CUENTA_CTE","PESOS")
paco.agregarCuenta("CAJA_DE_AHORRO","PESOS")
paco.agregarCuenta("CUENTA_CTE","PESOS")
paco.agregarCuenta("CAJA_DE_AHORRO","PESOS")
paco.agregarCuenta("CAJA_DE_AHORRO","PESOS")

#Generar reporte
print(nicolasGaston.generar_reporte())
#print(paco.generar_reporte())