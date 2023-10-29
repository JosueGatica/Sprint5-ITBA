class Transacciones():
    
    #Constructor
    def __init__(self,tipo,cuentaNumero,permitidoActualParaTransaccion,
                    monto, fecha,numero):
        self.estado = "Pendiente"
        self.tipo = tipo
        self.cuentaNumero = cuentaNumero
        self.permitidoActualParaTransaccion = permitidoActualParaTransaccion
        self.monto = monto 
        self.fecha = fecha
        self.numero = numero

    #FALTA LOGICA DE TRANSACCIONES PARA CONTROL DE ESTADOS