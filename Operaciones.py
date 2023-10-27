from enum import Enum

#Todos los estados posibles que pueden tener las operaciones 
class Operaciones(Enum):
    #Retiros
    RETIRO_EFECTIVO_CAJERO_AUTOMATICO = "RETIRO_EFECTIVO_CAJERO_AUTOMATICO"
    RETIRO_EFECTIVO_POR_CAJA = "RETIRO_EFECTIVO_POR_CAJA"

    #Compras
    COMPRA_EN_CUOTAS_TARJETA_CREDITO_VISA = "COMPRA_EN_CUOTAS_TARJETA_CREDITO_VISA"
    COMPRA_EN_CUOTAS_TARJETA_CREDITO_MASTER = "COMPRA_EN_CUOTAS_TARJETA_CREDITO_MASTER"
    COMPRA_EN_CUOTAS_TARJETA_CREDITO_AMEX = "COMPRA_EN_CUOTAS_TARJETA_CREDITO_AMEX"

    COMPRA_TARJETA_CREDITO_VISA = "COMPRA_TARJETA_CREDITO_VISA"
    COMPRA_TARJETA_CREDITO_MASTER = "COMPRA_TARJETA_CREDITO_MASTER"
    COMPRA_TARJETA_CREDITO_AMEX = "COMPRA_TARJETA_CREDITO_AMEX"

    #Altas
    ALTA_TARJETA_CREDITO_VISA = "ALTA_TARJETA_CREDITO_VISA"
    ALTA_TARJETA_CREDITO_MASTER = "ALTA_TARJETA_CREDITO_MASTER"
    ALTA_TARJETA_CREDITO_AMEX = "ALTA_TARJETA_CREDITO_AMEX"
    ALTA_TARJETA_DEBITO = "ALTA_TARJETA_DEBITO"
    ALTA_CHEQUERA = "ALTA_CHEQUERA"
    ALTA_CUENTA_CTE_PESOS = "ALTA_CUENTA_CTE_PESOS"
    ALTA_CUENTA_CTE_DOLARES = "ALTA_CUENTA_CTE_DOLARES"
    ALTA_CAJA_DE_AHORRO_PESOS = "ALTA_CAJA_DE_AHORRO_PESOS"
    ALTA_CAJA_DE_AHORRO_DOLARES = "ALTA_CAJA_DE_AHORRO_DOLARES"
    ALTA_CUENTA_DE_INVERSION = "ALTA_CUENTA_DE_INVERSION"

    #Compra-Venta dolar
    COMPRA_DOLAR = "COMPRA_DOLAR"
    VENTA_DOLAR = "VENTA_DOLAR"

    
    TRANSFERENCIA_ENVIADA_PESOS = "TRANSFERENCIA_ENVIADA_PESOS"
    TRANSFERENCIA_ENVIADA_DOLARES = "TRANSFERENCIA_ENVIADA_DOLARES"

    TRANSFERENCIA_RECIBIDA_PESOS = "TRANSFERENCIA_RECIBIDA_PESOS"
    TRANSFERENCIA_RECIBIDA_DOLARES = "TRANSFERENCIA_RECIBIDA_DOLARES"