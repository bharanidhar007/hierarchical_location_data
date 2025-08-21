from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
from geoalchemy2 import Geography

revision = '0001_init'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")

    op.create_table('countries',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('code', sa.String(length=3), nullable=False, unique=True, index=True),
        sa.Column('name', sa.String(length=255), nullable=False, index=True),
        sa.Column('translations', JSONB, server_default=sa.text("'{}'::jsonb"), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
    )

    op.create_table('states',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('country_id', sa.BigInteger, sa.ForeignKey('countries.id', ondelete="CASCADE"), nullable=False, index=True),
        sa.Column('code', sa.String(length=10), nullable=True, index=True),
        sa.Column('name', sa.String(length=255), nullable=False, index=True),
        sa.Column('translations', JSONB, server_default=sa.text("'{}'::jsonb"), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
    )

    op.create_table('cities',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('state_id', sa.BigInteger, sa.ForeignKey('states.id', ondelete="CASCADE"), nullable=False, index=True),
        sa.Column('name', sa.String(length=255), nullable=False, index=True),
        sa.Column('code', sa.String(length=20), nullable=True, index=True),
        sa.Column('translations', JSONB, server_default=sa.text("'{}'::jsonb"), nullable=False),
        sa.Column('latitude', sa.Float, nullable=True),
        sa.Column('longitude', sa.Float, nullable=True),
        sa.Column('geom', Geography(geometry_type='POINT', srid=4326), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
    )

    op.create_table('towns',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('city_id', sa.BigInteger, sa.ForeignKey('cities.id', ondelete="CASCADE"), nullable=False, index=True),
        sa.Column('name', sa.String(length=255), nullable=False, index=True),
        sa.Column('code', sa.String(length=20), nullable=True, index=True),
        sa.Column('translations', JSONB, server_default=sa.text("'{}'::jsonb"), nullable=False),
        sa.Column('latitude', sa.Float, nullable=True),
        sa.Column('longitude', sa.Float, nullable=True),
        sa.Column('geom', Geography(geometry_type='POINT', srid=4326), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
    )

    op.create_index('ix_countries_name_trgm', 'countries', ['name'], postgresql_using='gin', postgresql_ops={'name': 'gin_trgm_ops'})
    op.create_index('ix_states_name_trgm', 'states', ['name'], postgresql_using='gin', postgresql_ops={'name': 'gin_trgm_ops'})
    op.create_index('ix_cities_name_trgm', 'cities', ['name'], postgresql_using='gin', postgresql_ops={'name': 'gin_trgm_ops'})
    op.create_index('ix_towns_name_trgm', 'towns', ['name'], postgresql_using='gin', postgresql_ops={'name': 'gin_trgm_ops'})

def downgrade():
    op.drop_index('ix_towns_name_trgm', table_name='towns')
    op.drop_index('ix_cities_name_trgm', table_name='cities')
    op.drop_index('ix_states_name_trgm', table_name='states')
    op.drop_index('ix_countries_name_trgm', table_name='countries')
    op.drop_table('towns')
    op.drop_table('cities')
    op.drop_table('states')
    op.drop_table('countries')
