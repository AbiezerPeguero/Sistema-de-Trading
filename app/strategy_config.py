"""Responsabilidad única: Saber qué parámetros configurables tiene cada estrategia y con qué valores mínimos, máximos y por defecto."""


class StrategyConfig:
    def __init__(self):
        self._config = {
            
        "Rsi": [
            {"nombre": "periodo",      # nombre exacto del kwarg que recibe la estrategia
            "tipo": "int",            # "int" o "float"
            "min": 5,
            "max": 30,
            "default": 14,
            "label": "Período RSI"}    # texto legible que verá el usuario en la UI
        ],
        
        "Bollinger": [
            {"nombre": "periodo",
            "tipo": "int",
            "min": 5,
            "max": 50,
            "default": 20,
            "label": "Periodo"},
            
            {"nombre": "desviaciones",
            "tipo": "float",
            "min": 1.0,
            "max": 3.0,
            "default": 2.0,
            "label": "desviacion"}
        ],
        
        "MediaMovil": [],
        
        "Breakout": [
            {"nombre": "umbral",
            "tipo": "float",
            "min": 50,
            "max": 250,
            "default": 160,
            "label": "Umbral"}
        ],        
        
        "SmaCrossover": [
            {"nombre": "periodo_corto",
            "tipo": "int",
            "min": 2,
            "max": 20,
            "default": 5,
            "label": "Periodo Corto"},
            
            {"nombre": "periodo_largo",
            "tipo": "int",
            "min": 10,
            "max": 200,
            "default": 20,
            "label": "Periodo Largo"}
        ],
        
        "MACD": [
            {"nombre": "periodo_corto",
            "tipo": "int",
            "min": 5,
            "max": 20,
            "default": 12,
            "label": "Periodo Corto"},
            
            {"nombre": "periodo_largo",
            "tipo": "int",
            "min": 10,
            "max": 50,
            "default": 26,
            "label": "Periodo Largo"},
            
            {"nombre": "periodo_signal",
            "tipo": "int",
            "min": 3,
            "max": 15,
            "default": 9,
            "label": "Periodo Señal"}
        ]
    }
    
    # Devuelve la lista de parametros de cada estrategia
    def obtener_params(self, nombre_estrategia):
        if not nombre_estrategia in self._config:
            raise ValueError(f"Estrategia {nombre_estrategia} no encontrada")
        return self._config[nombre_estrategia]
        
    # Devuelve la lista de claves del diccionario.
    def nombres_estrategias(self):
        return list(self._config.keys())
