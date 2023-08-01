from models.usuario import Usuario, Tarjeta, Transaccion, session
from telebot import types

class TransaccionGasto:
    def __init__(self, bot):
        self.bot = bot

    def cancelar_registro(self, message):
        # Obtener el chat_id del usuario
        chat_id = message.chat.id

        # Deshabilitar el modo de guardar los controladores de pasos siguientes para esta conversación
        self.bot.disable_save_next_step_handlers()

        # Enviar un mensaje de confirmación de cancelación al usuario
        self.bot.send_message(chat_id, "Registro de transacción cancelado. Volviendo al menú principal.")


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

        transacciones = session.query(Transaccion).filter(
            Transaccion.usuario_id == usuario.usuario_id,
            Transaccion.tarjeta_id == tarjeta.tarjeta_id
        ).all()

        if transacciones:
            ingreso_total = 0
            egreso_total = 0

            for transaccion in transacciones:
                if transaccion.tipo == "Ingreso":
                    ingreso_total += transaccion.monto
                elif transaccion.tipo == "Egreso":
                    egreso_total += transaccion.monto

            resultado = ingreso_total - egreso_total

            mensaje_transacciones = f"Tus transacciones para {nombre_tarjeta} son:\n"
            for transaccion in transacciones:
                mensaje_transacciones += f"- {transaccion.tipo}: {transaccion.monto}\n"
            mensaje_transacciones += f"\nTotal de Ingresos: {ingreso_total}\n"
            mensaje_transacciones += f"Total de Egresos: {egreso_total}\n"
            mensaje_transacciones += f"Resultado (Ingresos - Egresos): {resultado}"

            self.bot.send_message(chat_id, mensaje_transacciones)

            # Ahora, creamos el "inline keyboard" para presentar opciones de modificación
            markup = types.InlineKeyboardMarkup()

            # Opción para NO modificar ninguna transacción
            markup.add(types.InlineKeyboardButton("No modificar ninguna transacción", callback_data="no_modificar"))

            # Opción para modificar alguna transacción
            markup.add(types.InlineKeyboardButton("Modificar transacción", callback_data="modificar"))

            # Enviamos el mensaje con el "inline keyboard"
            self.bot.send_message(chat_id, "¿Deseas modificar alguna transacción?", reply_markup=markup)
        else:
            self.bot.send_message(chat_id, "No tienes transacciones para esta tarjeta")

        self.bot.disable_save_next_step_handlers()

    def on_callback_query(self, callback_query):
        # Obtener el chat_id del usuario
        chat_id = callback_query.message.chat.id

        # Obtener el callback_data para saber qué opción se seleccionó
        callback_data = callback_query.data
        print(callback_data)

        if callback_data == "no_modificar":
            # Si selecciona "No modificar ninguna transacción", no se hace nada y la conversación termina
            self.bot.send_message(chat_id, "Entendido. No se realizarán modificaciones.")
        elif callback_data == "modificar":
            # Si selecciona "Modificar transacción", podemos continuar con el proceso de modificación
            # Puedes implementar aquí la lógica para modificar la transacción (por ejemplo, solicitar el ID de la transacción a modificar)
            self.bot.send_message(chat_id, "Ingresa el ID de la transacción que deseas modificar.")
            # Registramos el siguiente paso para manejar la entrada del ID de transacción a modificar
            self.bot.register_next_step_handler(callback_query.message, self.modificar_transaccion)

        elif callback_data.startswith("eliminar_transaccion:"):
            # Si el callback_data inicia con "eliminar_transaccion_", significa que el usuario seleccionó eliminar una transacción
            id_transaccion = callback_data.split(":")[1]

            # Consultar la transacción en base al ID proporcionado y al usuario
            usuario = session.query(Usuario).filter_by(telegram_id=chat_id).first()
            transaccion = session.query(Transaccion).filter_by(transaccion_id=id_transaccion, usuario_id=usuario.usuario_id).first()

            if transaccion:
                # Si se encontró la transacción, procedemos a eliminarla de la base de datos
                session.delete(transaccion)
                session.commit()
                self.bot.send_message(chat_id, f"La transacción con ID {id_transaccion} ha sido eliminada exitosamente.")
            else:
                # Si no se encontró la transacción, enviamos un mensaje de error
                self.bot.send_message(chat_id, f"No se encontró una transacción con ID {id_transaccion} asociada a tu usuario.")
        else:
            # Si el callback_data no es reconocido, simplemente enviamos un mensaje de error
            self.bot.send_message(chat_id, "Opción no válida.")

    def modificar_transaccion(self, message):
        # Obtener el chat_id del usuario
        chat_id = message.chat.id

        # Obtener el ID de la transacción a modificar
        id_transaccion = message.text

        # Consultar el perfil del usuario en base a su telegram_id
        usuario = session.query(Usuario).filter_by(telegram_id=chat_id).first()

        # Consultar la transacción específica en base al ID proporcionado y al usuario
        transaccion = session.query(Transaccion).filter_by(transaccion_id=id_transaccion, usuario_id=usuario.usuario_id).first()

        if transaccion:
            # Si se encontró la transacción, creamos un "inline keyboard" con una opción para eliminar la transacción
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Eliminar transacción", callback_data=f"eliminar_transaccion:{id_transaccion}"))

            # Enviamos un mensaje al usuario con la información de la transacción y las opciones de eliminar
            self.bot.send_message(chat_id, f"Información de la transacción:\n"
                                        f"Tipo: {transaccion.tipo}\n"
                                        f"Monto: {transaccion.monto}\n"
                                        f"Descripción: {transaccion.descripcion}\n"
                                        f"Fecha de Creación: {transaccion.fecha_creacion}\n\n"
                                        f"¿Deseas eliminar esta transacción?", reply_markup=markup)
        else:
            # Si no se encontró la transacción, enviamos un mensaje de error
            self.bot.send_message(chat_id, f"No se encontró una transacción con ID {id_transaccion} asociada a tu usuario.")

    
    def register_transaccion_commands(self, bot):
        bot.message_handler(commands=['registrar_transaccion'])(self.registrar_transaccion)
        bot.message_handler(commands=['cancelar'])(self.cancelar_registro)
        bot.message_handler(commands=['consultar_transacciones_tarjetas'])(self.consultar_transacciones_tarjetas)
        bot.callback_query_handler(func=lambda call: True)(self.on_callback_query)