from models.usuario import Usuario, Transaccion, session

# Crear un nuevo usuario
nuevo_usuario = Usuario(nombre="Juan", correo="juan@example.com", telegram_id=123456789)
session.add(nuevo_usuario)
session.commit()

# Crear una nueva transacción para el usuario
nueva_transaccion = Transaccion(tarjeta="Tarjeta1", tipo="egreso", monto=50.0, descripcion="Compra en tienda")
nuevo_usuario.transacciones.append(nueva_transaccion)
session.add(nueva_transaccion)
session.commit()
