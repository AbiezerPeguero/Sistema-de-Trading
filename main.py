from SRC.data_loader import DataLoader
from SRC.estrategia import EstrategiaMediaMovil
from SRC.backtester import Backtester
from SRC.reporte import Reporte


# Creando un DataLounder con la ruta del csv y llamando a cargar
cargar_los_datos = DataLoader("Backtesting/Data/precios.csv")
datos = cargar_los_datos.cargar()

# Creando la estrategia 
estrategia = EstrategiaMediaMovil()

# Creando un backtester con la estrategia proporcionada y un balance inicial
backtester = Backtester(estrategia, 10000)

# Ejecutando el backtentig
backtester.ejecutar(datos)

# Creando un reporte
reporte = Reporte(backtester.historial, 10000, backtester.balance)


reporte.mostrar_resultados()

