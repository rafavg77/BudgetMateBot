from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    usuario_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    correo = Column(String(100), nullable=False)
    telegram_id = Column(Integer, nullable=False, unique=True)
    status = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, server_default=func.now())

    tarjetas = relationship('Tarjeta', back_populates='usuario')
    transacciones = relationship('Transaccion', back_populates='usuario')

class Tarjeta(Base):
    __tablename__ = 'tarjetas'
    tarjeta_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_tarjeta = Column(String(50), nullable=False)
    descripcion = Column(String(100))
    status = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, server_default=func.now())

    usuario_id = Column(Integer, ForeignKey('usuarios.usuario_id'))
    usuario = relationship('Usuario', back_populates='tarjetas')
    transacciones = relationship('Transaccion', back_populates='tarjeta')

class Transaccion(Base):
    __tablename__ = 'transacciones'
    transaccion_id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String(10), nullable=False)
    monto = Column(Integer, nullable=False)
    descripcion = Column(String(100))
    status = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, server_default=func.now())

    usuario_id = Column(Integer, ForeignKey('usuarios.usuario_id'))
    usuario = relationship('Usuario', back_populates='transacciones')

    tarjeta_id = Column(Integer, ForeignKey('tarjetas.tarjeta_id'))
    tarjeta = relationship('Tarjeta', back_populates='transacciones')


# Configurar la conexión a la base de datos
# Aquí debes reemplazar 'nombre_de_bd' por el nombre de tu base de datos y 'usuario:contraseña' con tus credenciales.
engine = create_engine('sqlite:///nombre_de_bd.db')
Base.metadata.create_all(engine)

# Crear una sesión para interactuar con la base de datos
Session = sessionmaker(bind=engine)
session = Session()
