# core/seeder.py
import asyncio
import random
from sqlalchemy import insert
from core.database import async_session_maker
from models.product import Product

async def seed_products():
    """Inyecta registros de prueba en lotes utilizando Core DML para optimización de I/O."""
    async with async_session_maker() as session:
        print("Generando datos de prueba en memoria...")
        productos_lote = []
        
        for i in range(1, 10001):
            productos_lote.append({
                "name": f"Producto Inteligente {i}",
                "description": f"Descripción RAG simulada para el artículo {i}",
                "price": round(random.uniform(10.0, 999.99), 2),
                "stock": random.randint(0, 100),
                "embedding": [random.uniform(-1.0, 1.0) for _ in range(768)]
            })

        print("Iniciando inyección masiva en PostgreSQL...")
        await session.execute(insert(Product), productos_lote)
        await session.commit()
        
        print("Inyección completada exitosamente.")

if __name__ == "__main__":
    asyncio.run(seed_products())