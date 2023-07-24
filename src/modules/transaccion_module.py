from models.usuario import Usuario, Tarjeta, Transaccion, session
from telebot import types
#from datetime import datetime

class TransaccionGasto:
    def __init__(self, bot):
        self.bot = bot

    def registrar_transaccion(self, message):
        # Obtener el chat_id del usuario
        chat_id = message.chat.id

        # Habilitar el modo de guardar los controladores de pasos siguientes para esta conversación
        self.bot.enable_save_next_step_handlers()

        usuario = session.query(Usuario).filter_by(telegram_id=chat_id).first()
        tarjetas = session.query(Tarjeta).filter_by(usuario_id=usuario.usuario_id).all()
        if usuario:
            if tarjetas:
                if not tarjetas:
                    self.bot.disable_save_next_step_handlers()
                    self.bot.send_message(chat_id, "Aún no tienes tarjetas registradas /registrar_tarjeta.")
                else:
                    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                    #mensaje_tarjetas = "Tus tarjetas son: \n"
                    for tarjeta in tarjetas:
                    #    mensaje_tarjetas += f"- {tarjeta.nombre_tarjeta}\n"
                        markup.add(tarjeta.nombre_tarjeta)
                    
                    msg = self.bot.send_message(chat_id, "Selecciona la tarjeta ", reply_markup=markup)
                    self.bot.register_next_step_handler(msg, self.tipo_gasto)
            else:
                self.bot.disable_save_next_step_handlers()
                self.bot.send_message(chat_id, "NO tienes tarjetas registradas /registrar_tarjeta.")
        else:
            self.bot.disable_save_next_step_handlers()
            self.bot.send_message(chat_id, "No tienes un perfil registrado, para registar utiliza /crearperfil.")

    def tipo_gasto(self, message):
        # Obtener el chat_id del usuario
        chat_id = message.chat.id

        # Obtener el nombre de la tarjeta del mensaje anterior
        nombre_tarjeta = message.text

        # Pedir el tipo de transacción al usuario (Ingreso o Egreso)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Ingreso','Egreso')
        tipo_transaccion = self.bot.send_message(chat_id, "Selecciona el tipo de gasto.",reply_markup=markup)
        self.bot.register_next_step_handler(message, self.pedir_monto_transaccion, nombre_tarjeta=nombre_tarjeta)

    def pedir_monto_transaccion(self, message, nombre_tarjeta):
        # Obtener el chat_id del usuario
        chat_id = message.chat.id
        tipo_transaccion = message.text
        nombre_tarjeta = nombre_tarjeta
        print(tipo_transaccion, nombre_tarjeta)

        self.bot.send_message(chat_id, "Por favor, ingresa el monto de la transacción.")
        self.bot.register_next_step_handler(message, self.pedir_descripcion_transaccion, nombre_tarjeta=nombre_tarjeta, tipo_transaccion=tipo_transaccion)
        

    def pedir_descripcion_transaccion(self, message, nombre_tarjeta, tipo_transaccion):
        # Obtener el chat_id del usuario
        chat_id = message.chat.id

        # Obtener el monto de la transacción del mensaje anterior
        monto_transaccion = message.text

        # Validar que el monto sea un número válido
        try:
            monto_transaccion = float(monto_transaccion)
        except ValueError:
            self.bot.send_message(chat_id, "Monto inválido. Por favor, ingresa un número válido.")
            self.bot.register_next_step_handler(message, self.pedir_monto_transaccion, nombre_tarjeta=nombre_tarjeta, tipo_transaccion=tipo_transaccion)
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
        #fecha_creacion = datetime.utcnow()

        telegram_id = message.from_user.id

        # Consultar el perfil del usuario en base a su telegram_id
        usuario = session.query(Usuario).filter_by(telegram_id=telegram_id).first()
        #tarjetas = session.query(Tarjeta).filter_by(nombre_tarjeta=nombre_tarjeta).first()
        tarjeta = session.query(Tarjeta).filter(
            Tarjeta.nombre_tarjeta == nombre_tarjeta,
            Tarjeta.usuario_id == usuario.usuario_id
        ).first()

        nueva_transaccion = Transaccion(tipo=tipo_transaccion, monto=monto_transaccion, descripcion=descripcion_transaccion,usuario_id=usuario.usuario_id,tarjeta_id=tarjeta.tarjeta_id)
        session.add(nueva_transaccion)
        session.commit()

        # Cerrar la sesión
        session.close()


    
        # Deshabilitar el modo de guardar los controladores de pasos siguientes para esta conversación
        self.bot.disable_save_next_step_handlers()
        
        # Enviar un mensaje de confirmación al usuario
        self.bot.send_message(chat_id, "Transacción registrada con éxito.")
    
    def consultar_transacciones_tarjetas(self, message):
        # Obtener el chat_id del usuario
        print("consultar_transacciones_tarjetas")
        chat_id = message.chat.id

        # Habilitar el modo de guardar los controladores de pasos siguientes para esta conversación
        self.bot.enable_save_next_step_handlers()

        usuario = session.query(Usuario).filter_by(telegram_id=chat_id).first()
        tarjetas = session.query(Tarjeta).filter_by(usuario_id=usuario.usuario_id).all()
        if usuario:
            if tarjetas:
                if not tarjetas:
                    self.bot.disable_save_next_step_handlers()
                    self.bot.send_message(chat_id, "Aún no tienes tarjetas registradas /registrar_tarjeta.")
                else:
                    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                    #mensaje_tarjetas = "Tus tarjetas son: \n"
                    for tarjeta in tarjetas:
                    #    mensaje_tarjetas += f"- {tarjeta.nombre_tarjeta}\n"
                        markup.add(tarjeta.nombre_tarjeta)
                    
                    msg = self.bot.send_message(chat_id, "Selecciona la tarjeta ", reply_markup=markup)
                    self.bot.register_next_step_handler(msg, self.consultar_transacciones)
            else:
                self.bot.disable_save_next_step_handlers()
                self.bot.send_message(chat_id, "NO tienes tarjetas registradas /registrar_tarjeta.")
        else:
            self.bot.disable_save_next_step_handlers()
            self.bot.send_message(chat_id, "No tienes un perfil registrado, para registar utiliza /crearperfil.")

    def consultar_transacciones(self, message):
        # Obtener el chat_id del usuario
        chat_id = message.chat.id

        # Obtener el nombre de la tarjeta del mensaje anterior
        nombre_tarjeta = message.text
        
        usuario = session.query(Usuario).filter_by(telegram_id=chat_id).first()
        tarjeta = session.query(Tarjeta).filter(
            Tarjeta.nombre_tarjeta == nombre_tarjeta,
            Tarjeta.usuario_id == usuario.usuario_id
        ).first()

        trasnsacciones =  session.query(Transaccion).filter(
            Transaccion.usuario_id == usuario.usuario_id,
            Transaccion.tarjeta_id == tarjeta.tarjeta_id
        ).all()

        if trasnsacciones:
            mensaje_transacciones = "Tus transacciones son: \n"
            for transaccion in trasnsacciones:
                mensaje_transacciones += f"-{transaccion.tipo}-{transaccion.monto}-{transaccion.descripcion}-{transaccion.fecha_creacion}\n"
            self.bot.send_message(chat_id, mensaje_transacciones)
        else:
            self.bot.send_message(chat_id, "No tienes transacciones para esta tarjeta")

        self.bot.disable_save_next_step_handlers()