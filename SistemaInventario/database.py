
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float
)

from sqlalchemy.orm import declarative_base, sessionmaker


# CONEXION CON MYSQL
DATABASE_URL = (
    "mysql+pymysql://root:Santiago.12@localhost:3306/inventario"
)

engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True
)

Base = declarative_base()

SessionLocal = sessionmaker(
    bind=engine
)


# TABLA DE PRODUCTOS
class ProductoDB(Base):

    __tablename__ = "productos"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    nombre = Column(
        String(100),
        nullable=False
    )

    precio = Column(
        Float,
        nullable=False
    )

    stock = Column(
        Integer,
        nullable=False
    )

    categoria = Column(
        String(50),
        nullable=False
    )


# TABLA DE MOVIMIENTOS
class MovimientoDB(Base):

    __tablename__ = "movimientos"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    producto = Column(
        String(100),
        nullable=False
    )

    tipo = Column(
        String(20),
        nullable=False
    )

    cantidad = Column(
        Integer,
        nullable=False
    )

    fecha = Column(
        String(30),
        nullable=False
    )


# CREAR LAS TABLAS SI NO EXISTEN
Base.metadata.create_all(engine)
