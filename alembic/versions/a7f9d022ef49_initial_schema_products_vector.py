"""initial_schema_products_vector

Revision ID: a7f9d022ef49
Revises: 
Create Date: 2026-09-10 00:43:29.192459
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import pgvector.sqlalchemy  # Importe obligatorio para el tipo Vector

# revision identifiers, used by Alembic.
revision: str = 'a7f9d022ef49'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Activación de la extensión para Búsqueda Semántica
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    # 2. Creación limpia y desde cero de la tabla products
    op.create_table('products',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('stock', sa.Integer(), nullable=False),
        sa.Column('embedding', pgvector.sqlalchemy.Vector(dim=768), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 3. Índice estándar para acelerar búsquedas exactas por nombre
    op.create_index(op.f('ix_products_name'), 'products', ['name'], unique=False)


def downgrade() -> None:
    # Reversión limpia en caso de Rollback
    op.drop_index(op.f('ix_products_name'), table_name='products')
    op.drop_table('products')
    op.execute("DROP EXTENSION IF EXISTS vector;")