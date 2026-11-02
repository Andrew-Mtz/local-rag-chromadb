"""Contratos de salida del modelo y de la aplicación."""

from pydantic import BaseModel, Field


class RespuestaLLM(BaseModel):
    respuesta: str = Field(description="Texto de la respuesta basado en el contexto.")


class RAGResponse(BaseModel):
    respuesta: str
    fuentes: list[str]
    fragmentos_recuperados: int = Field(ge=0)
