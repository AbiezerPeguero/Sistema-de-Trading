from abc import ABC, abstractmethod

# Clase base abstracta. Define el contrato que todas las estrategias deben cumplir.
# No se puede instanciar directamente, solo sirve como plantilla.
class Estrategia(ABC):
    @abstractmethod
    def generar_senal(self, dato):
        # Recibe un diccionario con los datos de un día.
        # Debe devolver "comprar", "vender" o None.
        # Cada estrategia hija implementa su propia lógica.
        pass