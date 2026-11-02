"""Interacción por terminal; la ingesta se ejecuta por separado."""

import asyncio

from rag import get_rag_response


async def main() -> None:
    query = input("Escribí tu pregunta: ").strip()
    if not query:
        print("Ingresá una pregunta para continuar.")
        return
    try:
        result = await get_rag_response(query)
    except Exception:
        print("No se pudo generar la respuesta. Revisá la configuración de Gemini e intentá nuevamente.")
        return

    print(f"\nRespuesta: {result.respuesta}")
    print("Fuentes:")
    for source in result.fuentes:
        print(f"- {source}")
    if not result.fuentes:
        print("- Sin fuentes")
    print(f"Fragmentos recuperados: {result.fragmentos_recuperados}")


if __name__ == "__main__":
    asyncio.run(main())
