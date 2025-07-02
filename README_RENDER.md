
# Despliegue en Render.com - CC Checker Ultra Pro Bot

## 🚀 Guía Paso a Paso

### 1. Preparación del Código
✅ **Código optimizado para Render.com**
- Bot principal: `telegram_bot.py`
- Punto de entrada: `main.py`
- Health checks incluidos
- Logging optimizado

### 2. Configuración en Render

#### Crear Nuevo Web Service
1. Ve a [Render.com](https://render.com)
2. Conecta tu repositorio de GitHub
3. Selecciona "New Web Service"
4. Elige este repositorio

#### Configuración del Servicio
```
Name: chernobil-chlv-bot
Environment: Python 3
Build Command: pip install -r requirements_bot.txt
Start Command: python main.py
```

### 3. Variables de Entorno Requeridas

En la sección "Environment Variables" de Render, agrega:

```env
BOT_TOKEN=tu_token_de_telegram_bot
ADMIN_IDS=123456789,987654321
FOUNDER_IDS=123456789
COFOUNDER_IDS=987654321
PORT=5000
```

### 4. Obtener Token del Bot

1. Habla con [@BotFather](https://t.me/botfather) en Telegram
2. Crea un nuevo bot con `/newbot`
3. Copia el token y agrégalo a las variables de entorno

### 5. Configurar IDs

Para obtener tu ID de Telegram:
1. Habla con [@userinfobot](https://t.me/userinfobot)
2. Te dará tu ID numérico
3. Agrégalo a `ADMIN_IDS` en las variables de entorno

### 6. Desplegar

1. Hacer push de los cambios a GitHub
2. Render detectará automáticamente los cambios
3. El despliegue iniciará automáticamente
4. Espera 5-10 minutos para el primer despliegue

### 7. Verificar Funcionamiento

#### Health Check
- URL: `https://tu-app.onrender.com/`
- Debe retornar: `{"status": "healthy", ...}`

#### Status
- URL: `https://tu-app.onrender.com/status`
- Información detallada del bot

### 8. Configurar Dominio (Opcional)

En la configuración de Render:
1. Ve a "Settings"
2. Sección "Custom Domains"
3. Agrega tu dominio personalizado

### 9. Monitoreo

#### Logs en Tiempo Real
```bash
# En la consola de Render
tail -f logs
```

#### Métricas Disponibles
- CPU usage
- Memory usage
- Response time
- Request count

### 10. Mantenimiento

#### Actualizar el Bot
1. Hacer cambios en el código
2. Push a GitHub
3. Render redesplegará automáticamente

#### Reiniciar Servicio
- Desde el dashboard de Render
- Botón "Manual Deploy"

## 🔧 Características Optimizadas

### Performance
- ✅ Polling optimizado
- ✅ Memory management mejorado
- ✅ Error handling robusto
- ✅ Logging estructurado

### Escalabilidad
- ✅ Health checks integrados
- ✅ Graceful shutdown
- ✅ Database en archivo JSON
- ✅ Auto-restart en fallos

### Seguridad
- ✅ Variables de entorno
- ✅ SSL/TLS automático
- ✅ Rate limiting
- ✅ Anti-spam integrado

## 🆘 Troubleshooting

### Bot no responde
1. Verificar logs en Render
2. Confirmar BOT_TOKEN correcto
3. Verificar que el bot esté iniciado en Telegram

### Health check falla
1. Verificar que el puerto 5000 esté libre
2. Confirmar que Flask esté iniciando
3. Revisar logs de errores

### Variables de entorno
1. Verificar sintaxis correcta
2. Sin espacios extra
3. IDs numéricos válidos

## 📞 Soporte

- **Logs**: Dashboard de Render > Logs
- **Métricas**: Dashboard de Render > Metrics
- **Status**: `https://tu-app.onrender.com/status`

---

## 🎯 URLs Importantes

- **Health Check**: `https://tu-app.onrender.com/`
- **Status**: `https://tu-app.onrender.com/status`
- **Logs**: Dashboard de Render
- **Metrics**: Dashboard de Render

¡Tu bot está listo para funcionar 24/7 en Render.com! 🚀
