from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

# Crear la instancia de la base de datos
Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'

    usuario_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(100), nullable=False)
    telegram_id = Column(Integer, nullable=False, unique=True)
    status = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    # Relación hacia el modelo Transaccion
    transacciones = relationship("Transaccion", back_populates="usuario")

class Transaccion(Base):
    __tablename__ = 'transacciones'

    transaccion_id = Column(Integer, primary_key=True, autoincrement=True)
    tarjeta = Column(String(100))
    tipo = Column(String(10), nullable=False)  # Puede ser "ingreso" o "egreso"
    monto = Column(Float, nullable=False)
    descripcion = Column(String(200))
    status = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    # Relación hacia el modelo Usuario
    usuario_id = Column(Integer, ForeignKey('usuarios.usuario_id'))
    usuario = relationship("Usuario", back_populates="transacciones")

# Configurar la conexión a la base de datos
# Aquí debes reemplazar 'nombre_de_bd' por el nombre de tu base de datos y 'usuario:contraseña' con tus credenciales.
engine = create_engine('sqlite:///nombre_de_bd.db')
Base.metadata.create_all(engine)

# Crear una sesión para interactuar con la base de datos
Session = sessionmaker(bind=engine)
session = Session()
