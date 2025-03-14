from typing import Optional
from pydantic import BaseModel

class Aranhaverso(BaseModel):
    id: Optional[int] = None
    nome: Optional[str] = None
    idade: Optional[int] = None
    cores_uniforme: Optional[str] = None
    poderes: Optional[str] = None
    personalidade: Optional[str] = None
    universo: Optional[str] = None
    foto: Optional[str] = None
    