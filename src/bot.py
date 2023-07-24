import telebot
import logging
from utils.config import load_config
from modules.commands_module import register_commands
from modules.perfil_gasto_module import PerfilGasto
from modules.transaccion_gasto_module import TransaccionGasto

# Cargar configuración del archivo
config = load_config()

# Inicializar el bot con el token
bot = telebot.TeleBot(config['BOT_TOKEN'])

# Configurar el logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()  # Agrega el StreamHandler para mostrar logs en la consola
    ]
)
logger = logging.getLogger(__name__)

# Registrar las funciones de manejo de comandos automáticamente
register_commands(bot)

# Registrar las funciones de pefil de gasto
perfil_gasto = PerfilGasto(bot)
bot.message_handler(commands=['crearperfil'])(perfil_gasto.crear_perfil)
bot.message_handler(commands=['consultar_perfil'])(perfil_gasto.consultar_perfil)

# Registrar las funciones de pefil de gasto
transaccion_gasto = TransaccionGasto(bot)
bot.message_handler(commands=['registrar_transaccion'])(transaccion_gasto.registrar_transaccion)
bot.message_handler(commands=['consultar_transacciones'])(transaccion_gasto.consultar_transacciones)

# Iniciar el bot y mantenerlo en ejecución
bot.polling()
