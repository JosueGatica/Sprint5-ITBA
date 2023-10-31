class Transaccion():
    
    #Constructor
    def __init__(self,tipo,cuentaNumero,permitidoActualParaTransaccion,
                    monto, fecha):
        self.estado = "PENDIENTE"
        self.tipo = tipo
        self.cuentaNumero = cuentaNumero
        self.permitidoActualParaTransaccion = permitidoActualParaTransaccion
        self.monto = monto 
        self.fecha = fecha

    def setEstado(self,estado):
        self.estado = estado

    def setMonto(self,monto):
        self.monto = monto