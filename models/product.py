from typing import List, Optional
from pgvector.sqlalchemy import Vector
from sqlalchemy import String, Text, Numeric, Integer
from sqlalchemy.orm import Mapped, mapped_column

# Importación relativa a la carpeta raíz de tu proyecto
from core.database import Base

class Product(Base):
    __tablename__ = "products"

    # Nota: Se corrigió primary_level=True (que no existe) por primary_key=True
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    # Campo vectorial para búsqueda semántica RAG (768 dimensiones)
    embedding: Mapped[Optional[List[float]]] = mapped_column(Vector(768), nullable=True)