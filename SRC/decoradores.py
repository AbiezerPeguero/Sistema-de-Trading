import time

# Medir cuántos segundos tarda en ejecutarse cualquier función a la que se le aplique.
def medir_tiempo(funcion):
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = funcion(*args, **kwargs)
        fin = time.time()
        tiempo_ejecucion = round(fin - inicio, 4)
        print(f"La funcion tardó {tiempo_ejecucion} segundos")
        return resultado
    return wrapper

# Imprimir que la operacion comenzo y termino
def log_operacion(funcion):
    def operacion(*args, **kwargs):
        print("La operacion comenzo")
        resultado = funcion(*args, **kwargs)
        print("La operacion finalizo")
        return resultado
    return operacion

# Validar datos de lista, si esta vacia, mensaje de error
def validar_lista(funcion):
    def validar(lista):
        if not lista:
            print("La lista no puede estar vacia")
        else:
            return funcion(lista)
    return validar