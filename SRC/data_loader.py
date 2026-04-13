"""Responsabilidad única: Cargar el CSV y entregarlo como lista de diccionarios. Nada más."""
import csv

class DataLoader:
    # Recibe la ruta del archivo CSV al momento de crear el objeto.
    # Si la ruta está vacía, no tiene sentido continuar, lanzamos error inmediatamente.
    def __init__(self, ruta):
        if not ruta:
            raise ValueError("La ruta del archivo CSV no puede estar vacía.")
        self.ruta = ruta

    # Abrir el archivo CSV, lee cada fila y la convierte en un diccionario con las claves fecha, precio_cierre y volumen.
    # Devuelve una lista con todos esos diccionarios. Los valores numéricos deben quedar como float, no como texto.
    def cargar(self):
        # Abrimos el archivo CSV con newline='' para evitar problemas
        # con saltos de línea en diferentes sistemas operativos.
        with open(self.ruta, newline='') as csvfile:
            # DictReader lee cada fila y la convierte automáticamente en un diccionario
            # usando la primera fila del CSV (el encabezado) como claves.
            lector = csv.DictReader(csvfile)
            datos = [] # Lista donde acumularemos todas las filas procesadas.
            for fila in lector:
                # Cada fila llega como texto. Convertimos los valores numéricos a float
                # porque más adelante el Backtester necesita operar matemáticamente con ellos.
                # fecha se queda como texto porque solo se usa para identificar el día.
                datos.append({
                    "fecha": fila["fecha"],
                    "precio_cierre": float(fila["precio_cierre"]),
                    "volumen": float(fila["volumen"]),
                })
            # Validamos después de llenar la lista, no durante.
            # Si validáramos dentro del for, siempre estaría vacía en la primera iteración.
            if not datos:
                print("La lista no puede estar vacia")
            else:
                return datos # Devolvemos la lista completa solo si tiene datos.