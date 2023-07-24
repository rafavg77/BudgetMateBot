from models.usuario import Usuario, session
from telebot import types
from datetime import datetime

class PerfilGasto:
    def __init__(self, bot):
        self.bot = bot

    def crear_perfil(self, message):
        # Obtener el chat_id del usuario
        chat_id = message.chat.id

        # Habilitar el modo de guardar los controladores de pasos siguientes para esta conversación
        self.bot.enable_save_next_step_handlers()

        # Pedir el nombre al usuario
        self.bot.send_message(chat_id, "¡Hola! Para crear tu perfil, primero necesito saber tu nombre.")
        self.bot.register_next_step_handler(message, self.pedir_correo)

    def pedir_correo(self, message):
        # Obtener el chat_id del usuario
        chat_id = message.chat.id

        # Obtener el nombre del mensaje anterior
        nombre = message.text

        # Pedir el correo al usuario
        self.bot.send_message(chat_id, f"¡Hola, {nombre}! Ahora necesito tu correo electrónico.")
        self.bot.register_next_step_handler(message, self.guardar_perfil, nombre=nombre)

    def guardar_perfil(self, message, nombre):
        # Obtener el chat_id y correo del usuario
        chat_id = message.chat.id
        correo = message.text

        # Obtener la fecha de creación
        fecha_creacion = datetime.utcnow()

        # Crear el perfil del usuario y guardarlo en la base de datos
        nuevo_usuario = Usuario(nombre=nombre, correo=correo, telegram_id=chat_id, status=True, fecha_creacion=fecha_creacion)
        session.add(nuevo_usuario)
        session.commit()

        # Deshabilitar el modo de guardar los controladores de pasos siguientes para esta conversación
        self.bot.disable_save_next_step_handlers()

        # Enviar un mensaje de confirmación al usuario
        self.bot.send_message(chat_id, "¡Perfil creado con éxito! Ahora estás listo para comenzar a registrar tus gastos.")

    def consultar_perfil(self, message):
        # Obtener el chat_id del usuario
        chat_id = message.chat.id

        # Obtener el telegram_id del usuario
        telegram_id = message.from_user.id

        # Consultar el perfil del usuario en base a su telegram_id
        usuario = session.query(Usuario).filter_by(telegram_id=telegram_id).first()

        if usuario:
            # Si se encontró el perfil, mostrar la información al usuario
            respuesta = f"Información del perfil:\n\n" \
                        f"Nombre: {usuario.nombre}\n" \
                        f"Correo: {usuario.correo}\n" \
                        f"Fecha de Creación: {usuario.fecha_creacion}"
        else:
            # Si no se encontró el perfil, informar al usuario
            respuesta = "No se encontró un perfil asociado a tu Telegram ID."

        # Enviar la respuesta al usuario
        self.bot.send_message(chat_id, respuesta)    
