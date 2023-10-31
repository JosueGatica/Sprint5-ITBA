from enum import Enum

class Cuenta:
    def __init__(self, tipo_cuenta, tipo_moneda):
        self.tipo_cuenta = tipo_cuenta
        self.tipo_moneda = tipo_moneda
        self.saldo = 10000 #Default
        self.esInversion()

    def getTipoCuenta(self):
        return self.tipo_cuenta
    
    def getTipoMoneda(self):
        return self.tipo_moneda
    
    def retirar_plata(self, monto):
        if self.saldo >= monto:
            self.saldo -= monto
        else:
            print("MONTO INSUFICIENTE")

    def puedeRetirar(self, monto):
        return self.saldo >= monto

    def ingresar_plata(self,monto):
        self.saldo += monto
        return self.saldo
    
    def get_saldo(self):
        return self.saldo
    
    def get_plazo_fijo(self):
        return self.plazo_fijo
    
    def esInversion(self):
        if self.tipo_cuenta == "INVERSION":
            self.plazo_fijo = 5000 #Default para test
            
"""
class tipoCuentas(Enum):
    Caja_ahorro_pesos = "Caja de ahorro en peso"
    Caja_ahorro_dolares = "Caja de ahorro en dólares"
    Cuenta_corriente_pesos = "Cuenta Corriente en pesos"
    Cuenta_corriente_dolares = "Cuenta Corriente en dólares"
    Inversion = "Cuenta Inversión"""