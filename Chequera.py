class Chequera():
    idChequera = 1

    def __init__(self,titular) -> None:
        self.numeroChequera = self.idChequera
        Chequera.idChequera += 1

        self.titular = titular
        #self.saldo = saldo