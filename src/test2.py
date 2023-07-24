from models.usuario import Usuario, Tarjeta, Transaccion, session

"""
# Dar de alta un usuario
nuevo_usuario = Usuario(nombre='Marco', correo='marco@example.com', telegram_id=123456789)
session.add(nuevo_usuario)
session.commit()

# Dar de alta una tarjeta para el usuario
nueva_tarjeta = Tarjeta(nombre_tarjeta='Tarjeta Visa', descripcion='Tarjeta de crédito')
nuevo_usuario.tarjetas.append(nueva_tarjeta)
session.add(nueva_tarjeta)
session.commit()
"""

# Dar de alta una transacción para la tarjeta y el usuario
nueva_transaccion = Transaccion(tipo='Ingreso', monto=1000, descripcion='Pago mensual',usuario_id=1,tarjeta_id=1)
#nueva_tarjeta.transacciones(nueva_transaccion)
session.add(nueva_transaccion)
session.commit()

# Cerrar la sesión
session.close()

print("Usuario, tarjeta y transacción registrados exitosamente.")