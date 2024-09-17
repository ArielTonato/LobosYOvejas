class Estado:
    def __init__(self, estado_actual, sucesores):
        self.estado_actual = estado_actual
        self.sucesores = sucesores

    @property
    def Sucesores(self):
        return self.sucesores