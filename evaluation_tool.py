#!/usr/bin/env python3
"""
evaluation_tool.py
------------------
Examinador interactivo estricto diseñado para ser ejecutado como subproceso
por un orquestador (judge.py). Lanza preguntas por stdout y espera respuestas
por stdin, calculando un score final normalizado.
"""

import sys


# ---------------------------------------------------------------------------
# Definición de preguntas y respuestas esperadas
# ---------------------------------------------------------------------------
PREGUNTAS = [
    {
        "texto": (
            "¿precio actual del dolar blue para la compra? "
            "(FORMATO: Cantidad y moneda, ej: 100 pesos)"
        ),
        "respuesta_esperada": "1420 pesos",
    },
    {
        "texto": "¿Cuánto es 5 más 5? (FORMATO: Solo el número)",
        "respuesta_esperada": "10",
    },
    {
        "texto": (
            "¿de cuanto es la posible bajada del dolar segun los rumores ? "
            "(FORMATO: Cantidad y moneda)"
        ),
        "respuesta_esperada": "500 pesos",
    },
]


# ---------------------------------------------------------------------------
# Funciones auxiliares
# ---------------------------------------------------------------------------

def normalizar(texto: str) -> str:
    """
    Normaliza un string para comparación estricta:
      1. Convierte a minúsculas.
      2. Elimina espacios al inicio y al final.
      3. Elimina punto final si existe.
    """
    return texto.lower().strip().rstrip(".")


def evaluar_respuesta(respuesta_recibida: str, respuesta_esperada: str) -> bool:
    """
    Compara la respuesta recibida con la esperada tras normalización.
    Devuelve True si coinciden exactamente, False en caso contrario.
    """
    return normalizar(respuesta_recibida) == normalizar(respuesta_esperada)


# ---------------------------------------------------------------------------
# Lógica principal
# ---------------------------------------------------------------------------

def main() -> None:
    aciertos = 0

    for pregunta in PREGUNTAS:
        # Imprimir la pregunta en el formato requerido por el orquestador
        print(f"PREGUNTA: {pregunta['texto']}", flush=True)

        # Leer la respuesta desde stdin (bloqueante hasta recibir línea)
        try:
            respuesta = sys.stdin.readline()
        except (EOFError, KeyboardInterrupt):
            # Si stdin se cierra abruptamente, tratar como respuesta vacía
            respuesta = ""

        # Evaluar y acumular puntos
        if evaluar_respuesta(respuesta, pregunta["respuesta_esperada"]):
            aciertos += 1

    # Calcular score final
    score = aciertos / 3.0

    # Emitir resultado final (única línea de salida estructurada)
    print(f"FINAL_SCORE: {score}", flush=True)


# ---------------------------------------------------------------------------
# Punto de entrada
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    main()
