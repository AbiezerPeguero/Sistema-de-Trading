import config
from src.data_loader import DataLoader
from src.backtester import Backtester
from src.reporte import Reporte
from src.strategy_factory import crear_estrategia
from src.metrics import Metrics
from src.visualizacion import Visualizacion
import argparse
from src.optimizer import Optimizer
from src.strategies.sma_crossover import EstrategiaSmaCrossover


parser = argparse.ArgumentParser()
parser.add_argument("--ticker", type=str, default=None)
args = parser.parse_args()

# Cargando datos usando CSV_PATH desde config
if args.ticker:
    from src.data_fetcher import YahooFinanceFetcher
    fetcher = YahooFinanceFetcher(ticker=args.ticker, periodo="3mo")
    datos = fetcher.descargar()
else:
    cargar_datos = DataLoader(config.CSV_PATH)
    datos = cargar_datos.cargar()

# Creando estrategia con strategy_factory
estrategia = crear_estrategia()

# Creando backtester usando BALANCE_INICIAL
backtester = Backtester(estrategia, config.BALANCE_INICIAL)

# Ejecutando backtester
backtester.ejecutar(datos)

# Visualizando grafico
visualizar = Visualizacion(backtester.historial, datos, config.BALANCE_INICIAL)

# Llamando a grafico_curva_capital()
visualizar.grafico_curva_capital()

# Visualizando grafico
visualizar.grafico_histograma()

# Visualizando grafico
visualizar.grafico_precio_semanales()

# Visualizando grafico
visualizar.grafico_drawdown()


metrics = Metrics(backtester.historial)

metricas = metrics.resumen(config.BALANCE_INICIAL, backtester.balance)

# Creando un reporte
reporte = Reporte(backtester.historial, config.BALANCE_INICIAL, backtester.balance)

reporte.mostrar_resultados()

optimizer = Optimizer(
    estrategia_clase=EstrategiaSmaCrossover,
    datos=datos,
    balance_inicial=config.BALANCE_INICIAL,
    parametros={
        "periodo_corto": [2, 3, 5],
        "periodo_largo": [4, 5, 10]
    }
)

optimizer.optimizar()
