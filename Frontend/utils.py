from bcchapi import Siete

usuario = "tomasdubstep31@gmail.com"
token = "Tomas210059970"

def obtener_valor_dolar():
    try:
        siete = Siete(usuario, token)
        df = siete.cuadro(series=["F073.TCO.PRE.Z.D"], desde="2024-01-01", hasta="2024-12-31")
        valor_dolar = df.iloc[-1, 0]  # Primer valor de la última fila, usando acceso por posición
        return valor_dolar
    except Exception as e:
        print("Error al obtener el valor del dólar:", e)
        return None

# Bloque de prueba (puedes dejarlo o quitarlo según prefieras)
if __name__ == "__main__":
    valor_dolar = obtener_valor_dolar()
    print("El valor del dólar es:", valor_dolar)