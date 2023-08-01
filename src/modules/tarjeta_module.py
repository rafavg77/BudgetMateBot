from models.usuario import Usuario, Tarjeta , session
from telebot import types
from datetime import datetime

class TarjetaGasto:
    def __init__(self, bot):
        self.bot = bot

    def crear_tarjeta(self, message):
        chat_id = message.chat.id

        # Habilitar el modo de guardar los controladores de pasos siguientes para esta conversación
        self.bot.enable_save_next_step_handlers()

        # Pedir el nombre al usuario
        self.bot.send_message(chat_id, "¡Hola! Para crear una tarjeta, primero necesito saber tu nombre que tendrá la tarjeta.")
        self.bot.register_next_step_handler(message, self.pedir_descripcion_tarjeta)

    def pedir_descripcion_tarjeta(self, message):
        # Obtener el chat_id del usuario
        chat_id = message.chat.id

        # Obtener el nombre del mensaje anterior
        nombre_tarjeta = message.text

        # Pedir el correo al usuario
        self.bot.send_message(chat_id, f"Por favor dame una descripción para la tarjeta  {nombre_tarjeta}, puede ser el nombre del banco y si es de debito o crédito.")
        self.bot.register_next_step_handler(message, self.guardar_tarjeta, nombre_tarjeta=nombre_tarjeta)

    def guardar_tarjeta(self, message, nombre_tarjeta):
        # Obtener el chat_id y correo del usuario
        chat_id = message.chat.id
        descripcion = message.text

        # Obtener la fecha de creación
        #fecha_creacion = datetime.utcnow()

        usuario = session.query(Usuario).filter_by(telegram_id=chat_id).first()
        nueva_tarjeta = Tarjeta(nombre_tarjeta=nombre_tarjeta, descripcion=descripcion)
        usuario.tarjetas.append(nueva_tarjeta)
        session.add(nueva_tarjeta)
        session.commit()

        # Deshabilitar el modo de guardar los controladores de pasos siguientes para esta conversación
        self.bot.disable_save_next_step_handlers()

        # Enviar un mensaje de confirmación al usuario
        self.bot.send_message(chat_id, "¡Tarjeta creada con éxito! Ahora estás listo para comenzar a registrar tus Trasnsacciones para esta tarjeta. \n/consultar_tarjetas")

    def consultar_tarjetas(self, message):
        # Obtener el chat_id del usuario
        chat_id = message.chat.id

        # Obtener el telegram_id del usuario
        telegram_id = message.from_user.id

        # Consultar el perfil del usuario en base a su telegram_id
        usuario = session.query(Usuario).filter_by(telegram_id=telegram_id).first()
        tarjetas = session.query(Tarjeta).filter_by(usuario_id=usuario.usuario_id).all()
        if tarjetas:
            if not tarjetas:
                self.bot.send_message(telegram_id, "Aún no tienes tarjetas registradas.")
            else:
                mensaje_tarjetas = "Tus tarjetas son: \n"
                for tarjeta in tarjetas:
                    mensaje_tarjetas += f"- {tarjeta.nombre_tarjeta} - {tarjeta.descripcion} \n"
                self.bot.send_message(telegram_id, mensaje_tarjetas)
        else:
            self.bot.send_message(telegram_id, "Para consultar tus tarjetas, primero debes crear tus tarjetas en /registrar_tarjeta.")

    def register_tarjeta_commands(self, bot):
        bot.message_handler(commands=['crear_tarjeta'])(self.crear_tarjeta)
        bot.message_handler(commands=['consultar_tarjetas'])(self.consultar_tarjetas)