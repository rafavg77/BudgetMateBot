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
BOT_MASTER = config.get('BOT_MASTER')
BOOT_MESSAGE = config.get('BOOT_MESSAGE')

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

perfil_gasto = PerfilGasto(bot)
perfil_gasto.register_perfil_commands(bot)

tarjeta_gasto = TarjetaGasto(bot)
tarjeta_gasto.register_tarjeta_commands(bot)

transaccion_gasto = TransaccionGasto(bot)
transaccion_gasto.register_transaccion_commands(bot)

# Iniciar el bot y mantenerlo en ejecución
logger.info(BOOT_MESSAGE)
bot.send_message(BOT_MASTER, BOOT_MESSAGE)
bot.polling(none_stop=True, timeout=123)