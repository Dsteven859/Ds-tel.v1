
#!/usr/bin/env python3
"""
Script principal para ejecutar el CC Checker Ultra Pro Bot
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def check_requirements():
    """Verifica que todos los requisitos estén instalados"""
    try:
        import telegram
        from telegram.ext import Application
        import requests
        logger.info("✅ Todas las dependencias están instaladas")
        return True
    except ImportError as e:
        logger.error(f"❌ Falta dependencia: {e}")
        logger.error("Ejecuta: pip install -r requirements_bot.txt")
        return False

def check_environment():
    """Verifica variables de entorno"""
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        logger.error("❌ BOT_TOKEN no configurado")
        logger.error("Configura tu token en las variables de entorno")
        return False
    
    logger.info("✅ Variables de entorno configuradas")
    return True

def main():
    """Función principal"""
    logger.info("🚀 Iniciando CC Checker Ultra Pro Bot...")
    
    # Verificar requisitos
    if not check_requirements():
        sys.exit(1)
    
    if not check_environment():
        sys.exit(1)
    
    try:
        # Importar y ejecutar el bot
        from telegram_bot import main as run_bot
        run_bot()
    except KeyboardInterrupt:
        logger.info("🛑 Bot detenido por el usuario")
    except Exception as e:
        logger.error(f"❌ Error crítico: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
import os
import sys
from telegram_bot import main

if __name__ == "__main__":
    main()
