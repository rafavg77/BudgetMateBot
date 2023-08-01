from telebot.types import Message

def handle_start(bot, message):
    bot.send_message(message.chat.id, "¡Hola! Soy un bot modular. ¡Comencemos!\
                    \nEstos son los comandos: \n /crearperfil \n/consultar_perfil \n/crear_tarjeta \n/consultar_tarjetas \n/registrar_transaccion \n/consultar_transacciones_tarjetas \n/cancelar ")

def handle_help(bot, message):
    bot.send_message(message.chat.id, "Este es un mensaje de ayuda.")

def register_commands(bot):
    # Registra las funciones de manejo de comandos en el objeto bot automáticamente
    bot.message_handler(commands=['start'])(lambda message: handle_start(bot, message))
    bot.message_handler(commands=['help'])(lambda message: handle_help(bot, message))
