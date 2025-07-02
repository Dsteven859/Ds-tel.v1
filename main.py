
#!/usr/bin/env python3
"""
Punto de entrada principal para CC Checker Ultra Pro Bot
Optimizado para Render.com
"""

import os
import sys
import logging
import threading
import time
from flask import Flask

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Crear aplicación Flask para health checks de Render
app = Flask(__name__)

@app.route('/')
def health_check():
    """Health check endpoint para Render"""
    return {
        "status": "healthy",
        "service": "CC Checker Ultra Pro Bot",
        "timestamp": time.time(),
        "message": "Bot is running successfully on Render.com"
    }

@app.route('/status')
def bot_status():
    """Status endpoint detallado"""
    return {
        "bot_name": "CC Checker Ultra Pro",
        "status": "active",
        "platform": "Render.com",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "uptime": "24/7"
    }

def run_flask():
    """Ejecutar servidor Flask en hilo separado"""
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

def main():
    """Función principal"""
    logger.info("🚀 Iniciando CC Checker Ultra Pro Bot en Render.com...")
    
    # Verificar variables de entorno requeridas
    if not os.getenv('BOT_TOKEN'):
        logger.error("❌ BOT_TOKEN no configurado en variables de entorno")
        sys.exit(1)
    
    try:
        # Iniciar servidor Flask en hilo separado para health checks
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()
        logger.info(f"✅ Servidor Flask iniciado en puerto {os.environ.get('PORT', 5000)}")
        
        # Importar y ejecutar el bot principal
        from telegram_bot import main as run_bot
        run_bot()
        
    except KeyboardInterrupt:
        logger.info("🛑 Bot detenido por usuario")
    except Exception as e:
        logger.error(f"❌ Error crítico: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
