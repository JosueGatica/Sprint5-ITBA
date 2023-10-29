from enum import Enum

class Cuenta:
    def __init__(self, tipo_cuenta, tipo_moneda):
        self.tipo_cuenta = tipo_cuenta
        self.tipo_moneda = tipo_moneda
        self.saldo = 0

class tipoCuentas(Enum):
    Caja_ahorro_pesos = "Caja de ahorro en peso"
    Caja_ahorro_dolares = "Caja de ahorro en dólares"
    Cuenta_corriente_pesos = "Cuenta Corriente en pesos"
    Cuenta_corriente_dolares = "Cuenta Corriente en dólares"
    Inversion = "Cuenta Inversión"