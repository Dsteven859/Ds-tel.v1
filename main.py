

#!/usr/bin/env python3
"""
Punto de entrada principal para el CC Checker Ultra Pro Bot
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Función principal que ejecuta el bot desde la subcarpeta correcta"""
    try:
        # Cambiar al directorio del bot
        bot_path = Path("CC-BOt-defi-v1/CC-BOt-definity/CC-Chece-51/CHL-Chernobiil41")
        
        if not bot_path.exists():
            print("❌ Error: No se encontró el directorio del bot")
            return
        
        # Ejecutar el bot desde su directorio
        os.chdir(bot_path)
        
        # Verificar que el token esté configurado
        bot_token = os.getenv('BOT_TOKEN')
        if not bot_token:
            print("❌ ERROR: BOT_TOKEN no configurado")
            print("💡 Configura tu token en la sección 'Secrets' de Replit")
            return
        
        print("🚀 Iniciando CC Checker Ultra Pro Bot...")
        
        # Ejecutar el bot
        subprocess.run([sys.executable, "main.py"], check=True)
        
    except KeyboardInterrupt:
        print("🛑 Bot detenido por el usuario")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando el bot: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

