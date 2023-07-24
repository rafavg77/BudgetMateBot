import telebot
import logging
from utils.config import load_config
from modules.comandos_module import register_commands
from modules.perfil_module import PerfilGasto
from modules.tarjeta_module import TarjetaGasto
from modules.transaccion_module import TransaccionGasto

# Cargar configuración del archivo
config = load_config()

# Inicializar el bot con el token
bot = telebot.TeleBot(config['BOT_TOKEN'])

# Configurar el logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler() 
    ]
)
logger = logging.getLogger(__name__)

# Registrar las funciones de manejo de comandos automáticamente
register_commands(bot)

# Registrar las funciones de pefil de gasto
perfil_gasto = PerfilGasto(bot)
bot.message_handler(commands=['crearperfil'])(perfil_gasto.crear_perfil)
bot.message_handler(commands=['consultar_perfil'])(perfil_gasto.consultar_perfil)

tarjeta_gasto = TarjetaGasto(bot)
bot.message_handler(commands=['crear_tarjeta'])(tarjeta_gasto.crear_tarjeta)
bot.message_handler(commands=['consultar_tarjetas'])(tarjeta_gasto.consultar_tarjetas)

# Registrar las funciones de pefil de gasto
transaccion_gasto = TransaccionGasto(bot)
bot.message_handler(commands=['registrar_transaccion'])(transaccion_gasto.registrar_transaccion)
bot.message_handler(commands=['consultar_transacciones_tarjetas'])(transaccion_gasto.consultar_transacciones_tarjetas)

# Iniciar el bot y mantenerlo en ejecución
bot.polling()
