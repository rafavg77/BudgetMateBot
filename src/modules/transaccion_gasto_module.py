from models.usuario import Usuario, Transaccion, session
from telebot import types
from datetime import datetime

class TransaccionGasto:
    def __init__(self, bot):
        self.bot = bot

    def registrar_transaccion(self, message):
        # Obtener el chat_id del usuario
        chat_id = message.chat.id

        # Habilitar el modo de guardar los controladores de pasos siguientes para esta conversación
        self.bot.enable_save_next_step_handlers()

        # Pedir el nombre de la tarjeta al usuario
        self.bot.send_message(chat_id, "Para registrar una transacción, primero necesito el nombre de la tarjeta.")
        self.bot.register_next_step_handler(message, self.pedir_tipo_tarjeta)

    def pedir_tipo_tarjeta(self, message):
        # Obtener el chat_id del usuario
        chat_id = message.chat.id

        # Obtener el nombre de la tarjeta del mensaje anterior
        nombre_tarjeta = message.text

        # Pedir el tipo de transacción al usuario (Ingreso o Egreso)
        self.bot.send_message(chat_id, "¿La transacción es un Ingreso o un Egreso? Por favor, responde con 'Ingreso' o 'Egreso'.")
        self.bot.register_next_step_handler(message, self.pedir_monto_tarjeta, nombre_tarjeta=nombre_tarjeta)

    def pedir_monto_tarjeta(self, message, nombre_tarjeta):
        # Obtener el chat_id del usuario
        chat_id = message.chat.id

        # Obtener el tipo de transacción del mensaje anterior
        tipo_transaccion = message.text.lower()

        # Verificar que el tipo de transacción sea válido (Ingreso o Egreso)
        if tipo_transaccion not in ['ingreso', 'egreso']:
            self.bot.send_message(chat_id, "Tipo de transacción inválido. Por favor, responde con 'Ingreso' o 'Egreso'.")
            self.bot.register_next_step_handler(message, self.pedir_monto_tarjeta, nombre_tarjeta=nombre_tarjeta)
            return

        # Pedir el monto de la transacción al usuario
        self.bot.send_message(chat_id, "Por favor, ingresa el monto de la transacción.")
        self.bot.register_next_step_handler(message, self.pedir_descripcion_tarjeta, nombre_tarjeta=nombre_tarjeta, tipo_transaccion=tipo_transaccion)

    def pedir_descripcion_tarjeta(self, message, nombre_tarjeta, tipo_transaccion):
        # Obtener el chat_id del usuario
        chat_id = message.chat.id

        # Obtener el monto de la transacción del mensaje anterior
        monto_transaccion = message.text

        # Validar que el monto sea un número válido
        try:
            monto_transaccion = float(monto_transaccion)
        except ValueError:
            self.bot.send_message(chat_id, "Monto inválido. Por favor, ingresa un número válido.")
            self.bot.register_next_step_handler(message, self.pedir_descripcion_tarjeta, nombre_tarjeta=nombre_tarjeta, tipo_transaccion=tipo_transaccion)
            return

        # Pedir la descripción de la transacción al usuario
        self.bot.send_message(chat_id, "Por favor, ingresa una descripción de la transacción.")
        self.bot.register_next_step_handler(message, self.guardar_transaccion, nombre_tarjeta=nombre_tarjeta, tipo_transaccion=tipo_transaccion, monto_transaccion=monto_transaccion)

    def guardar_transaccion(self, message, nombre_tarjeta, tipo_transaccion, monto_transaccion):
        # Obtener el chat_id del usuario
        chat_id = message.chat.id

        # Obtener la descripción de la transacción del mensaje anterior
        descripcion_transaccion = message.text

        # Obtener la fecha de creación
        fecha_creacion = datetime.utcnow()

        telegram_id = message.from_user.id

        # Consultar el perfil del usuario en base a su telegram_id
        usuario = session.query(Usuario).filter_by(telegram_id=telegram_id).first()

        # Crear la transacción y guardarla en la base de datos
        nueva_transaccion = Transaccion(tarjeta=nombre_tarjeta, tipo=tipo_transaccion, monto=monto_transaccion,
                                        descripcion=descripcion_transaccion, status=True, fecha_creacion=fecha_creacion)
        usuario.transacciones.append(nueva_transaccion)
        session.add(nueva_transaccion)
        session.commit()
    
        # Deshabilitar el modo de guardar los controladores de pasos siguientes para esta conversación
        self.bot.disable_save_next_step_handlers()
        print(nombre_tarjeta, tipo_transaccion, monto_transaccion,
                                        descripcion_transaccion, True, fecha_creacion)

        # Enviar un mensaje de confirmación al usuario
        self.bot.send_message(chat_id, "Transacción registrada con éxito.")
    
    def consultar_transacciones(self, message):
        # Obtener el chat_id del usuario

        telegram_id = message.from_user.id

        # Consultar el perfil del usuario en base a su telegram_id
        usuario = session.query(Usuario).filter_by(telegram_id=telegram_id).first()

        # Verificar si el usuario existe en la base de datos
        if usuario:
            # Obtener el usuario_id
            usuario_id = usuario.usuario_id

            # Consultar todas las transacciones del usuario
            transacciones = session.query(Transaccion).filter_by(usuario_id=usuario_id).all()

            # Verificar si el usuario tiene transacciones registradas
            if not transacciones:
                self.bot.send_message(telegram_id, "Aún no tienes transacciones registradas.")
            else:
                # Enviar las transacciones al usuario
                mensaje_transacciones = "Tus transacciones:\n"
                for transaccion in transacciones:
                    mensaje_transacciones += f"- {transaccion.tarjeta} - {transaccion.tipo} - ${transaccion.monto} - {transaccion.descripcion} \n"

                self.bot.send_message(telegram_id, mensaje_transacciones)

        else:
            # Enviar un mensaje de que primero debe crear un perfil
            self.bot.send_message(telegram_id, "Para consultar tus transacciones, primero debes crear tu perfil.")

