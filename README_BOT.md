
# 🔥 CC Checker Ultra Pro Bot 🔥

Bot de Telegram avanzado para verificación de tarjetas de crédito con sistema de créditos, roles de admin y funciones premium.

## 🚀 Características

### 🎯 Funciones Principales
- **Generación de tarjetas** con algoritmos BIN avanzados
- **Verificación LIVE** con múltiples métodos de pago
- **Extrapolación avanzada** para revivir tarjetas muertas
- **Generador de direcciones** mundial
- **Sistema de créditos** con bonos diarios

### 👑 Sistema Premium
- **Verificación completa** con 4 métodos simultáneos
- **Límites aumentados** en generación
- **Algoritmos premium** con mayor efectividad
- **Soporte prioritario**

### 👮‍♂️ Panel de Administración
- **Gestión de usuarios** y roles
- **Estadísticas avanzadas**
- **Sistema de baneos** y advertencias
- **Activación de premium**

## 📱 Comandos Disponibles

### Generales
```
/start - Iniciar el bot
/gen [BIN] [cantidad] - Generar tarjetas
/live [tarjeta] - Verificar tarjetas
/direccion [país] - Generar direcciones
/ex [tarjeta] - Extrapolación avanzada
/status - Estado del bot
```

### Sistema de Créditos
```
/credits - Ver tus créditos
/bonus - Bono diario gratis
/infocredits - Cómo ganar créditos
/donate [user_id] [cantidad] - Donar créditos
/apply_key [código] - Aplicar clave premium
```

### Información
```
/dni [número] - Consulta RENIEC
/pasarela - Pasarelas de pago
```

### Solo Administradores
```
/setroles - Gestionar admins
/clean - Limpiar mensajes
/ban [user_id] - Banear usuario
/warn [user_id] - Advertir usuario
/premium [user_id] [días] - Dar premium
/stats - Estadísticas completas
```

## 🛠️ Instalación en Replit

### 1. Configurar Variables de Entorno

En la pestaña "Secrets" de Replit, agrega:

```
BOT_TOKEN = tu_token_de_botfather
ADMIN_IDS = 123456789,987654321
```

### 2. Instalar Dependencias

```bash
pip install -r requirements_bot.txt
```

### 3. Ejecutar el Bot

```bash
python run_bot.py
```

## 🔧 Configuración

### Obtener Token del Bot

1. Habla con [@BotFather](https://t.me/botfather) en Telegram
2. Usa `/newbot` y sigue las instrucciones
3. Copia el token que te proporciona

### Configurar Administradores

1. Obtén tu ID de Telegram desde [@userinfobot](https://t.me/userinfobot)
2. Agrega tu ID a la variable `ADMIN_IDS`

## 💎 Sistema de Créditos

### Cómo Funciona
- **Usuarios nuevos:** 10 créditos iniciales
- **Bono diario:** 10 créditos (15 premium)
- **Costo por comando:**
  - Generar: 2 créditos
  - Verificar: 3 créditos
  - Extrapolación: 5 créditos
  - Direcciones: 1 crédito

### Ganar Créditos Gratis
- **Bono diario** con `/bonus`
- **Invitar amigos**
- **Completar tareas**
- **Eventos especiales**

## 🎮 Uso Avanzado

### Generación de Tarjetas
```
/gen 557910 20
```
Genera 20 tarjetas con BIN 557910

### Verificación Premium
```
/live 5579100448040590|10|2029|285
```
Verifica con todos los métodos disponibles

### Extrapolación
```
/ex 5579100448040590|10|2029|285
```
Genera variaciones inteligentes

## 🔒 Seguridad

- **Validación de entrada** en todos los comandos
- **Control de acceso** por roles
- **Rate limiting** automático
- **Logs de auditoría** completos

## 📊 Estadísticas

El bot mantiene estadísticas detalladas:
- **Usuarios activos**
- **Comandos ejecutados**
- **Tarjetas verificadas**
- **Créditos distribuidos**

## 🆘 Soporte

Para soporte técnico:
1. Usa `/status` para verificar el estado
2. Contacta a los administradores
3. Revisa la documentación completa

## 📝 Notas Importantes

⚠️ **Este bot es solo para fines educativos y de demostración**

- No usar para actividades ilegales
- Respetar términos de servicio
- Uso responsable de las funciones

## 🔄 Actualizaciones

- **v2.0:** Sistema completo con premium
- **v1.5:** Comandos de administración
- **v1.0:** Funciones básicas

---

**Desarrollado con ❤️ para la comunidad**
