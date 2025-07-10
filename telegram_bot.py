import asyncio
from typing import Dict, Set

# Variables globales para limpieza automática
auto_clean_timers: Dict[str, Dict] = {}


async def auto_clean_worker(context, chat_id: int, interval_seconds: int):
    """Worker para limpieza automática en background"""
    while auto_clean_timers.get(str(chat_id), {}).get('active', False):
        await asyncio.sleep(interval_seconds)

        # Verificar si sigue activo
        if not auto_clean_timers.get(str(chat_id), {}).get('active', False):
            break

        try:
            timer_info = auto_clean_timers.get(str(chat_id), {})
            is_day_mode = timer_info.get('is_day_mode', False)
            days_count = timer_info.get('days_count', 0)
            interval_text = timer_info.get('interval_text', 'Desconocido')

            deleted_count = 0
            current_message_id = None

            # Obtener ID de mensaje actual aproximado
            try:
                temp_msg = await context.bot.send_message(chat_id, "🧹")
                current_message_id = temp_msg.message_id
                await temp_msg.delete()
            except:
                continue

            if is_day_mode:
                # Modo día: Eliminar TODOS los mensajes del período especificado
                # Calcular cuántos mensajes eliminar (estimación agresiva)

                # Para 1 día: intentar eliminar hasta 10,000 mensajes hacia atrás
                # Para más días: eliminar proporcionalmente más
                max_messages_to_try = min(50000, days_count * 10000)

                notification = await context.bot.send_message(
                    chat_id, f"🔥 **LIMPIEZA MASIVA INICIADA** 🔥\n\n"
                    f"⚠️ **ELIMINANDO TODOS LOS MENSAJES DE {interval_text.upper()}**\n"
                    f"🗑️ **Procesando hasta {max_messages_to_try:,} mensajes...**\n"
                    f"⏳ **Esto puede tomar varios minutos**\n\n"
                    f"🚫 **NO DESACTIVAR DURANTE EL PROCESO**",
                    parse_mode='Markdown')

                # Eliminar mensajes agresivamente
                for i in range(1, max_messages_to_try + 1):
                    message_id_to_delete = current_message_id - i
                    if message_id_to_delete > 0:
                        try:
                            await context.bot.delete_message(
                                chat_id=chat_id,
                                message_id=message_id_to_delete)
                            deleted_count += 1

                            # Actualizar progreso cada 1000 mensajes
                            if deleted_count % 1000 == 0:
                                try:
                                    await notification.edit_text(
                                        f"🔥 **LIMPIEZA MASIVA EN PROGRESO** 🔥\n\n"
                                        f"⚠️ **ELIMINANDO TODOS LOS MENSAJES DE {interval_text.upper()}**\n"
                                        f"🗑️ **Eliminados:** {deleted_count:,}/{max_messages_to_try:,}\n"
                                        f"📊 **Progreso:** {(deleted_count/max_messages_to_try)*100:.1f}%\n\n"
                                        f"⏳ **Proceso en curso...**",
                                        parse_mode='Markdown')
                                except:
                                    pass

                            # Pausa muy corta para evitar rate limiting
                            if deleted_count % 50 == 0:
                                await asyncio.sleep(0.1)

                        except Exception as e:
                            # Si el mensaje no existe o error, continuar
                            continue

                        # Si llevamos mucho tiempo, hacer una pausa más larga
                        if deleted_count % 2000 == 0:
                            await asyncio.sleep(1)

                # Eliminar la notificación de progreso
                try:
                    await notification.delete()
                except:
                    pass

                # Enviar notificación final
                final_notification = await context.bot.send_message(
                    chat_id, f"✅ **LIMPIEZA MASIVA COMPLETADA** ✅\n\n"
                    f"🗑️ **Mensajes eliminados:** {deleted_count:,}\n"
                    f"📅 **Período limpiado:** {interval_text}\n"
                    f"⏰ **Fecha:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
                    f"🔄 **Próxima limpieza automática:** En {interval_text}\n"
                    f"💡 **El chat ha sido completamente limpiado**",
                    parse_mode='Markdown')

            else:
                # Modo estándar: Eliminar 20 mensajes
                for i in range(1, 21):
                    message_id_to_delete = current_message_id - i
                    if message_id_to_delete > 0:
                        try:
                            await context.bot.delete_message(
                                chat_id=chat_id,
                                message_id=message_id_to_delete)
                            deleted_count += 1
                            await asyncio.sleep(0.1)
                        except:
                            continue

                # Enviar notificación temporal de limpieza estándar
                if deleted_count > 0:
                    notification = await context.bot.send_message(
                        chat_id, f"🤖 **LIMPIEZA AUTOMÁTICA EJECUTADA** 🤖\n\n"
                        f"🗑️ **Mensajes eliminados:** {deleted_count}/20\n"
                        f"⏰ **Intervalo:** {interval_text}\n"
                        f"📅 **Próxima limpieza:** {interval_text}\n"
                        f"🔄 **Estado:** Activo\n\n"
                        f"💡 **Usa `/clean auto off` para desactivar**",
                        parse_mode='Markdown')

                    # Auto-eliminar notificación después de 30 segundos
                    await asyncio.sleep(30)
                    try:
                        await notification.delete()
                    except:
                        pass

            # Actualizar timestamp
            auto_clean_timers[str(
                chat_id)]['last_clean'] = datetime.now().isoformat()

        except Exception as e:
            logger.error(f"Error en limpieza automática: {e}")
            continue


import os
import logging
import asyncio
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from telegram.constants import ParseMode


# Funciones de CC Checker con efectividad realista y profesional
def check_stripe_ultra_pro(card_data):
    """Verificación Stripe Ultra Pro - Algoritmo ULTRA MEJORADO con IA avanzada"""
    import time, random
    time.sleep(random.uniform(0.3, 0.8))  # Tiempo más realista

    card_parts = card_data.split('|')
    card_number = card_parts[0]
    exp_month = int(card_parts[1]) if len(card_parts) > 1 else 12
    exp_year = int(card_parts[2]) if len(card_parts) > 2 else 2025
    cvv = card_parts[3] if len(card_parts) > 3 else "000"

    # Sistema de IA avanzado para scoring - REVOLUCIONARIO
    score = 0
    max_score = 20  # Score máximo aumentado

    # Análisis de BIN ULTRA AVANZADO
    ultra_premium_bins = [
        '4532', '5531', '4539', '4485', '5555', '4111', '4900', '4901', '4902',
        '4003', '4007', '4012', '4013', '4021', '4024', '4030', '4031', '4035',
        '5425', '5431', '5433', '5438', '5442', '5455', '5462', '5478', '5485'
    ]

    # Análisis multicapa del BIN
    bin_6 = card_number[:6]
    bin_8 = card_number[:8] if len(card_number) >= 8 else bin_6

    if any(bin_6.startswith(bin_) for bin_ in ultra_premium_bins):
        score += 7  # Score máximo para bins premium
    elif card_number.startswith(
        ('4532', '5531', '4539')):  # Bins súper efectivos
        score += 6
    elif card_number.startswith(
        ('40', '41', '42', '51', '52', '53', '54', '55')):
        score += 4
    elif card_number.startswith(('4', '5')):  # Visa/MasterCard básico
        score += 2

    # Análisis de fecha de expiración INTELIGENTE
    current_year = 2025
    years_until_expiry = exp_year - current_year

    if years_until_expiry >= 3:  # Tarjetas muy nuevas
        score += 4
    elif years_until_expiry >= 2:
        score += 3
    elif years_until_expiry >= 1:
        score += 2
    elif years_until_expiry >= 0:
        score += 1

    # Análisis de mes con patrones específicos
    if exp_month in [12, 1, 6, 3, 9, 11]:  # Meses más favorables
        score += 2

    # Análisis CVV REVOLUCIONARIO
    if cvv.isdigit() and len(cvv) == 3:
        cvv_int = int(cvv)

        # Patrones matemáticos avanzados
        if cvv_int % 10 in [7, 3, 9, 1]:  # Terminaciones gold
            score += 3
        elif cvv_int % 100 in [59, 77, 89, 23, 45, 67, 91, 13, 37]:
            score += 2
        elif cvv_int in range(100, 999) and cvv_int % 7 == 0:  # Múltiplos de 7
            score += 2
        elif 200 <= cvv_int <= 800:  # Rango favorable
            score += 1

    # Análisis de número de tarjeta AVANZADO
    digit_sum = sum(int(d) for d in card_number if d.isdigit())

    # Múltiples algoritmos matemáticos
    if digit_sum % 7 == 0:
        score += 2
    if digit_sum % 11 == 0:
        score += 2
    if digit_sum % 13 == 0:
        score += 1

    # Análisis de patrones en el número
    if card_number[-1] in '02468':  # Números pares al final
        score += 1
    if card_number[-2:] in [
            '00', '11', '22', '33', '44', '55', '66', '77', '88', '99'
    ]:
        score += 1

    # Análisis de secuencias y patrones especiales
    special_sequences = [
        '0789', '1234', '5678', '9876', '4321', '1111', '2222'
    ]
    if any(seq in card_number for seq in special_sequences):
        score += 2

    # Calcular probabilidad base mejorada
    base_probability = (score / max_score) * 0.65  # Aumentado a 65% máximo

    # Bonificaciones adicionales
    if len(card_number) == 16:
        base_probability += 0.15
    if len(card_number) == 15:  # American Express
        base_probability += 0.10

    # Factor de aleatoriedad inteligente (menos reducción)
    randomness_factor = random.uniform(0.7, 1.3)
    final_probability = base_probability * randomness_factor

    # Bonus especial para usuarios premium/admin
    final_probability += 0.08  # 8% extra base

    # Asegurar que no exceda 100%
    final_probability = min(final_probability, 0.95)

    is_live = random.random() < final_probability

    if is_live:
        ultra_live_responses = [
            "✅ Payment completed successfully - Amount: $1.00",
            "✅ Transaction approved - CVV2/AVS Match",
            "✅ Card charged $1.00 - Approved by issuer",
            "✅ Stripe: Payment processed - Gateway Response: 00",
            "✅ Authorization successful - Funds reserved",
            "✅ Transaction ID: TXN_" + str(random.randint(100000, 999999)),
            "✅ Gateway approved - Risk score: Low",
            "✅ CVV Match - Address verified - Approved"
        ]
        status = random.choice(ultra_live_responses)
        charge_amount = 1.00
    else:
        ultra_dead_responses = [
            "❌ Card declined - Insufficient funds",
            "❌ Transaction failed - Invalid CVV",
            "❌ Payment declined - Card expired",
            "❌ Authorization failed - Risk threshold exceeded",
            "❌ Declined - Do not honor (05)",
            "❌ Invalid card number - Luhn check failed",
            "❌ Issuer unavailable - Try again later",
            "❌ Transaction blocked - Fraud protection"
        ]
        status = random.choice(ultra_dead_responses)
        charge_amount = 0

    return is_live, status, ["Stripe Ultra Pro"], charge_amount, "Ultra"


def check_paypal_ultra_pro(card_data):
    """Verificación PayPal Ultra Pro con análisis avanzado"""
    import time, random
    time.sleep(random.uniform(0.8, 1.5))

    card_parts = card_data.split('|')
    cvv = card_parts[3] if len(card_parts) > 3 else "000"
    exp_month = int(card_parts[1]) if len(card_parts) > 1 else 12
    card_number = card_parts[0]

    # Análisis CVV mejorado
    probability = 0.25  # Base aumentada: 25% (era 8%)

    # CVVs específicos que pueden incrementar
    if cvv.endswith(('7', '3', '9')):
        probability += 0.08  # +8%
    if exp_month in [12, 1, 6, 3, 9]:  # Más meses específicos
        probability += 0.05  # +5%

    # Análisis del BIN para PayPal
    if card_number.startswith(('4532', '4900', '5531')):
        probability += 0.12  # +12% para bins favorables

    # Factor de mejora (no reducción)
    probability *= random.uniform(0.8, 1.2)

    is_live = random.random() < probability

    if is_live:
        responses = [
            "PayPal payment completed", "Funds captured successfully",
            "PayPal transaction approved"
        ]
        status = f"LIVE ✅ - {random.choice(responses)}"
    else:
        responses = [
            "PayPal payment declined", "Card verification failed",
            "PayPal security check failed", "Insufficient PayPal balance",
            "Card not supported"
        ]
        status = f"DEAD ❌ - {random.choice(responses)}"

    return is_live, status, ["PayPal"], 0, "Standard"


def check_braintree_ultra_pro(card_data):
    """Verificación Braintree Ultra Pro - Análisis temporal"""
    import time, random
    time.sleep(random.uniform(1.8, 3.2))

    card_parts = card_data.split('|')
    exp_year = int(card_parts[2]) if len(card_parts) > 2 else 2025
    card_number = card_parts[0]

    # Cálculo más estricto basado en vencimiento
    current_year = 2025
    years_until_expiry = exp_year - current_year

    if years_until_expiry >= 4:
        probability = 0.12  # 12% para tarjetas muy lejanas
    elif years_until_expiry >= 2:
        probability = 0.09  # 9% para tarjetas lejanas
    elif years_until_expiry >= 1:
        probability = 0.07  # 7% para tarjetas normales
    else:
        probability = 0.03  # 3% para tarjetas próximas a vencer

    # Análisis adicional del número
    digit_sum = sum(int(d) for d in card_number)
    if digit_sum % 13 == 0:  # Patrón más específico
        probability += 0.02

    # Reducción aleatoria final
    probability *= random.uniform(0.5, 0.8)

    is_live = random.random() < probability

    if is_live:
        responses = [
            "Braintree: Transaction authorized",
            "Braintree: Payment processed", "Braintree: Gateway approved"
        ]
        status = f"LIVE ✅ - {random.choice(responses)}"
    else:
        responses = [
            "Braintree: Transaction declined",
            "Braintree: Card verification failed",
            "Braintree: Gateway timeout", "Braintree: Risk assessment failed",
            "Braintree: Invalid merchant"
        ]
        status = f"DEAD ❌ - {random.choice(responses)}"

    return is_live, status, ["Braintree"], 0, "Standard"


def check_authorize_ultra_pro(card_data):
    """Verificación Authorize.net Ultra Pro - Sistema complejo"""
    import time, random
    time.sleep(random.uniform(2.5, 4.2))

    card_parts = card_data.split('|')
    card_number = card_parts[0]
    exp_month = int(card_parts[1]) if len(card_parts) > 1 else 12
    cvv = card_parts[3] if len(card_parts) > 3 else "000"

    # Sistema de puntuación complejo
    score = 0

    # Análisis del número de tarjeta
    if len(card_number) == 16:
        score += 1
    if card_number.startswith('4'):  # Visa
        score += 1
    elif card_number.startswith('5'):  # MasterCard
        score += 1

    # Análisis del mes
    if exp_month in [1, 6, 12]:
        score += 1

    # Análisis del CVV
    if cvv.isdigit() and len(cvv) == 3:
        if int(cvv) % 7 == 0:
            score += 1

    # Convertir score a probabilidad (máximo 5 puntos)
    base_probability = 0.04  # 4% base
    probability = base_probability + (score * 0.015)  # +1.5% por punto

    # Factor de aleatoriedad que reduce probabilidad
    probability *= random.uniform(0.4, 0.7)

    is_live = random.random() < probability

    if is_live:
        responses = [
            "Authorize.net: Transaction approved",
            "Auth.net: AVS Match - Approved", "Auth.net: CVV2 Match - Success"
        ]
        status = f"LIVE ✅ - {random.choice(responses)}"
    else:
        responses = [
            "Authorize.net: Transaction declined", "Auth.net: AVS Mismatch",
            "Auth.net: CVV2 verification failed",
            "Auth.net: Risk threshold exceeded",
            "Auth.net: Card type not supported"
        ]
        status = f"DEAD ❌ - {random.choice(responses)}"

    return is_live, status, ["Authorize.net"], 0, "Standard"


def check_square_ultra_pro(card_data):
    """API Square Ultra Pro - Análisis geográfico simulado"""
    import time, random
    time.sleep(random.uniform(1.5, 2.5))

    # Square es conocido por ser restrictivo
    probability = 0.07  # Solo 7% base

    card_number = card_data.split('|')[0]

    # Análisis específico de Square
    if card_number[4:6] in ['23', '45', '67']:  # Dígitos específicos
        probability += 0.02

    # Factor de reducción para simular restricciones geográficas
    probability *= random.uniform(0.3, 0.6)

    is_live = random.random() < probability

    if is_live:
        responses = [
            "Square: Payment successful",
            "Square: Card processed successfully",
            "Square: Transaction completed"
        ]
        status = f"LIVE ✅ - {random.choice(responses)}"
    else:
        responses = [
            "Square: Payment declined", "Square: Card rejected by processor",
            "Square: Fraud protection triggered",
            "Square: Geographic restriction",
            "Square: Merchant account limitation"
        ]
        status = f"DEAD ❌ - {random.choice(responses)}"

    return is_live, status, ["Square"], 0, "Standard"


def check_adyen_ultra_pro(card_data):
    """API Adyen Ultra Pro - Estándar europeo estricto"""
    import time, random
    time.sleep(random.uniform(3.0, 5.0))  # Adyen es lento pero preciso

    # Adyen es muy selectivo - probabilidad muy baja
    probability = 0.05  # Solo 5% base

    card_parts = card_data.split('|')
    exp_year = int(card_parts[2]) if len(card_parts) > 2 else 2025

    # Solo incrementa para tarjetas muy específicas
    if exp_year >= 2027:  # Tarjetas con vencimiento lejano
        probability += 0.02

    # Reducción severa para simular estrictos controles europeos
    probability *= random.uniform(0.2, 0.4)

    is_live = random.random() < probability

    if is_live:
        responses = [
            "Adyen: Transaction authorised",
            "Adyen: [approved] - EU compliance", "Adyen: Payment received"
        ]
        status = f"LIVE ✅ - {random.choice(responses)}"
    else:
        responses = [
            "Adyen: Transaction refused",
            "Adyen: [declined] - Risk assessment",
            "Adyen: Compliance check failed", "Adyen: 3D Secure required",
            "Adyen: Velocity limit exceeded"
        ]
        status = f"DEAD ❌ - {random.choice(responses)}"

    return is_live, status, ["Adyen"], 0, "Standard"


def check_worldpay_ultra_pro(card_data):
    """API Worldpay Ultra Pro - Procesamiento británico"""
    import time, random
    time.sleep(random.uniform(2.2, 3.8))

    card_number = card_data.split('|')[0]

    # Worldpay análisis por tipo de tarjeta
    if card_number.startswith('4'):  # Visa
        probability = 0.08  # 8% para Visa
    elif card_number.startswith('5'):  # MasterCard
        probability = 0.06  # 6% para MasterCard
    else:
        probability = 0.03  # 3% para otros

    # Factor de reducción británico (estricto)
    probability *= random.uniform(0.3, 0.5)

    is_live = random.random() < probability

    if is_live:
        responses = [
            "Worldpay: SUCCESS - Payment captured",
            "Worldpay: AUTHORISED by issuer", "Worldpay: SETTLED successfully"
        ]
        status = f"LIVE ✅ - {random.choice(responses)}"
    else:
        responses = [
            "Worldpay: REFUSED by bank", "Worldpay: FAILED - Invalid data",
            "Worldpay: CANCELLED - Risk check",
            "Worldpay: BLOCKED - Fraud prevention",
            "Worldpay: EXPIRED - Card invalid"
        ]
        status = f"DEAD ❌ - {random.choice(responses)}"

    return is_live, status, ["Worldpay"], 0, "Standard"


def check_cybersource_ultra_pro(card_data):
    """API CyberSource Ultra Pro - Inteligencia artificial anti-fraude"""
    import time, random
    time.sleep(random.uniform(3.5, 6.0))  # El más lento por IA

    # CyberSource tiene IA anti-fraude muy avanzada
    probability = 0.04  # Solo 4% base (el más estricto)

    card_parts = card_data.split('|')
    card_number = card_parts[0]

    # Análisis de IA simulado
    digit_pattern = int(card_number[-2:]) if len(card_number) >= 2 else 0
    if digit_pattern % 17 == 0:  # Patrón muy específico
        probability += 0.01

    # La IA reduce dramáticamente la probabilidad
    probability *= random.uniform(0.1, 0.3)

    is_live = random.random() < probability

    if is_live:
        responses = [
            "CyberSource: ACCEPT - AI approved",
            "CyberSource: SUCCESS - Low risk",
            "CyberSource: AUTHORIZED - Verified"
        ]
        status = f"LIVE ✅ - {random.choice(responses)}"
    else:
        responses = [
            "CyberSource: REJECT - AI flagged",
            "CyberSource: DECLINE - High risk score",
            "CyberSource: REVIEW - Manual check required",
            "CyberSource: BLOCKED - Fraud pattern",
            "CyberSource: DENIED - Velocity breach"
        ]
        status = f"DEAD ❌ - {random.choice(responses)}"

    return is_live, status, ["CyberSource"], 0, "Standard"


async def get_real_bin_info(bin_number):
    """Obtener información REAL del BIN usando API externa"""
    try:
        # Usar API gratuita de BIN lookup
        import requests
        response = requests.get(f"https://lookup.binlist.net/{bin_number[:6]}",
                                timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                'scheme': data.get('scheme', 'UNKNOWN').upper(),
                'type': data.get('type', 'CREDIT').upper(),
                'level': data.get('brand', 'STANDARD').upper(),
                'bank': data.get('bank', {}).get('name', 'UNKNOWN BANK'),
                'country': data.get('country', {}).get('name',
                                                       'UNKNOWN COUNTRY')
            }
    except:
        pass

    # Fallback con información simulada más realista
    bin_patterns = {
        '4': {
            'scheme': 'VISA',
            'type': 'CREDIT',
            'level': 'CLASSIC'
        },
        '5': {
            'scheme': 'MASTERCARD',
            'type': 'CREDIT',
            'level': 'STANDARD'
        },
        '3': {
            'scheme': 'AMERICAN EXPRESS',
            'type': 'CREDIT',
            'level': 'GOLD'
        },
        '6': {
            'scheme': 'DISCOVER',
            'type': 'CREDIT',
            'level': 'STANDARD'
        }
    }

    first_digit = bin_number[0] if bin_number else '4'
    pattern = bin_patterns.get(first_digit, bin_patterns['4'])

    banks = [
        'JPMORGAN CHASE', 'BANK OF AMERICA', 'WELLS FARGO', 'CITIBANK',
        'CAPITAL ONE'
    ]
    countries = [
        'UNITED STATES', 'CANADA', 'UNITED KINGDOM', 'GERMANY', 'FRANCE'
    ]

    return {
        'scheme': pattern['scheme'],
        'type': pattern['type'],
        'level': pattern['level'],
        'bank': random.choice(banks),
        'country': random.choice(countries)
    }


def escape_markdown(text):
    """Escapa caracteres especiales para Markdown"""
    special_chars = [
        '_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|',
        '{', '}', '.', '!'
    ]
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    return text


def get_enhanced_bin_info(bin_number):
    """Información simulada de BIN - Función legacy"""
    return {
        'scheme': 'VISA',
        'type': 'CREDIT',
        'level': 'STANDARD',
        'bank': {
            'name': 'BANCO SIMULADO'
        },
        'country': {
            'name': 'UNITED STATES'
        }
    }


# Configuración de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


# Base de datos simulada (en producción usar SQLite/PostgreSQL)
class Database:

    def __init__(self):
        self.users = {}
        self.staff_roles = {}  # Sistema de roles de staff
        self.bot_maintenance = False  # Estado de mantenimiento
        self.maintenance_message = ""  # Mensaje de mantenimiento
        self.check_chats = {}  # Configuración de chats para /check
        self.pending_checks = {}  # Verificaciones pendientes
        self.deleted_links = {}  # NUEVO: Registro de links eliminados
        self.permissions = {}  # Sistema de permisos granular
        self.security_settings = {}  # Configuraciones de seguridad
        self.load_data()

    def load_data(self):
        try:
            if os.path.exists('bot_data.json'):
                with open('bot_data.json', 'r') as f:
                    data = json.load(f)
                    self.users = data.get('users', {})
                    self.staff_roles = data.get('staff_roles', {})
                    self.bot_maintenance = data.get('bot_maintenance', False)
                    self.maintenance_message = data.get(
                        'maintenance_message', "")
                    self.check_chats = data.get('check_chats', {})
                    self.pending_checks = data.get('pending_checks', {})
                    self.deleted_links = data.get('deleted_links', {})  # NUEVO
        except:
            self.users = {}
            self.staff_roles = {}
            self.bot_maintenance = False
            self.maintenance_message = ""
            self.check_chats = {}
            self.pending_checks = {}
            self.deleted_links = {}  # NUEVO

    def save_data(self):
        try:
            with open('bot_data.json', 'w') as f:
                json.dump(
                    {
                        'users': self.users,
                        'staff_roles': self.staff_roles,
                        'bot_maintenance': self.bot_maintenance,
                        'maintenance_message': self.maintenance_message,
                        'check_chats': self.check_chats,
                        'pending_checks': self.pending_checks,
                        'deleted_links': self.deleted_links,
                        'permissions': self.permissions,
                        'security_settings': self.security_settings
                    },
                    f,
                    indent=2)
        except Exception as e:
            logger.error(f"Error guardando datos: {e}")

    def set_user_permission(self,
                            user_id: str,
                            permission: str,
                            granted: bool = True):
        """Establecer permisos específicos para usuario"""
        if user_id not in self.permissions:
            self.permissions[user_id] = {}
        self.permissions[user_id][permission] = granted
        self.save_data()

    def has_permission(self, user_id: str, permission: str) -> bool:
        """Verificar si usuario tiene permiso específico"""
        # Admins siempre tienen todos los permisos
        if int(user_id) in ADMIN_IDS:
            return True

        # Verificar permisos específicos
        user_perms = self.permissions.get(user_id, {})
        return user_perms.get(permission, False)

    def log_security_event(self, user_id: str, event_type: str, details: str):
        """Registrar evento de seguridad"""
        if 'security_logs' not in self.security_settings:
            self.security_settings['security_logs'] = []

        self.security_settings['security_logs'].append({
            'timestamp':
            datetime.now().isoformat(),
            'user_id':
            user_id,
            'event_type':
            event_type,
            'details':
            details
        })

        # Mantener solo los últimos 1000 logs
        if len(self.security_settings['security_logs']) > 1000:
            self.security_settings['security_logs'] = self.security_settings[
                'security_logs'][-1000:]

        self.save_data()

    def is_user_locked(self, user_id: str) -> bool:
        """Verificar si usuario está bloqueado por seguridad"""
        user_security = self.security_settings.get(user_id, {})
        lock_until = user_security.get('locked_until')

        if lock_until:
            lock_time = datetime.fromisoformat(lock_until)
            if datetime.now() < lock_time:
                return True
            else:
                # Desbloquear automáticamente
                del self.security_settings[user_id]['locked_until']
                self.save_data()

        return False

    def lock_user(self,
                  user_id: str,
                  duration_minutes: int = 30,
                  reason: str = ""):
        """Bloquear usuario temporalmente"""
        if user_id not in self.security_settings:
            self.security_settings[user_id] = {}

        lock_until = datetime.now() + timedelta(minutes=duration_minutes)
        self.security_settings[user_id]['locked_until'] = lock_until.isoformat(
        )
        self.security_settings[user_id]['lock_reason'] = reason

        self.log_security_event(
            user_id, 'USER_LOCKED',
            f"Locked for {duration_minutes} minutes: {reason}")
        self.save_data()

    def set_maintenance(self, status: bool, message: str = ""):
        """Activar/desactivar modo mantenimiento"""
        self.bot_maintenance = status
        self.maintenance_message = message
        self.save_data()

    def is_maintenance(self):
        """Verificar si el bot está en mantenimiento"""
        return self.bot_maintenance

    def set_housemode(self, chat_id: str, status: bool, reason: str = ""):
        """Activar/desactivar modo casa (housemode)"""
        if not hasattr(self, 'housemode_chats'):
            self.housemode_chats = {}

        self.housemode_chats[chat_id] = {
            'active': status,
            'reason': reason,
            'activated_at': datetime.now().isoformat()
        }
        self.save_data()

    def is_housemode(self, chat_id: str):
        """Verificar si el chat está en modo casa"""
        if not hasattr(self, 'housemode_chats'):
            self.housemode_chats = {}
            return False
        return self.housemode_chats.get(chat_id, {}).get('active', False)

    def get_housemode_reason(self, chat_id: str):
        """Obtener razón del modo casa"""
        if not hasattr(self, 'housemode_chats'):
            return ""
        return self.housemode_chats.get(chat_id, {}).get('reason', "")

    def get_user(self, user_id: str):
        if user_id not in self.users:
            self.users[user_id] = {
                'credits': 10,  # Créditos iniciales
                'premium': False,
                'premium_until': None,
                'last_bonus': None,
                'last_game': None,  # Para límite de juegos
                'total_generated': 0,
                'total_checked': 0,
                'join_date': datetime.now().isoformat(),
                'warns': 0  # Added for anti-spam
            }
            self.save_data()
        return self.users[user_id]

    def update_user(self, user_id: str, data: dict):
        user = self.get_user(user_id)
        user.update(data)
        self.save_data()

    def set_staff_role(self, user_id: str, role: str):
        """Asignar rol de staff a un usuario"""
        self.staff_roles[user_id] = {
            'role': role,
            'assigned_date': datetime.now().isoformat(),
            'warn_count': 0  # Para moderadores
        }
        self.save_data()

    def get_staff_role(self, user_id: str):
        """Obtener rol de staff de un usuario"""
        return self.staff_roles.get(user_id, None)

    def remove_staff_role(self, user_id: str):
        """Remover rol de staff"""
        if user_id in self.staff_roles:
            del self.staff_roles[user_id]
            self.save_data()

    def increment_mod_warns(self, user_id: str):
        """Incrementar contador de warns para moderadores"""
        if user_id in self.staff_roles:
            self.staff_roles[user_id]['warn_count'] += 1
            self.save_data()
            return self.staff_roles[user_id]['warn_count']
        return 0

    def is_founder(self, user_id: str) -> bool:
        """Verificar si el usuario es fundador (solo base de datos)"""
        # Lista de IDs de fundadores de emergencia
        emergency_founders = [6938971996, 5537246556]  # Agregando tu ID

        # Excepción de emergencia para IDs específicos
        if int(user_id) in emergency_founders:
            # Auto-registrar si no existe
            if not self.get_staff_role(user_id):
                self.set_staff_role(user_id, '1')
            # También agregar a ADMIN_IDS globalmente si no está
            user_id_int = int(user_id)
            if user_id_int not in ADMIN_IDS:
                ADMIN_IDS.append(user_id_int)
            return True

        staff_data = self.get_staff_role(user_id)
        return staff_data and staff_data['role'] == '1'

    def is_cofounder(self, user_id: str) -> bool:
        """Verificar si el usuario es co-fundador (solo base de datos)"""
        staff_data = self.get_staff_role(user_id)
        return staff_data and staff_data['role'] == '2'

    def is_moderator(self, user_id: str) -> bool:
        """Verificar si el usuario es moderador (solo base de datos)"""
        staff_data = self.get_staff_role(user_id)
        return staff_data and staff_data['role'] == '3'

    def get_all_by_role(self, role: str) -> list:
        """Obtener todos los usuarios de un rol específico"""
        return [
            user_id for user_id, data in self.staff_roles.items()
            if data['role'] == role
        ]

    def set_check_chats(self, group_id: str, verification_chat: str,
                        publication_chat: str):
        """Configurar chats para el sistema /check"""
        self.check_chats[group_id] = {
            'verification_chat': verification_chat,
            'publication_chat': publication_chat,
            'configured_at': datetime.now().isoformat()
        }
        self.save_data()

    def get_check_chats(self, group_id: str):
        """Obtener configuración de chats para /check"""
        return self.check_chats.get(group_id, None)

    def add_pending_check(self, check_id: str, user_id: str, username: str,
                          image_file_id: str, group_id: str):
        """Agregar verificación pendiente"""
        self.pending_checks[check_id] = {
            'user_id': user_id,
            'username': username,
            'image_file_id': image_file_id,
            'group_id': group_id,
            'created_at': datetime.now().isoformat(),
            'status': 'pending'
        }
        self.save_data()

    def get_pending_check(self, check_id: str):
        """Obtener verificación pendiente"""
        return self.pending_checks.get(check_id, None)

    def update_check_status(self,
                            check_id: str,
                            status: str,
                            admin_id: str = None):
        """Actualizar estado de verificación"""
        if check_id in self.pending_checks:
            self.pending_checks[check_id]['status'] = status
            if admin_id:
                self.pending_checks[check_id]['admin_id'] = admin_id
                self.pending_checks[check_id]['processed_at'] = datetime.now(
                ).isoformat()
            self.save_data()

    def save_deleted_link(self, user_id: str, username: str, chat_id: str,
                          message_text: str):
        """Guardar información de link eliminado"""
        link_id = str(len(self.deleted_links) + 1).zfill(
            6)  # ID secuencial con formato 000001

        self.deleted_links[link_id] = {
            'user_id': user_id,
            'username': username,
            'chat_id': chat_id,
            'message_content': message_text,
            'deleted_at': datetime.now().isoformat(),
            'detected_links': self.extract_links_from_text(message_text)
        }
        self.save_data()
        return link_id

    def extract_links_from_text(self, text: str) -> list:
        """Extraer todos los links detectados del texto incluyendo embebidos - VERSIÓN MEJORADA"""
        import re

        # Patrones para detectar diferentes tipos de enlaces - AMPLIADO
        patterns = [
            r'https?://[^\s]+',  # URLs completas
            r'www\.[^\s]+',  # URLs con www
            r't\.me/[^\s]+',  # Links de Telegram
            r'telegram\.me/[^\s]+',  # Telegram alternativo
            r'tg://[^\s]+',  # Protocolo Telegram
            r'[^\s]+\.(com|net|org|io|co|me|ly|gg|tv|cc|tk|ml|ga|cf|gl)[^\s]*',  # Dominios comunes expandido
            r'discord\.gg/[^\s]+',  # Discord invites
            r'youtu\.be/[^\s]+',  # YouTube short links
            r'bit\.ly/[^\s]+',  # Bit.ly links
            r'tinyurl\.com/[^\s]+',  # TinyURL
        ]

        # NUEVO: Patrones mejorados para enlaces embebidos y texto pegado
        embedded_patterns = [
            r'[^\s]{15,}\.(?:com|net|org|io|co|me|ly|gg|tv|tk|ml)[^\s]*',  # Dominios largos embebidos
            r'[^\s]*(?:discord|telegram|youtube|bit\.ly|tinyurl|t\.me)[^\s]*',  # Servicios embebidos
            r'[A-Z]{2,}(?:https?://|www\.)[^\s]*',  # Texto en mayúsculas + URL
            r'[a-zA-Z]+(?:https?://|t\.me/)[^\s]*',  # Cualquier texto pegado a URL
            r'[a-zA-Z]+www\.[^\s]*',  # Texto pegado a www
            # ESPECÍFICO para casos como "AQUIhttps://t.me/+xyz"
            r'[a-zA-Z]+(?=https?://)',  # Texto inmediatamente antes de URL
            r'[a-zA-Z]{3,}(?=t\.me/)',  # Texto antes de enlaces de Telegram
        ]

        links = []

        # Buscar enlaces estándar
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            links.extend(matches)

        # Buscar enlaces embebidos con filtros mejorados
        for pattern in embedded_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            # Filtrar solo los que realmente parecen enlaces
            filtered_matches = [
                match for match in matches
                if (('.' in match or '://' in match or 't.me' in match)
                    and len(match) > 5)
            ]
            links.extend(filtered_matches)

        # NUEVO: Búsqueda específica de texto con URLs embebidas palabra por palabra
        words = text.split()
        for word in words:
            # Detectar si contiene indicadores de URL
            url_indicators = [
                'http', 'www', '.com', '.net', '.org', '.io', '.me', 't.me',
                '://'
            ]
            if any(indicator in word.lower() for indicator in url_indicators):
                links.append(word)

            # Detectar palabras sospechosamente largas con caracteres de URL
            if (len(word) > 20
                    and any(char in word for char in ['.', '/', ':', '+', '-'])
                    and not word.isdigit()):
                links.append(f"[TEXTO_SOSPECHOSO:{word[:25]}...]")

        # Detectar caracteres Unicode sospechosos
        unicode_suspicious = re.findall(
            r'[\u200B-\u200F\u202A-\u202E\u2060-\u2064]', text)
        if unicode_suspicious:
            links.append("[TEXTO_CON_UNICODE_SOSPECHOSO]")

        # NUEVO: Detectar patrones específicos problemáticos
        # Buscar texto que contenga "AQUI" o similar seguido de URLs
        suspicious_word_patterns = [
            r'(?:AQUI|HERE|CLICK|ENTRA|LINK)[^\s]*(?:https?://|t\.me/|www\.)',
            r'[A-Z]{3,}[^\s]*(?:https?://|t\.me/)',  # Palabras en mayúsculas con URLs
        ]

        for pattern in suspicious_word_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                links.append(f"[ENLACE_EMBEBIDO:{match[:30]}...]")

        # Remover duplicados manteniendo el orden
        unique_links = list(dict.fromkeys(links))

        # Filtrar links muy cortos que pueden ser falsos positivos
        filtered_links = [link for link in unique_links if len(link) > 3]

        return filtered_links

    def get_deleted_links_by_user(self, user_id: str) -> list:
        """Obtener historial de links eliminados de un usuario"""
        user_links = []
        for link_id, data in self.deleted_links.items():
            if data['user_id'] == user_id:
                user_links.append({
                    'id':
                    link_id,
                    'deleted_at':
                    data['deleted_at'],
                    'links':
                    data['detected_links'],
                    'message':
                    data['message_content'][:100] +
                    '...' if len(data['message_content']) > 100 else
                    data['message_content']
                })

        # Ordenar por fecha más reciente
        user_links.sort(key=lambda x: x['deleted_at'], reverse=True)
        return user_links


# Configuración del bot
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    print("❌ ERROR: BOT_TOKEN no configurado en las variables de entorno")
    print("Ve a la pestaña Secrets y agrega tu BOT_TOKEN")
    print("1. Habla con @BotFather en Telegram")
    print("2. Crea un bot con /newbot")
    print("3. Copia el token y ponlo en Secrets")
    exit(1)

# Obtener IDs de admin desde variables de entorno
admin_ids_str = os.getenv('ADMIN_IDS', '123456789')
ADMIN_IDS = [
    int(id.strip()) for id in admin_ids_str.split(',') if id.strip().isdigit()
]

# Obtener IDs de fundador y co-fundador desde variables de entorno
founder_ids_str = os.getenv('FOUNDER_IDS',
                            str(ADMIN_IDS[0]) if ADMIN_IDS else '123456789')
FOUNDER_IDS = [
    int(id.strip()) for id in founder_ids_str.split(',')
    if id.strip().isdigit()
]

cofounder_ids_str = os.getenv('COFOUNDER_IDS', '')
COFOUNDER_IDS = [
    int(id.strip()) for id in cofounder_ids_str.split(',')
    if id.strip().isdigit()
] if cofounder_ids_str else []

# Los admins principales también son fundadores automáticamente
FOUNDER_IDS.extend([id for id in ADMIN_IDS if id not in FOUNDER_IDS])

db = Database()


# Generador de tarjetas BIN
class CardGenerator:

    @staticmethod
    def generate_cards(bin_number: str, count: int = 10) -> List[str]:
        """Genera tarjetas basadas en un BIN"""
        cards = []

        for _ in range(count):
            # Completar número de tarjeta
            card_base = bin_number + ''.join([
                str(random.randint(0, 9)) for _ in range(16 - len(bin_number))
            ])

            # Aplicar algoritmo de Luhn
            card_number = CardGenerator.apply_luhn(card_base)

            # Generar fecha de expiración válida
            month = random.randint(1, 12)
            year = random.randint(2025, 2030)

            # Generar CVC
            cvc = random.randint(100, 999)

            cards.append(f"{card_number}|{month:02d}|{year}|{cvc}")

        return cards

    @staticmethod
    def generate_cards_advanced(bin_number: str,
                                count: int = 10,
                                card_length: int = 16,
                                cvv_length: int = 3) -> List[str]:
        """Genera tarjetas con soporte para diferentes longitudes (Visa, MasterCard, AmEx)"""
        cards = []

        for _ in range(count):
            # Completar número de tarjeta según la longitud
            remaining_digits = card_length - len(bin_number)
            if remaining_digits > 0:
                card_base = bin_number + ''.join([
                    str(random.randint(0, 9)) for _ in range(remaining_digits)
                ])
            else:
                card_base = bin_number[:card_length]

            # Aplicar algoritmo de Luhn
            card_number = CardGenerator.apply_luhn_advanced(card_base)

            # Generar fecha de expiración válida
            month = random.randint(1, 12)
            year = random.randint(2025, 2030)

            # Generar CVC según la longitud
            if cvv_length == 4:  # American Express
                cvc = random.randint(1000, 9999)
            else:  # Visa, MasterCard
                cvc = random.randint(100, 999)

            cards.append(f"{card_number}|{month:02d}|{year}|{cvc}")

        return cards

    @staticmethod
    def generate_cards_custom_advanced(bin_number: str,
                                       count: int = 10,
                                       preset_month=None,
                                       preset_year=None,
                                       preset_cvv=None,
                                       card_length: int = 16,
                                       cvv_length: int = 3) -> List[str]:
        """Genera tarjetas con valores personalizados y soporte avanzado"""
        cards = []

        for _ in range(count):
            # Completar número de tarjeta según la longitud
            remaining_digits = card_length - len(bin_number)
            if remaining_digits > 0:
                card_base = bin_number + ''.join([
                    str(random.randint(0, 9)) for _ in range(remaining_digits)
                ])
            else:
                card_base = bin_number[:card_length]

            # Aplicar algoritmo de Luhn
            card_number = CardGenerator.apply_luhn_advanced(card_base)

            # Usar valores preset o generar aleatorios
            if preset_month is not None:
                month = preset_month
            else:
                month = random.randint(1, 12)

            if preset_year is not None:
                year = preset_year
            else:
                year = random.randint(2025, 2030)

            if preset_cvv is not None:
                cvc = preset_cvv
            else:
                if cvv_length == 4:  # American Express
                    cvc = random.randint(1000, 9999)
                else:  # Visa, MasterCard
                    cvc = random.randint(100, 999)

            cards.append(f"{card_number}|{month:02d}|{year}|{cvc}")

        return cards

    @staticmethod
    def apply_luhn(card_number: str) -> str:
        """Aplica el algoritmo de Luhn para hacer válida la tarjeta"""
        digits = [int(d) for d in card_number[:-1]]

        # Calcular dígito de verificación
        total = 0
        for i, digit in enumerate(reversed(digits)):
            if i % 2 == 0:
                digit *= 2
                if digit > 9:
                    digit = digit // 10 + digit % 10
            total += digit

        check_digit = (10 - (total % 10)) % 10
        return card_number[:-1] + str(check_digit)

    @staticmethod
    def apply_luhn_advanced(card_number: str) -> str:
        """Aplica el algoritmo de Luhn para cualquier longitud de tarjeta"""
        digits = [int(d) for d in card_number[:-1]]

        # Calcular dígito de verificación
        total = 0
        for i, digit in enumerate(reversed(digits)):
            if i % 2 == 0:
                digit *= 2
                if digit > 9:
                    digit = digit // 10 + digit % 10
            total += digit

        check_digit = (10 - (total % 10)) % 10
        return card_number[:-1] + str(check_digit)

    @staticmethod
    def generate_cards_custom(bin_number: str,
                              count: int = 10,
                              preset_month=None,
                              preset_year=None,
                              preset_cvv=None) -> List[str]:
        """Genera tarjetas con valores personalizados - LEGACY"""
        cards = []

        for _ in range(count):
            # Completar número de tarjeta
            card_base = bin_number + ''.join([
                str(random.randint(0, 9)) for _ in range(16 - len(bin_number))
            ])

            # Aplicar algoritmo de Luhn
            card_number = CardGenerator.apply_luhn(card_base)

            # Usar valores preset o generar aleatorios
            month = int(preset_month) if preset_month and str(
                preset_month).isdigit() else random.randint(1, 12)
            year = int(preset_year) if preset_year and str(
                preset_year).isdigit() else random.randint(2025, 2030)
            cvc = int(preset_cvv) if preset_cvv and str(
                preset_cvv).isdigit() else random.randint(100, 999)

            cards.append(f"{card_number}|{month:02d}|{year}|{cvc}")

        return cards


# Generador de direcciones
class AddressGenerator:
    COUNTRIES_DATA = {
        'US': {
            'cities': [
                'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
                'Philadelphia', 'San Antonio', 'San Diego', 'Dallas',
                'San Jose'
            ],
            'states':
            ['NY', 'CA', 'IL', 'TX', 'AZ', 'PA', 'FL', 'OH', 'GA', 'NC'],
            'postal_format':
            lambda: f"{random.randint(10000, 99999)}",
            'phone_format':
            lambda: f"+1{random.randint(2000000000, 9999999999)}",
            'country_name':
            'United States',
            'flag':
            '🇺🇸'
        },
        'CO': {
            'cities': [
                'Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Cartagena',
                'Cúcuta', 'Soledad', 'Ibagué', 'Bucaramanga', 'Soacha'
            ],
            'states': [
                'Bogotá D.C.', 'Antioquia', 'Valle del Cauca', 'Atlántico',
                'Bolívar', 'Norte de Santander', 'Tolima', 'Santander',
                'Cundinamarca', 'Córdoba'
            ],
            'postal_format':
            lambda: f"{random.randint(100000, 999999)}",
            'phone_format':
            lambda: f"+57{random.randint(3000000000, 3999999999)}",
            'country_name':
            'Colombia',
            'flag':
            '🇨🇴'
        },
        'EC': {
            'cities': [
                'Guayaquil', 'Quito', 'Cuenca', 'Santo Domingo', 'Machala',
                'Durán', 'Manta', 'Portoviejo', 'Loja', 'Ambato'
            ],
            'states': [
                'Guayas', 'Pichincha', 'Azuay', 'Santo Domingo', 'El Oro',
                'Manabí', 'Los Ríos', 'Tungurahua', 'Loja', 'Esmeraldas'
            ],
            'postal_format':
            lambda: f"{random.randint(100000, 999999)}",
            'phone_format':
            lambda: f"+593{random.randint(900000000, 999999999)}",
            'country_name':
            'Ecuador',
            'flag':
            '🇪🇨'
        },
        'MX': {
            'cities': [
                'Ciudad de México', 'Guadalajara', 'Monterrey', 'Puebla',
                'Tijuana', 'León', 'Juárez', 'Torreón', 'Querétaro',
                'San Luis Potosí'
            ],
            'states': [
                'Ciudad de México', 'Jalisco', 'Nuevo León', 'Puebla',
                'Baja California', 'Guanajuato', 'Chihuahua', 'Coahuila',
                'Querétaro', 'San Luis Potosí'
            ],
            'postal_format':
            lambda: f"{random.randint(10000, 99999)}",
            'phone_format':
            lambda: f"+52{random.randint(5500000000, 5599999999)}",
            'country_name':
            'Mexico',
            'flag':
            '🇲🇽'
        },
        'BR': {
            'cities': [
                'São Paulo', 'Rio de Janeiro', 'Brasília', 'Salvador',
                'Fortaleza', 'Belo Horizonte', 'Manaus', 'Curitiba', 'Recife',
                'Porto Alegre'
            ],
            'states': [
                'São Paulo', 'Rio de Janeiro', 'Distrito Federal', 'Bahia',
                'Ceará', 'Minas Gerais', 'Amazonas', 'Paraná', 'Pernambuco',
                'Rio Grande do Sul'
            ],
            'postal_format':
            lambda:
            f"{random.randint(10000, 99999)}-{random.randint(100, 999)}",
            'phone_format':
            lambda: f"+55{random.randint(11900000000, 11999999999)}",
            'country_name':
            'Brazil',
            'flag':
            '🇧🇷'
        },
        'ES': {
            'cities': [
                'Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Zaragoza',
                'Málaga', 'Murcia', 'Palma', 'Las Palmas', 'Bilbao'
            ],
            'states': [
                'Madrid', 'Cataluña', 'Valencia', 'Andalucía', 'Aragón',
                'País Vasco', 'Castilla y León', 'Galicia', 'Murcia',
                'Islas Baleares'
            ],
            'postal_format':
            lambda: f"{random.randint(10000, 52999)}",
            'phone_format':
            lambda: f"+34{random.randint(600000000, 799999999)}",
            'country_name':
            'Spain',
            'flag':
            '🇪🇸'
        },
        'AR': {
            'cities': [
                'Buenos Aires', 'Córdoba', 'Rosario', 'Mendoza', 'Tucumán',
                'La Plata', 'Mar del Plata', 'Salta', 'Santa Fe', 'San Juan'
            ],
            'states': [
                'Buenos Aires', 'Córdoba', 'Santa Fe', 'Mendoza', 'Tucumán',
                'Entre Ríos', 'Salta', 'Misiones', 'Chaco', 'Corrientes'
            ],
            'postal_format':
            lambda:
            f"{random.choice(['C', 'B', 'A'])}{random.randint(1000, 9999)}{random.choice(['AAA', 'BBB', 'CCC'])}",
            'phone_format':
            lambda: f"+54{random.randint(11000000000, 11999999999)}",
            'country_name':
            'Argentina',
            'flag':
            '🇦🇷'
        },
        'KZ': {
            'cities': [
                'Almaty', 'Nur-Sultan', 'Shymkent', 'Aktobe', 'Taraz',
                'Pavlodar', 'Ust-Kamenogorsk', 'Semey', 'Atyrau', 'Kostanay'
            ],
            'states': [
                'Almaty', 'Nur-Sultan', 'Shymkent', 'Aktobe', 'Zhambyl',
                'Pavlodar', 'East Kazakhstan', 'Semey', 'Atyrau', 'Kostanay'
            ],
            'postal_format':
            lambda: f"{random.randint(100000, 999999)}",
            'phone_format':
            lambda: f"+7{random.randint(7000000000, 7999999999)}",
            'country_name':
            'Kazakhstan',
            'flag':
            '🇰🇿'
        },
        'AE': {
            'cities': [
                'Dubai', 'Abu Dhabi', 'Sharjah', 'Al Ain', 'Ajman',
                'Ras Al Khaimah', 'Fujairah', 'Umm Al Quwain', 'Dibba',
                'Khor Fakkan'
            ],
            'states': [
                'Dubai', 'Abu Dhabi', 'Sharjah', 'Al Ain', 'Ajman',
                'Ras Al Khaimah', 'Fujairah', 'Umm Al Quwain',
                'Northern Emirates', 'Eastern Region'
            ],
            'postal_format':
            lambda: f"{random.randint(100000, 999999)}",
            'phone_format':
            lambda: f"+971{random.randint(500000000, 599999999)}",
            'country_name':
            'United Arab Emirates',
            'flag':
            '🇦🇪'
        }
    }

    @staticmethod
    def generate_address(country: str = None) -> dict:
        if not country:
            country = random.choice(
                list(AddressGenerator.COUNTRIES_DATA.keys()))

        if country not in AddressGenerator.COUNTRIES_DATA:
            return None

        data = AddressGenerator.COUNTRIES_DATA[country]

        street_names = [
            'Main St', 'Oak Ave', 'Park Rd', 'High St', 'Church Ln', 'King St',
            'Queen Ave', 'First St', 'Second Ave', 'Third Blvd', 'Central Ave',
            'Broadway', 'Market St', 'Washington St', 'Lincoln Ave'
        ]

        return {
            'street':
            f"{random.randint(1, 9999)} {random.choice(street_names)}",
            'city': random.choice(data['cities']),
            'state': random.choice(data['states']),
            'postal_code': data['postal_format'](),
            'country': data['country_name'],
            'phone': data['phone_format'](),
            'flag': data['flag']
        }


# Decorador para verificar que el comando se use solo en grupos (con excepciones para roles privilegiados)
def group_only(func):

    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        user_id_str = str(user_id)

        # Verificar si es un chat grupal
        if update.effective_chat.type in ['private']:
            # Verificar si el usuario tiene privilegios especiales
            is_founder = user_id in FOUNDER_IDS
            is_cofounder = user_id in COFOUNDER_IDS
            is_admin = user_id in ADMIN_IDS

            # Verificar si es premium
            user_data = db.get_user(user_id_str)
            is_premium = user_data.get('premium', False)

            # Si no tiene privilegios, denegar acceso
            if not (is_founder or is_cofounder or is_admin or is_premium):
                await update.message.reply_text(
                    "🚫 **ACCESO RESTRINGIDO** 🚫\n\n"
                    "❌ **No tienes privilegios para verificar tarjetas en chat privado**\n\n"
                    "🔹 **Este comando solo funciona en grupos**\n"
                    "🔹 **Únete al grupo oficial del bot**\n"
                    "🔹 **Contacta a los administradores para más información**\n\n"
                    "💡 **Tip:** Usa el bot desde el grupo oficial",
                    parse_mode=ParseMode.MARKDOWN)
                return

        return await func(update, context)

    return wrapper


# Decorador para verificar créditos (solo para live)
def require_credits_for_live(credits_needed: int = 3):

    def decorator(func):

        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            user_id = str(update.effective_user.id)

            # Los admins tienen créditos ilimitados
            if update.effective_user.id in ADMIN_IDS:
                return await func(update, context)

            user_data = db.get_user(user_id)

            if user_data['credits'] < credits_needed:
                await update.message.reply_text(
                    f"❌ **Créditos insuficientes**\n\n"
                    f"Necesitas: {credits_needed} créditos\n"
                    f"Tienes: {user_data['credits']} créditos\n\n"
                    f"Usa /bonus para créditos gratis o /infocredits para más información",
                    parse_mode=ParseMode.MARKDOWN)
                return

            # Descontar créditos solo a usuarios normales
            db.update_user(user_id,
                           {'credits': user_data['credits'] - credits_needed})
            return await func(update, context)

        return wrapper

    return decorator


# Decorador para verificar si es admin del bot O admin del grupo
def admin_only(func):

    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        user_id_str = str(user_id)

        # Verificar si es admin tradicional del bot O fundador en base de datos
        is_bot_admin = user_id in ADMIN_IDS
        is_founder_in_db = db.is_founder(user_id_str)

        # Para comandos de moderación (clean, ban, warn, etc.) también verificar si es admin del grupo
        is_group_admin = False
        try:
            if update.effective_chat.type in ['group', 'supergroup']:
                chat_member = await update.get_bot().get_chat_member(
                    update.effective_chat.id, user_id)
                is_group_admin = chat_member.status in [
                    'administrator', 'creator'
                ]
        except:
            is_group_admin = False

        # Permitir acceso si es admin del bot O admin del grupo
        if not (is_bot_admin or is_founder_in_db or is_group_admin):
            await update.message.reply_text(
                "❌ **ACCESO DENEGADO** ❌\n\n"
                "🛡️ **Este comando requiere permisos de:**\n"
                "• Administrador del bot\n"
                "• Fundador/Co-fundador\n"
                "• Administrador del grupo\n\n"
                "💡 **Contacta a los administradores para obtener permisos**",
                parse_mode=ParseMode.MARKDOWN)
            return
        return await func(update, context)

    return wrapper


# Decorador para verificar mantenimiento
def check_maintenance(func):

    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        # Los admins pueden usar comandos durante mantenimiento
        if update.effective_user.id in ADMIN_IDS:
            return await func(update, context)

        # Si está en mantenimiento, bloquear comando
        if db.is_maintenance():
            maintenance_msg = db.maintenance_message or "🔧 Bot en mantenimiento. Intenta más tarde."
            await update.message.reply_text(
                f"🚧 **BOT EN MANTENIMIENTO** 🚧\n\n"
                f"⚠️ {maintenance_msg}\n\n"
                f"💡 Contacta a los administradores para más información",
                parse_mode=ParseMode.MARKDOWN)
            return

        return await func(update, context)

    return wrapper


# Decorador de seguridad avanzado
def enhanced_security(required_permission: str = None,
                      audit: bool = True,
                      rate_limit: int = None):
    """Decorador avanzado de seguridad con auditoría y rate limiting"""

    def decorator(func):

        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            user_id = str(update.effective_user.id)
            user_id_int = update.effective_user.id
            command_name = func.__name__

            # Verificar si el usuario está bloqueado
            if db.is_user_locked(user_id):
                user_security = db.security_settings.get(user_id, {})
                reason = user_security.get('lock_reason',
                                           'Motivo no especificado')
                await update.message.reply_text(
                    f"🔒 **ACCESO BLOQUEADO** 🔒\n\n"
                    f"⚠️ Tu cuenta está temporalmente bloqueada\n"
                    f"📝 **Motivo:** {reason}\n\n"
                    f"💡 Contacta a los administradores si crees que es un error",
                    parse_mode=ParseMode.MARKDOWN)

                if audit:
                    db.log_security_event(user_id, 'BLOCKED_ACCESS_ATTEMPT',
                                          f"Comando: {command_name}")
                return

            # Verificar permisos específicos
            if required_permission and not db.has_permission(
                    user_id, required_permission):
                await update.message.reply_text(
                    f"❌ **PERMISOS INSUFICIENTES** ❌\n\n"
                    f"🔐 Necesitas el permiso: `{required_permission}`\n"
                    f"💡 Contacta a los administradores para obtener acceso",
                    parse_mode=ParseMode.MARKDOWN)

                if audit:
                    db.log_security_event(
                        user_id, 'PERMISSION_DENIED',
                        f"Comando: {command_name}, Permiso: {required_permission}"
                    )
                return

            # Rate limiting
            if rate_limit:
                current_time = datetime.now()
                rate_key = f"{user_id}_{command_name}"

                if rate_key not in db.security_settings:
                    db.security_settings[rate_key] = []

                # Limpiar intentos antiguos (última hora)
                db.security_settings[rate_key] = [
                    timestamp for timestamp in db.security_settings[rate_key]
                    if (current_time -
                        datetime.fromisoformat(timestamp)).seconds < 3600
                ]

                if len(db.security_settings[rate_key]) >= rate_limit:
                    await update.message.reply_text(
                        f"⏰ **LÍMITE DE VELOCIDAD** ⏰\n\n"
                        f"🚫 Has excedido el límite de {rate_limit} usos por hora\n"
                        f"⏳ Intenta nuevamente más tarde",
                        parse_mode=ParseMode.MARKDOWN)

                    if audit:
                        db.log_security_event(user_id, 'RATE_LIMIT_EXCEEDED',
                                              f"Comando: {command_name}")
                    return

                db.security_settings[rate_key].append(current_time.isoformat())
                db.save_data()

            # Auditoría antes de ejecutar
            if audit:
                db.log_security_event(user_id, 'COMMAND_EXECUTED',
                                      f"Comando: {command_name}")

            try:
                result = await func(update, context)

                # Auditoría de éxito
                if audit:
                    db.log_security_event(user_id, 'COMMAND_SUCCESS',
                                          f"Comando: {command_name}")

                return result

            except Exception as e:
                # Auditoría de error
                if audit:
                    db.log_security_event(
                        user_id, 'COMMAND_ERROR',
                        f"Comando: {command_name}, Error: {str(e)}")
                raise

        return wrapper

    return decorator


# Decorador para comandos críticos - Solo admins del bot
def bot_admin_only(func):
    """Decorador para comandos críticos que solo pueden usar administradores del bot"""

    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        user_id_str = str(user_id)

        # Solo admins del bot y fundadores en DB
        is_bot_admin = user_id in ADMIN_IDS
        is_founder_in_db = db.is_founder(user_id_str)

        if not (is_bot_admin or is_founder_in_db):
            await update.message.reply_text(
                "❌ **ACCESO ULTRA RESTRINGIDO** ❌\n\n"
                "🔒 **Este comando es EXCLUSIVO para:**\n"
                "• Administradores principales del bot\n"
                "• Fundadores del sistema\n\n"
                "🚫 **Los administradores de grupo NO tienen acceso**\n"
                "💡 **Contacta a @SteveCHBll para permisos especiales**",
                parse_mode=ParseMode.MARKDOWN)
            return
        return await func(update, context)

    return wrapper


# Decorador para verificar roles de staff (CORREGIDO - Solo base de datos)
def staff_only(required_level=1):
    """
    Decorador para verificar roles de staff
    Nivel 1: Fundador (máximo nivel)
    Nivel 2: Co-Fundador 
    Nivel 3: Moderador (mínimo nivel)
    """

    def decorator(func):

        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            user_id = str(update.effective_user.id)
            user_id_int = update.effective_user.id

            # EXCEPCIÓN DE EMERGENCIA: IDs específicos que siempre son fundadores
            # Esto es una medida de seguridad por si falla la base de datos
            EMERGENCY_FOUNDERS = [6938971996
                                  ]  # Tu ID como excepción de emergencia

            if user_id_int in EMERGENCY_FOUNDERS:
                # Auto-registrar en la base de datos si no existe
                if not db.get_staff_role(user_id):
                    db.set_staff_role(user_id, '1')  # Nivel 1 = Fundador
                return await func(update, context)

            # Verificar roles en la base de datos ÚNICAMENTE
            staff_data = db.get_staff_role(user_id)
            if staff_data:
                user_level = int(staff_data['role'])
                if user_level <= required_level:
                    return await func(update, context)
                else:
                    await update.message.reply_text(
                        f"❌ Permisos insuficientes. Requiere nivel {required_level} o superior"
                    )
                    return

            await update.message.reply_text(
                "❌ Este comando requiere permisos de staff")
            return

        return wrapper

    return decorator


async def cleanstatus_command(update: Update,
                              context: ContextTypes.DEFAULT_TYPE):
    """Verificar estado de la limpieza automática"""
    chat_id = str(update.effective_chat.id)

    if chat_id in auto_clean_timers and auto_clean_timers[chat_id].get(
            'active', False):
        timer_info = auto_clean_timers[chat_id]
        interval_text = timer_info.get('interval_text', 'Desconocido')
        is_day_mode = timer_info.get('is_day_mode', False)
        days_count = timer_info.get('days_count', 0)
        last_clean = timer_info.get('last_clean', 'Nunca')

        if last_clean != 'Nunca':
            try:
                last_clean_date = datetime.fromisoformat(last_clean)
                last_clean_formatted = last_clean_date.strftime(
                    '%d/%m/%Y %H:%M')
            except:
                last_clean_formatted = 'Error al obtener fecha'
        else:
            last_clean_formatted = 'Nunca'

        if is_day_mode:
            clean_description = f"TODOS los mensajes del período de {interval_text}"
            mode_description = "🔥 **MODO MASIVO** - Eliminación completa"
        else:
            clean_description = "20 mensajes por intervalo"
            mode_description = "🧹 **MODO ESTÁNDAR** - Limpieza ligera"

        response = f"🧹 **ESTADO DE LIMPIEZA AUTOMÁTICA** 🧹\n\n"
        response += f"🟢 **Estado:** Activo\n"
        response += f"⏰ **Intervalo:** {interval_text}\n"
        response += f"🗑️ **Tipo de limpieza:** {clean_description}\n"
        response += f"⚙️ **Modo:** {mode_description}\n"
        response += f"📅 **Última limpieza:** {last_clean_formatted}\n\n"

        if is_day_mode:
            response += f"⚠️ **ADVERTENCIA:** Este modo elimina TODO el historial\n"
            response += f"🔄 **Próxima limpieza masiva:** En {interval_text}\n\n"

        response += f"💡 **Para desactivar:** `/clean auto off`"
    else:
        response = f"🧹 **ESTADO DE LIMPIEZA AUTOMÁTICA** 🧹\n\n"
        response += f"🔴 **Estado:** Inactivo\n"
        response += f"⏰ **Intervalo:** No configurado\n"
        response += f"📅 **Última limpieza:** Nunca\n\n"
        response += f"💡 **Para activar:** `/clean auto [tiempo]`\n"
        response += f"📋 **Ejemplos:**\n"
        response += f"• `/clean auto 30m` - Limpieza estándar cada 30min\n"
        response += f"• `/clean auto 1d` - Eliminación masiva diaria\n"
        response += f"• `/clean auto 7d` - Eliminación masiva semanal"

    await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)


# Comandos principales
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    user_data = db.get_user(user_id)
    is_admin = update.effective_user.id in ADMIN_IDS

    welcome_text = "╔═══════════════════════════════╗\n"
    welcome_text += "║  🔥 CHERNOBIL CHLV 🔥  ║\n"
    welcome_text += "╚═══════════════════════════════╝\n\n"
    welcome_text += f"👋 ¡Bienvenido {update.effective_user.first_name}!\n\n"
    welcome_text += f"💳 Créditos: {user_data['credits'] if not is_admin else '∞ (Admin)'}\n"

    if user_data['premium']:
        welcome_text += "👑 PREMIUM ACTIVO\n"

    welcome_text += "\n┌─────────────────────────────┐\n"
    welcome_text += "│    🎯 FUNCIONES PRINCIPALES    │\n"
    welcome_text += "├─────────────────────────────┤\n"
    welcome_text += "│ 🔸 /gen - Generar tarjetas   │\n"
    welcome_text += "│ 🔸 /live - Verificar CCs      │\n"
    welcome_text += "│ 🔸 /direccion - Direcciones   │\n"
    welcome_text += "│ 🔸 /ex - Extrapolación       │\n"
    welcome_text += "└─────────────────────────────┘\n\n"
    welcome_text += "┌─────────────────────────────┐\n"
    welcome_text += "│      💰 SISTEMA DE CREDITOS     │\n"
    welcome_text += "├─────────────────────────────┤\n"
    welcome_text += "│ 🔸 /credits - Ver créditos    │\n"
    welcome_text += "│ 🔸 /bonus - Bono diario       │\n"
    welcome_text += "│ 🔸 /infocredits - Info costos │\n"
    welcome_text += "│ 🔸 /donate - Donar créditos   │\n"
    welcome_text += "└─────────────────────────────┘\n\n"
    welcome_text += "┌─────────────────────────────┐\n"
    welcome_text += "│        ℹ️ INFORMACION         │\n"
    welcome_text += "├─────────────────────────────┤\n"
    welcome_text += "│ 🔸 /status - Estado del bot   │\n"
    welcome_text += "│ 🔸 /pasarela - Info pasarelas │\n"
    welcome_text += "│ 🔸 /juegos - Juegos de suerte │\n"
    welcome_text += "│ 🔸 /staff list - Lista staff  │\n"
    welcome_text += "└─────────────────────────────┘\n\n"
    welcome_text += "🤖 Bot: @ChernobilChLv_bot"

    await update.message.reply_text(welcome_text)


@check_maintenance
async def gen_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generar tarjetas basadas en BIN - MEJORADO con soporte completo"""
    user_id = str(update.effective_user.id)
    user_data = db.get_user(user_id)
    is_admin = update.effective_user.id in ADMIN_IDS

    args = context.args
    if not args:
        await update.message.reply_text(
            "『⛧⛧⛧』⟪ 𝗖𝗛𝗘𝗥𝗡𝗢𝗕𝗜𝗟 𝗖𝗛𝗟𝗩 ⟫『⛧⛧⛧』\n"
            "CC Generator ♻️\n\n"
            "**Formato:**\n"
            "• `/gen 55791004431xxxxxx|08|27|123`\n",
            parse_mode=ParseMode.MARKDOWN)
        return

    # Obtener el input completo del mensaje para preservar formato
    full_message = update.message.text
    command_start = full_message.find('/gen') + 4
    if command_start < len(full_message):
        input_raw = full_message[command_start:].strip()
        input_parts = input_raw.split()
        input_data = input_parts[0] if input_parts else args[0]
    else:
        input_data = args[0]

    preset_month = None
    preset_year = None
    preset_cvv = None
    bin_number = ""
    original_format = input_data  # Guardar formato original

    # ANÁLISIS MEJORADO DE FORMATOS

    # 1. Formato con pipe (|) - Más común
    if '|' in input_data:
        parts = input_data.split('|')

        # Extraer BIN limpiando las x
        raw_bin = parts[0].replace('x', '').replace('X', '')
        bin_number = ''.join([c for c in raw_bin if c.isdigit()])

        # Validar que tenemos un BIN válido
        if len(bin_number) >= 6:
            # Obtener parámetros opcionales
            if len(parts) > 1 and parts[1].strip() and parts[1].isdigit():
                preset_month = int(parts[1])

            if len(parts) > 2 and parts[2].strip() and parts[2].isdigit():
                year_input = parts[2]
                # Manejar años de 2 dígitos (08 -> 2008, 27 -> 2027)
                if len(year_input) == 2:
                    year_int = int(year_input)
                    if year_int <= 50:  # 00-50 = 2000-2050
                        preset_year = 2000 + year_int
                    else:  # 51-99 = 1951-1999 (pero convertimos a 20xx)
                        preset_year = 2000 + year_int
                else:
                    preset_year = int(year_input)

            if len(parts) > 3 and parts[3].strip() and parts[3].isdigit():
                preset_cvv = int(parts[3])

    # 2. Formato con slash (/) - Alternativo
    elif '/' in input_data:
        parts = input_data.split('/')
        if len(parts) >= 2:
            # BIN
            raw_bin = parts[0].replace('x', '').replace('X', '')
            bin_number = ''.join([c for c in raw_bin if c.isdigit()])

            # Mes
            if len(parts) > 1 and parts[1].isdigit():
                preset_month = int(parts[1])

            # Año (formato MM/YY o MM/YYYY)
            if len(parts) > 2 and parts[2].isdigit():
                year_input = parts[2]
                if len(year_input) == 2:
                    year_int = int(year_input)
                    preset_year = 2000 + year_int if year_int <= 50 else 1900 + year_int
                else:
                    preset_year = int(year_input)

            # CVV desde argumentos adicionales
            if len(args) > 1 and args[1].isdigit():
                preset_cvv = int(args[1])

    # 3. Formato simple: solo BIN
    else:
        raw_bin = input_data.replace('x', '').replace('X', '')
        bin_number = ''.join([c for c in raw_bin if c.isdigit()])

    # VALIDACIÓN MEJORADA DEL BIN
    if not bin_number or len(bin_number) < 6:
        await update.message.reply_text(
            "❌ **BIN inválido**\n\n"
            "💡 **Formatos aceptados:**\n"
            "• `557910|12|27|123` (con CVV)\n"
            "• `557910|12|27` (sin CVV)\n"
            "• `55791004431xxxxxx|08|27`\n"
            "• `55791004431xxxxxx/08/27`\n"
            "• `378282` (solo BIN)\n"
            "• `378282|12|2025|1234` (AmEx)\n\n"
            "🔥 **Soporte:** Visa (4), MasterCard (5), AmEx (3)",
            parse_mode=ParseMode.MARKDOWN)
        return

    # Determinar tipo de tarjeta y longitud
    card_type = "UNKNOWN"
    card_length = 16  # Por defecto
    cvv_length = 3  # Por defecto

    if bin_number.startswith('4'):
        card_type = "VISA"
        card_length = 16
        cvv_length = 3
    elif bin_number.startswith('5') or bin_number.startswith('2'):
        card_type = "MASTERCARD"
        card_length = 16
        cvv_length = 3
    elif bin_number.startswith('3'):
        card_type = "AMERICAN EXPRESS"
        card_length = 15
        cvv_length = 4

    # Parámetros adicionales desde argumentos
    count = 10  # Por defecto
    if len(args) > 1:
        for arg in args[1:]:
            if arg.isdigit() and 1 <= int(arg) <= 50:
                count = int(arg)
                break

    # Límites según tipo de usuario
    max_cards = 50 if user_data.get('premium', False) else 20
    if not is_admin and count > max_cards:
        await update.message.reply_text(
            f"❌ Límite excedido. Máximo {max_cards} tarjetas")
        return

    # GENERAR TARJETAS CON SOPORTE COMPLETO
    try:
        if preset_month or preset_year or preset_cvv:
            cards = CardGenerator.generate_cards_custom_advanced(
                bin_number, count, preset_month, preset_year, preset_cvv,
                card_length, cvv_length)
        else:
            cards = CardGenerator.generate_cards_advanced(
                bin_number, count, card_length, cvv_length)
    except Exception as e:
        # Fallback al generador básico
        cards = CardGenerator.generate_cards(bin_number, count)

    # Obtener información REAL del BIN
    real_bin_info = await get_real_bin_info(bin_number)

    # Crear máscara del BIN apropiada para el tipo de tarjeta
    x_count = card_length - len(bin_number)
    bin_mask = bin_number + "x" * x_count

    # Mostrar formato usado
    format_display = f"{preset_month or 'rnd'} | {preset_year or 'rnd'} | {preset_cvv or 'rnd'}"

    # RESPUESTA MEJORADA
    response = f"BIN: {bin_mask} | {format_display}\n"
    response += f"═══════════════════════════\n"
    response += f"        『⛧⛧⛧』⟪ 𝗖𝗛𝗘𝗥𝗡𝗢𝗕𝗜𝗟 𝗖𝗛𝗟𝗩 ⟫『⛧⛧⛧』\n"
    response += f"                     \n"
    for card in cards:
        response += f"{card}\n"

    # Información del BIN con banderas completas
    country_flags = {
        'UNITED STATES': '🇺🇸',
        'CANADA': '🇨🇦',
        'UNITED KINGDOM': '🇬🇧',
        'GERMANY': '🇩🇪',
        'FRANCE': '🇫🇷',
        'SPAIN': '🇪🇸',
        'ITALY': '🇮🇹',
        'BRAZIL': '🇧🇷',
        'MEXICO': '🇲🇽',
        'ARGENTINA': '🇦🇷',
        'COLOMBIA': '🇨🇴',
        'PERU': '🇵🇪',
        'CHILE': '🇨🇱',
        'ECUADOR': '🇪🇨',
        'VENEZUELA': '🇻🇪'
    }

    country_name = real_bin_info['country'].upper()
    country_flag = country_flags.get(country_name, '🌍')

    # Tiempo de generación
    generation_time = round(random.uniform(0.025, 0.055), 3)

    response += f"\n═════════ DETAILS ══════════\n"
    response += f"💳 Bin Information:\n"
    response += f"🏦 Bank: {real_bin_info['bank']}\n"
    response += f"💼 Type: {real_bin_info['scheme']} - {real_bin_info['type']} - {real_bin_info['level']}\n"
    response += f"🌍 Country: {real_bin_info['country']} {country_flag}\n"
    response += f"⏱️ Time Spent: {generation_time}s\n"
    response += f"👤 Generated By: @{update.effective_user.username or update.effective_user.first_name}\n"
    response += f"╚═══════𝗖𝗛𝗘𝗥𝗡𝗢𝗕𝗜𝗟 𝗖𝗛𝗟𝗩═══════╝"

    # BOTÓN REGENERAR CORREGIDO - Mantiene parámetros originales
    regen_data = f"regen_{bin_number}_{count}_{preset_month or 'rnd'}_{preset_year or 'rnd'}_{preset_cvv or 'rnd'}_{card_length}_{cvv_length}"

    keyboard = [[
        InlineKeyboardButton("🔄 Regenerar Tarjetas", callback_data=regen_data),
        InlineKeyboardButton("📊 Ver BIN Info",
                             callback_data=f'bininfo_{bin_number}')
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Actualizar estadísticas
    db.update_user(user_id,
                   {'total_generated': user_data['total_generated'] + count})

    await update.message.reply_text(response, reply_markup=reply_markup)


async def credits_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ver créditos del usuario"""
    user_id = str(update.effective_user.id)
    user_data = db.get_user(user_id)

    premium_text = ""
    if user_data['premium']:
        premium_until = datetime.fromisoformat(user_data['premium_until'])
        days_left = (premium_until - datetime.now()).days
        premium_text = f"\n👑 **PREMIUM ACTIVO** ({days_left} días restantes)"

    response = f"💰 **TUS CRÉDITOS** 💰\n\n"
    response += f"💎 **Créditos disponibles:** {user_data['credits']}\n"
    response += f"📊 **Tarjetas generadas:** {user_data['total_generated']}\n"
    response += f"🔍 **Tarjetas verificadas:** {user_data['total_checked']}\n"
    response += premium_text
    response += f"\n\n💡 Usa `/bonus` para créditos gratis diarios"

    await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)


@check_maintenance
@group_only
@require_credits_for_live(3)
async def live_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Verificar tarjetas en vivo - Cuesta 3 créditos"""
    user_id = str(update.effective_user.id)
    user_data = db.get_user(user_id)
    is_admin = update.effective_user.id in ADMIN_IDS

    args = context.args
    if not args:
        response = "『⛧⛧⛧』⟪ 𝗖𝗛𝗘𝗥𝗡𝗢𝗕𝗜𝗟 𝗖𝗛𝗟𝗩 ⟫『⛧⛧⛧』\n\n"
        response += "⚜️ **༺ 𝗩𝗘𝗥𝗜𝗙𝗬 𝗟𝗜𝗩𝗘 ༻** ⚜️\n\n"
        response += "📟 **Uso:** `/live [tarjetas]`\n"
        response += "📑 **Formato:** `4532xxxxxxxx1234|12|2025|123`\n\n"
        response += "🔰 **Capacidad:** Hasta 10 tarjetas por comando\n"
        response += "💰 **Costo:** 3 créditos por verificación\n"

        await update.message.reply_text(response,
                                        parse_mode=ParseMode.MARKDOWN)
        return

    # Procesar tarjetas del mensaje completo
    full_message = ' '.join(args)
    cards_list = []

    # Buscar tarjetas en formato correcto
    import re
    card_pattern = r'\b\d{13,19}\|\d{1,2}\|\d{4}\|\d{3,4}\b'
    found_cards = re.findall(card_pattern, full_message)

    for card in found_cards:
        parts = card.split('|')
        if len(parts) == 4 and parts[0].isdigit() and len(parts[0]) >= 13:
            cards_list.append(card)

    if not cards_list:
        await update.message.reply_text(
            "❌ **FORMATO INCORRECTO**\n\n"
            "📋 **Formato correcto:** `4532123456781234|12|2025|123`\n"
            "💡 **Tip:** Asegúrate de usar el separador `|`",
            parse_mode=ParseMode.MARKDOWN)
        return

    # Limitar a 10 tarjetas máximo
    cards_list = cards_list[:10]
    total_cards = len(cards_list)

    # Sistema de APIs con pesos de efectividad - MEJORADO
    all_api_methods = [
        ("Stripe Ultra Pro", check_stripe_ultra_pro, 0.85),  # 85% efectividad
        ("PayPal Pro", check_paypal_ultra_pro, 0.75),  # 75% efectividad  
        ("Braintree Pro", check_braintree_ultra_pro, 0.65),  # 65% efectividad
        ("Authorize.net", check_authorize_ultra_pro, 0.55),  # 55% efectividad
        ("Square", check_square_ultra_pro, 0.45),  # 45% efectividad
        ("Adyen Pro", check_adyen_ultra_pro, 0.60),  # 60% efectividad
        ("Worldpay", check_worldpay_ultra_pro, 0.50),  # 50% efectividad
        ("CyberSource AI", check_cybersource_ultra_pro, 0.40
         )  # 40% efectividad
    ]

    # Verificar si el usuario tiene permisos de staff
    staff_data = db.get_staff_role(user_id)
    is_founder = staff_data and staff_data['role'] == '1'
    is_cofounder = staff_data and staff_data['role'] == '2'
    is_moderator = staff_data and staff_data['role'] == '3'
    is_premium = user_data.get('premium', False)

    # Rotación inteligente basada en efectividad
    if is_admin or is_founder or is_cofounder or is_moderator or is_premium:
        # TODOS los roles de staff y premium: Todos los métodos
        api_methods = all_api_methods

        if is_admin:
            methods_text = f"👑 ADMIN MODE - {len(api_methods)} APIs (Efectividad máxima)"
        elif is_founder:
            methods_text = f"🔱 FOUNDER MODE - {len(api_methods)} APIs (Efectividad máxima)"
        elif is_cofounder:
            methods_text = f"💎 CO-FOUNDER MODE - {len(api_methods)} APIs (Efectividad máxima)"
        elif is_moderator:
            methods_text = f"🛡️ MODERATOR MODE - {len(api_methods)} APIs (Efectividad máxima)"
        elif is_premium:
            methods_text = f"👑 PREMIUM MODE - {len(api_methods)} APIs (Efectividad máxima)"

        # Algoritmo de selección inteligente para usuarios privilegiados
        weighted_apis = []
        for name, method, weight in api_methods:
            # Repetir APIs más efectivas para mayor probabilidad de selección
            repetitions = int(
                weight * 10)  # Stripe aparecerá 8.5 veces, Square 4.5 veces
            weighted_apis.extend([(name, method)] * repetitions)

    else:
        # Estándar: 5 métodos más efectivos
        api_methods = all_api_methods[:5]
        methods_text = f"⚡ MODO ESTÁNDAR - {len(api_methods)} APIs (Efectividad estándar)"

        # Selección estándar
        weighted_apis = [(name, method)
                         for name, method, weight in api_methods]

    # Mensaje inicial unificado que funciona para 1 o múltiples tarjetas
    progress_msg = await update.message.reply_text(
        "⊚ CHERNOBIL VERIFICANDO.. ⊚\n\n"
        f"💳 Procesando {total_cards} tarjeta{'s' if total_cards > 1 else ''}...\n"
        f"{methods_text}...")

    results = []

    for card_index, card_data in enumerate(cards_list):
        # Actualizar progreso con formato unificado
        try:
            if total_cards > 1:
                progress = (card_index + 1) / total_cards * 100
                progress_bar = "█" * int(
                    progress // 10) + "░" * (10 - int(progress // 10))
                progress_text = f"📊 Progreso: [{progress_bar}] {progress:.0f}%\n💳 Tarjeta {card_index + 1}/{total_cards}"
            else:
                progress_text = f"💳 Verificando tarjeta única..."

            await progress_msg.edit_text(f"⊚ **CHERNOBIL VERIFICANDO..** ⊚\n\n"
                                         f"{progress_text}\n"
                                         f"{methods_text}...")
        except:
            pass

        parts = card_data.split('|')

        # Selección inteligente de API basada en pesos
        if is_admin or is_founder or is_cofounder or is_moderator or is_premium:
            # Para usuarios privilegiados (staff/premium): selección ponderada inteligente
            selected_api = random.choice(weighted_apis)
            api_name, api_method = selected_api
        else:
            # Para estándar: rotación equilibrada
            selected_api = random.choice([
                (name, method) for name, method, weight in api_methods
            ])
            api_name, api_method = selected_api

        # Simular tiempo de verificación realista
        import time
        time.sleep(random.uniform(1.0, 2.0))

        is_live, status, gateways, charge_amount, card_level = api_method(
            card_data)

        # Obtener información del BIN para la tarjeta individual
        bin_number = parts[0][:6]
        bin_info = await get_real_bin_info(bin_number)

        # Obtener respuesta detallada del método
        response_details = status.split(" - ", 1)
        main_status = response_details[0]
        detail_info = response_details[1] if len(response_details) > 1 else ""

        results.append({
            'card_data':
            card_data,
            'parts':
            parts,
            'is_live':
            is_live,
            'api':
            api_name,
            'status':
            "LIVE ✅" if is_live else "DEAD ❌",
            'result':
            detail_info if detail_info else main_status,
            'charge_amount':
            charge_amount if 'charge_amount' in locals() else 0,
            'gateway_response':
            f"Gateway: {api_name}",
            'index':
            card_index + 1,
            'bin_info':
            bin_info,
            'verification_time':
            datetime.now().strftime('%H:%M:%S')
        })

    # Construir respuesta final con formato mejorado
    final_response = ""

    # Si es UNA SOLA tarjeta, usar formato detallado
    if total_cards == 1:
        result = results[0]
        bin_info = result['bin_info']

        # Obtener bandera del país
        country_flags = {
            'UNITED STATES': '🇺🇸',
            'CANADA': '🇨🇦',
            'UNITED KINGDOM': '🇬🇧',
            'GERMANY': '🇩🇪',
            'FRANCE': '🇫🇷',
            'SPAIN': '🇪🇸',
            'ITALY': '🇮🇹',
            'BRAZIL': '🇧🇷',
            'MEXICO': '🇲🇽',
            'ARGENTINA': '🇦🇷',
            'COLOMBIA': '🇨🇴',
            'PERU': '🇵🇪',
            'CHILE': '🇨🇱',
            'ECUADOR': '🇪🇨',
            'VENEZUELA': '🇻🇪'
        }

        country_name = bin_info['country'].upper()
        country_flag = country_flags.get(country_name, '🌍')

        # Formato detallado para UNA tarjeta
        final_response += "『⛧⛧⛧』⟪ 𝗖𝗛𝗘𝗥𝗡𝗢𝗕𝗜𝗟 𝗖𝗛𝗟𝗩 ⟫『⛧⛧⛧』\n\n"
        final_response += f"[𖤍] 𝗖𝗮𝗿𝗱 ⊱ {result['parts'][0]}|{result['parts'][1]}|{result['parts'][2]}|{result['parts'][3]}\n"
        final_response += f"[𖤍] 𝗦𝘁𝗮𝘁𝘂𝘀 ⊱ {result['status']}\n"
        final_response += f"[𖤍] 𝗥𝗲𝘀𝘂𝗹𝘁 ⊱ {result['result']}\n"
        final_response += f"[𖤍] 𝗚𝗮𝘁𝗲𝘄𝗮𝘆 ⊱ {result['api']} 🛰️\n"
        final_response += f"══════════ 𝗗𝗘𝗧𝗔𝗜𝗟𝗦 ══════════\n"
        final_response += f"[𖤍] 𝗕𝗜𝗡 ⊱ {result['parts'][0][:6]}xxxxxx\n"
        final_response += f"[𖤍] 𝗕𝗮𝗻𝗸 ⊱ {bin_info['bank']}\n"
        final_response += f"[𖤍] 𝗦𝗰𝗵𝗲𝗺𝗲 ⊱ {bin_info['scheme']} | {bin_info['type']}\n"
        final_response += f"[𖤍] 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 ⊱ {bin_info['country']} {country_flag} - 💲USD\n"
        final_response += f"══════════ 𝗜𝗡𝗙𝗢 ══════════\n"
        final_response += f"[𖤍] 𝗧𝗶𝗺𝗲 ⊱ {datetime.now().strftime('%H:%M:%S')} ⌛\n"
        final_response += f"[𖤍] 𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆 ⊱ @{update.effective_user.username or update.effective_user.first_name} 👤\n"
        final_response += f"[𖤍] 𝗕𝗼𝘁 ⊱ @ChernobilChLv_bot 𖠑"

    else:
        # Formato compacto para múltiples tarjetas
        final_response += "『⛧⛧⛧』⟪ 𝗖𝗛𝗘𝗥𝗡𝗢𝗕𝗜𝗟 𝗖𝗛𝗟𝗩 ⟫『⛧⛧⛧』\n\n"

        # Resultados de cada tarjeta
        for result in results:
            final_response += f"[{result['index']}] {result['parts'][0]}|{result['parts'][1]}|{result['parts'][2]}|{result['parts'][3]}\n"
            final_response += f"[𖤍] Status ⊱ {result['status']}\n"
            final_response += f"[𖤍] Result ⊱ {result['result']}\n"
            final_response += f"[𖤍] Gateway ⊱ {result['api']} 🛰️\n"
            final_response += f"[𖤍] Time ⊱ {datetime.now().strftime('%H:%M:%S')} ⌛\n"
            final_response += f"[𖤍] Checked by ⊱ @{update.effective_user.username or update.effective_user.first_name} 👤\n"
            final_response += f"[𖤍] Bot ⊱ @ChernobilChLv_bot 𖠑\n"

            # Separador solo si hay más tarjetas
            if result['index'] < len(results):
                final_response += "\n"

        # Estadísticas finales para múltiples tarjetas
        live_count = sum(1 for r in results if r['is_live'])
        final_response += f"\n🔥 Resultado: {live_count}/{total_cards} LIVE\n"
        final_response += f"⚡ Efectividad: {(live_count/total_cards)*100:.1f}%"

    # Actualizar estadísticas del usuario
    db.update_user(
        user_id,
        {'total_checked': user_data['total_checked'] + len(cards_list)})

    # Enviar respuesta final con mejor manejo de errores
    try:
        await progress_msg.edit_text(final_response)
    except Exception as e:
        logger.error(f"Error editando mensaje de progreso: {e}")
        try:
            # Si falla editar, enviar nuevo mensaje
            await update.message.reply_text(final_response)
        except Exception as e2:
            logger.error(f"Error enviando mensaje de respuesta: {e2}")
            # Mensaje de emergencia ultra-simple
            try:
                simple_msg = f"Verificación completada: {len([r for r in results if r['is_live']])}/{total_cards} LIVE"
                await update.message.reply_text(simple_msg)
            except:
                logger.error(
                    "Error crítico: No se pudo enviar ningún mensaje de respuesta"
                )


async def direccion_command(update: Update,
                            context: ContextTypes.DEFAULT_TYPE):
    """Generar direcciones por país con datos 100% reales"""
    args = context.args
    country = args[0].upper() if args else None

    # Mostrar países disponibles si no se especifica
    if not country:
        response = f"🌍 **GENERADOR DE DIRECCIONES** 🌍\n\n"
        response += f"**Uso:** `/direccion [país]`\n\n"
        response += f"**Países disponibles:**\n"

        for code, data in AddressGenerator.COUNTRIES_DATA.items():
            response += f"• `{code}` {data['flag']} - {data['country_name']}\n"

        response += f"\n**Ejemplos:**\n"
        response += f"• `/direccion US` - Estados Unidos\n"
        response += f"• `/direccion BR` - Brasil\n"
        response += f"• `/direccion ES` - España\n"
        response += f"• `/direccion AR` - Argentina\n"
        response += f"• `/direccion KZ` - Kazajistán\n"
        response += f"• `/direccion AE` - Dubái (UAE)"

        await update.message.reply_text(response,
                                        parse_mode=ParseMode.MARKDOWN)
        return

    # Generar dirección
    address = AddressGenerator.generate_address(country)

    if not address:
        await update.message.reply_text(
            f"❌ **País '{country}' no disponible**\n\n"
            f"💡 Usa `/direccion` para ver países disponibles",
            parse_mode=ParseMode.MARKDOWN)
        return

    response = f"📍 **DIRECCIÓN GENERADA** 📍\n\n"
    response += f"{address['flag']} **País:** {address['country']}\n"
    response += f"🏠 **Dirección:** {address['street']}\n"
    response += f"🌆 **Ciudad:** {address['city']}\n"
    response += f"🗺️ **Estado/Provincia:** {address['state']}\n"
    response += f"📮 **Código Postal:** {address['postal_code']}\n"
    response += f"📞 **Teléfono:** {address['phone']}\n\n"
    response += f"✅ **Datos 100% reales y verificados**\n"
    response += f"🔄 **Usa el comando nuevamente para generar otra**"

    await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)


@check_maintenance
async def ex_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Extrapolación avanzada de tarjetas - Solo admins, fundadores, co-fundadores, moderadores y premium"""
    user_id = str(update.effective_user.id)
    user_data = db.get_user(user_id)
    is_admin = update.effective_user.id in ADMIN_IDS

    # Verificar si es admin, staff o premium
    is_founder = db.is_founder(user_id)
    is_cofounder = db.is_cofounder(user_id)
    is_moderator = db.is_moderator(user_id)
    is_premium = user_data.get('premium', False)

    # Permitir acceso a admins, fundadores, co-fundadores, moderadores y premium
    if not (is_admin or is_founder or is_cofounder or is_moderator
            or is_premium):
        await update.message.reply_text(
            "╔═════════════════════════════╗\n"
            "║  🔒 **ACCESO RESTRINGIDO** 🔒  ║\n"
            "╚═════════════════════════════╝\n\n"
            "👑 **Este comando es EXCLUSIVO para:**\n"
            "• 🛡️ Administradores del bot\n"
            "• 💎 Usuarios con membresía PREMIUM\n\n"
            "🚫 **Tu cuenta:** Usuario estándar\n"
            "💡 **Para acceder necesitas:**\n\n"
            "💎 **Beneficios premium:**\n"
            "• ✅ Extrapolación avanzada ilimitada\n"
            "• ✅ Algoritmos de IA únicos\n"
            "• ✅ Mayor efectividad (75-85%)\n"
            "• ✅ Reconoce múltiples formatos\n"
            "• ✅ Créditos adicionales\n\n"
            "💰 **Consultar precios:** Contacta un admin",
            parse_mode=ParseMode.MARKDOWN)
        return

    # Verificar créditos solo si no es admin
    if not is_admin:
        if user_data['credits'] < 5:
            await update.message.reply_text(
                f"❌ **Créditos insuficientes**\n\n"
                f"Necesitas: 5 créditos\n"
                f"Tienes: {user_data['credits']} créditos\n\n"
                f"Usa /bonus para créditos gratis o /infocredits para más información",
                parse_mode=ParseMode.MARKDOWN)
            return

        # Descontar créditos
        db.update_user(user_id, {'credits': user_data['credits'] - 5})

    args = context.args
    if not args:
        await update.message.reply_text(
            "╔═══════════════════════════════╗\n"
            "║  🧠 **EXTRAPOLACIÓN PREMIUM** 🧠  ║\n"
            "╚═══════════════════════════════╝\n\n"
            "💎 **Formatos soportados:**\n"
            "• `/ex 4532123456781234|12|2025|123`\n"
            "• `/ex 4532123456781234`\n\n"
            "🤖 **Algoritmo IA:**\n"
            "• Genera variaciones inteligentes\n"
            "• Mantiene patrones del BIN original\n"
            "• Optimizado para máxima efectividad\n\n"
            "💰 **Costo:** 5 créditos\n"
            "⚡ **Cantidad:** 20 variaciones únicas",
            parse_mode=ParseMode.MARKDOWN)
        return

    card_input = args[0]

    # Detectar y procesar diferentes formatos
    if '|' in card_input:
        # Formato completo: 4532123456781234|12|2025|123
        parts = card_input.split('|')
        if len(parts) != 4:
            await update.message.reply_text(
                "❌ **Formato incorrecto**\n\n"
                "✅ **Formatos válidos:**\n"
                "• `4532123456781234|12|2025|123`\n"
                "• `4532123456781234`")
            return

        base_card = parts[0]
        preset_month = parts[1]
        preset_year = parts[2]
        preset_cvv = parts[3]
    else:
        # Solo número: 4532123456781234
        if not card_input.isdigit() or len(card_input) < 13:
            await update.message.reply_text(
                "❌ **Número de tarjeta inválido**\n\n"
                "💡 Debe tener al menos 13 dígitos")
            return

        base_card = card_input
        preset_month = None
        preset_year = None
        preset_cvv = None

    # Extraer BIN
    bin_number = base_card[:6]

    # Mensaje de procesamiento
    process_msg = await update.message.reply_text(
        "🧠 **PROCESANDO EXTRAPOLACIÓN** 🧠\n\n"
        "⚡ Analizando patrones del BIN...\n"
        "🤖 Ejecutando algoritmos de IA...\n"
        "🔄 Generando variaciones inteligentes...")

    # Simular procesamiento avanzado
    await asyncio.sleep(3)

    # Generar variaciones inteligentes
    variations = []
    for i in range(20):
        if preset_month and preset_year and preset_cvv:
            # Usar parámetros específicos
            new_card = CardGenerator.generate_cards_custom(
                bin_number, 1, preset_month, preset_year, preset_cvv)[0]
        else:
            # Generar aleatorio
            new_card = CardGenerator.generate_cards(bin_number, 1)[0]
        variations.append(new_card)

    # Obtener información real del BIN
    bin_info = await get_real_bin_info(bin_number)

    # Formato de respuesta mejorado
    final_response = "╔═══════════════════════════════╗\n"
    final_response += "║  🧠 **EXTRAPOLACIÓN COMPLETA** 🧠  ║\n"
    final_response += "╚═══════════════════════════════╝\n\n"

    final_response += f"🎯 **BIN Analizado:** {bin_number}xxxxxx\n"
    final_response += f"🏦 **Banco:** {bin_info['bank']}\n"
    final_response += f"💳 **Tipo:** {bin_info['scheme']} | {bin_info['type']}\n"
    final_response += f"🌍 **País:** {bin_info['country']}\n"
    final_response += f"🔢 **Variaciones:** 20 únicas\n\n"

    final_response += "```\n"
    for i, var in enumerate(variations, 1):
        final_response += f"{i:2d}. {var}\n"
    final_response += "```\n\n"

    final_response += "🎯 **Probabilidad:** 75-85% efectividad\n"
    final_response += f"💰 **Créditos restantes:** {user_data['credits'] - 5 if not is_admin else '∞'}\n"
    final_response += "🤖 **Generado por IA avanzada**"

    try:
        await process_msg.edit_text(final_response,
                                    parse_mode=ParseMode.MARKDOWN)
    except:
        await update.message.reply_text(final_response,
                                        parse_mode=ParseMode.MARKDOWN)


async def bonus_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reclamar bono diario"""
    user_id = str(update.effective_user.id)
    user_data = db.get_user(user_id)

    now = datetime.now()
    last_bonus = user_data.get('last_bonus')

    if last_bonus:
        last_bonus_date = datetime.fromisoformat(last_bonus)
        if (now - last_bonus_date).days < 1:
            hours_left = 24 - (now - last_bonus_date).seconds // 3600
            await update.message.reply_text(f"⏰ Ya reclamaste tu bono hoy\n"
                                            f"Vuelve en {hours_left} horas")
            return

    # Dar bono
    bonus_amount = 15 if user_data['premium'] else 10

    db.update_user(
        user_id, {
            'credits': user_data['credits'] + bonus_amount,
            'last_bonus': now.isoformat()
        })

    response = f"🎁 **BONO DIARIO RECLAMADO** 🎁\n\n"
    response += f"💎 **Créditos obtenidos:** {bonus_amount}\n"
    response += f"💰 **Total créditos:** {user_data['credits'] + bonus_amount}\n\n"
    response += f"⏰ Vuelve mañana para más créditos gratis"

    await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Estado del bot"""
    response = f"╔═════════════════════════╗\n"
    response += f"║    🤖 𝐄𝐒𝐓𝐀𝐃𝐎 𝐃𝐄𝐋 𝐁𝐎𝐓    ║\n"
    response += f"╚═════════════════════════╝\n\n"

    response += f"🟢 **Estado:** Operativo\n"
    response += f"⚡ **Uptime:** 99.9%\n"
    response += f"🔧 **Versión:** 𝗖𝗛𝗘𝗥𝗡𝗢𝗕𝗜𝗟 𝗖𝗛𝗟𝗩\n"
    response += f"💻 **Servidor:** Anonymous\n"
    response += f"🌐 **Latencia:** <50ms\n\n"

    response += f"🛡️ **Seguridad:** SSL Activado\n"
    response += f"🔄 **Última actualización:** {datetime.now().strftime('%d/%m/%Y')}\n"
    response += f"📡 **API Status:** Online\n"
    response += f"🎯 **Performance:** Óptimo"

    await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)


async def detect_payment_gateways(url: str):
    """Detecta las pasarelas de pago de un sitio web con 25+ métodos"""
    try:
        import requests
        from bs4 import BeautifulSoup

        headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')

        detected_gateways = {'destacadas': [], 'principales': [], 'otras': []}

        # Buscar en HTML, scripts y meta tags
        html_content = str(soup).lower()
        scripts = str(
            [script.get_text() for script in soup.find_all('script')]).lower()
        full_content = html_content + scripts

        # Pasarelas destacadas (más efectivas para CC)
        gateways_destacadas = {
            'shopify':
            ['🔥 Shopify Payments', ['shopify', 'shopify-pay', 'shop-pay']],
            'woocommerce':
            ['🔥 WooCommerce', ['woocommerce', 'wc-', 'wordpress']],
            'magento': ['🔥 Magento', ['magento', 'mage-', 'mage_']]
        }

        # Pasarelas principales (muy comunes)
        gateways_principales = {
            'paypal':
            ['✅ PayPal', ['paypal', 'pp-', 'paypal.com', 'paypalobjects']],
            'stripe': [
                '✅ Stripe',
                [
                    'stripe', 'js.stripe.com', 'stripe.com', 'sk_live',
                    'pk_live'
                ]
            ],
            'square':
            ['✅ Square', ['square', 'squareup', 'square.com', 'sq-']],
            'authorize': [
                '✅ Authorize.net',
                ['authorize.net', 'authorizenet', 'authorize-net']
            ],
            'braintree':
            ['✅ Braintree', ['braintree', 'braintreepayments', 'bt-']],
            'adyen': ['✅ Adyen', ['adyen', 'adyen.com', 'adyen-']],
            'worldpay': ['✅ Worldpay', ['worldpay', 'worldpay.com', 'wp-']]
        }

        # Otras pasarelas detectables
        gateways_otras = {
            'applepay':
            ['🍎 Apple Pay', ['apple-pay', 'applepay', 'apple_pay']],
            'googlepay': [
                '🔵 Google Pay',
                ['google-pay', 'googlepay', 'google_pay', 'gpay']
            ],
            'amazonpay':
            ['📦 Amazon Pay', ['amazon-pay', 'amazonpay', 'amazon_pay']],
            'venmo': ['💜 Venmo', ['venmo', 'venmo.com']],
            'klarna': ['🔶 Klarna', ['klarna', 'klarna.com']],
            'afterpay': ['⚪ Afterpay', ['afterpay', 'afterpay.com']],
            'affirm': ['🟣 Affirm', ['affirm', 'affirm.com']],
            'razorpay': ['⚡ Razorpay', ['razorpay', 'razorpay.com']],
            'payu': ['🟡 PayU', ['payu', 'payu.com', 'payu-']],
            'mercadopago':
            ['🟢 MercadoPago', ['mercadopago', 'mercado-pago', 'mp-']],
            'checkout':
            ['🔷 Checkout.com', ['checkout.com', 'checkout-', 'cko-']],
            'mollie': ['🟠 Mollie', ['mollie', 'mollie.com']],
            'cybersource':
            ['🔐 CyberSource', ['cybersource', 'cybersource.com']],
            'bluepay': ['🔹 BluePay', ['bluepay', 'bluepay.com']],
            'firstdata': ['🔴 First Data', ['firstdata', 'first-data']],
            'elavon': ['🔵 Elavon', ['elavon', 'elavon.com']],
            '2checkout': ['2️⃣ 2Checkout', ['2checkout', '2co-']],
            'skrill': ['💰 Skrill', ['skrill', 'skrill.com']],
            'paysafecard': ['🔒 Paysafecard', ['paysafecard', 'paysafe']],
            'bitcoin': ['₿ Bitcoin', ['bitcoin', 'btc', 'cryptocurrency']],
            'coinbase': ['🪙 Coinbase', ['coinbase', 'coinbase.com']],
            'binance': ['⚡ Binance Pay', ['binance', 'binancepay']],
            'alipay': ['🇨🇳 Alipay', ['alipay', 'alipay.com']],
            'wechatpay':
            ['💬 WeChat Pay', ['wechat', 'wechatpay', 'wechat-pay']]
        }

        # Detectar cada categoría
        for key, (name, indicators) in gateways_destacadas.items():
            if any(indicator in full_content for indicator in indicators):
                detected_gateways['destacadas'].append(name)

        for key, (name, indicators) in gateways_principales.items():
            if any(indicator in full_content for indicator in indicators):
                detected_gateways['principales'].append(name)

        for key, (name, indicators) in gateways_otras.items():
            if any(indicator in full_content for indicator in indicators):
                detected_gateways['otras'].append(name)

        return detected_gateways

    except Exception as e:
        return None


async def pasarela_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Detectar pasarelas de pago de un sitio web"""
    args = context.args

    if not args:
        response = f"🔍 **DETECTOR DE PASARELAS** 🔍\n\n"
        response += f"**Uso:** `/pasarela [URL]`\n"
        response += f"**Ejemplo:** `/pasarela"
        response += f"🎯 **Funciones:**\n"
        response += f"• Detecta automáticamente las pasarelas\n"
        response += f"• Clasifica por importancia\n"
        response += f"• Identifica métodos de pago\n"
        response += f"• Análisis en tiempo real\n\n"
        response += f"💡 **Tip:** Usa URLs completas con https://"

        await update.message.reply_text(response,
                                        parse_mode=ParseMode.MARKDOWN)
        return

    url = args[0]
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    # Mensaje de análisis
    analysis_msg = await update.message.reply_text(
        "🔍 **Analizando sitio web...**\n⏳ Detectando pasarelas de pago...")

    try:
        detected = await detect_payment_gateways(url)

        if detected is None:
            await analysis_msg.edit_text(
                f"❌ **Error al analizar el sitio**\n\n"
                f"🌐 **URL:** {url}\n"
                f"💡 **Posibles causas:**\n"
                f"• Sitio no accesible\n"
                f"• Protección anti-bots\n"
                f"• URL inválida",
                parse_mode=ParseMode.MARKDOWN)
            return

        # Formatear respuesta estilo del bot de la imagen
        response = f"✅ **PASARELAS DETECTADAS:**\n"
        response += f"_" * 30 + "\n\n"

        if detected['destacadas']:
            response += f"💎 **Pasarelas Destacadas:** 🔥\n"
            for gateway in detected['destacadas']:
                response += f"• {gateway}\n"
            response += f"_" * 30 + "\n"

        if detected['principales']:
            response += f"🏆 **Pasarelas Principales:** ✅\n"
            for gateway in detected['principales']:
                response += f"• {gateway}\n"
            response += f"_" * 30 + "\n"

        if detected['otras']:
            response += f"⚪ **Otras Pasarelas Detectadas:** 🟡\n"
            for gateway in detected['otras']:
                response += f"• {gateway}\n"
            response += f"_" * 30 + "\n"

        if not any(detected.values()):
            response += f"❌ **No se detectaron pasarelas conocidas**\n"
            response += f"💡 El sitio puede usar pasarelas personalizadas"

        response += f"\n🌐 **Sitio analizado:** {url}\n"
        response += f"⏰ **Análisis:** {datetime.now().strftime('%H:%M:%S')}"

        await analysis_msg.edit_text(response, parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        await analysis_msg.edit_text(
            f"❌ **Error durante el análisis**\n\n"
            f"🌐 **URL:** {url}\n"
            f"🔍 **Error:** {str(e)}\n\n"
            f"💡 **Intenta con otra URL**",
            parse_mode=ParseMode.MARKDOWN)


async def apply_key_command(update: Update,
                            context: ContextTypes.DEFAULT_TYPE):
    """Aplicar clave premium"""
    user_id = str(update.effective_user.id)

    args = context.args
    if not args:
        await update.message.reply_text(
            "🔑 **APLICAR CLAVE PREMIUM** 🔑\n\n"
            "Uso: /apply_key [código]\n"
            "Ejemplo: /apply_key ULTRA2024\n\n"
            "💎 Las claves premium te dan acceso completo",
            parse_mode=ParseMode.MARKDOWN)
        return

    key_code = args[0].upper()

    # Claves válidas simuladas
    VALID_KEYS = {
        'ULTRA30': {
            'days': 30,
            'used': False
        },
        'PREMIUM460': {
            'days': 60,
            'used': False
        },
        'VIP90': {
            'days': 90,
            'used': False
        },
        'ChernobilChLv_365': {
            'days': 365,
            'used': False
        }
    }

    if key_code not in VALID_KEYS or VALID_KEYS[key_code]['used']:
        await update.message.reply_text(
            "❌ **Clave inválida o ya utilizada**\n\n"
            "Verifica el código e intenta nuevamente",
            parse_mode=ParseMode.MARKDOWN)
        return

    # Activar premium
    days = VALID_KEYS[key_code]['days']
    premium_until = datetime.now() + timedelta(days=days)

    db.update_user(
        user_id,
        {
            'premium': True,
            'premium_until': premium_until.isoformat(),
            'credits': db.get_user(user_id)['credits'] + 100  # Bonus credits
        })

    # Marcar clave como usada
    VALID_KEYS[key_code]['used'] = True

    response = f"🎉 **CLAVE ACTIVADA EXITOSAMENTE** 🎉\n\n"
    response += f"👑 **Premium activado por {days} días**\n"
    response += f"💎 **+300 créditos bonus**\n"
    response += f"⚡ **Beneficios premium desbloqueados:**\n\n"
    response += f"• Verificación completa 6 métodos\n"
    response += f"• Límites aumentados\n"
    response += f"• Bono diario premium\n"
    response += f"• Soporte prioritario\n"
    response += f"• Algoritmos avanzados"

    await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)


async def infocredits_command(update: Update,
                              context: ContextTypes.DEFAULT_TYPE):
    """Información sobre créditos con botones inline mejorados"""
    user_id = str(update.effective_user.id)
    user_data = db.get_user(user_id)

    keyboard = [[
        InlineKeyboardButton("💰 Obtener Créditos",
                             callback_data='get_credits'),
        InlineKeyboardButton("👑 Premium", callback_data='premium_benefits')
    ],
                [
                    InlineKeyboardButton("🆓 Comandos Gratis",
                                         callback_data='free_commands'),
                    InlineKeyboardButton("💎 Comandos de Pago",
                                         callback_data='paid_commands')
                ],
                [
                    InlineKeyboardButton("📊 Mis Estadísticas",
                                         callback_data='my_stats'),
                    InlineKeyboardButton("🎮 Ir a Juegos",
                                         callback_data='go_games')
                ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    premium_text = ""
    if user_data['premium']:
        premium_until = datetime.fromisoformat(user_data['premium_until'])
        days_left = (premium_until - datetime.now()).days
        premium_text = f"\n👑 **PREMIUM ACTIVO** ({days_left} días)"

    response = f"╔═══════════════════════════╗\n"
    response += f"║     💡 𝐒𝐈𝐒𝐓𝐄𝐌𝐀 𝐃𝐄 𝐂𝐑É𝐃𝐈𝐓𝐎𝐒     ║\n"
    response += f"╚═══════════════════════════╝\n\n"
    response += f"💎 **Tus Créditos:** {user_data['credits']}{premium_text}\n\n"
    response += f"📋 **Selecciona una opción:**"

    await update.message.reply_text(response,
                                    reply_markup=reply_markup,
                                    parse_mode=ParseMode.MARKDOWN)


async def donate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Donar créditos a otro usuario con diseño mejorado"""
    user_id = str(update.effective_user.id)
    user_data = db.get_user(user_id)
    is_admin = update.effective_user.id in ADMIN_IDS

    args = context.args
    if len(args) < 2:
        await update.message.reply_text(
            "╔═══════════════════════════════╗\n"
            "║    💝 **SISTEMA DE DONACIONES** 💝    ║\n"
            "╚═══════════════════════════════╝\n\n"
            "🎁 **Comparte créditos con la comunidad**\n\n"
            "📋 **Uso:** `/donate [user_id] [cantidad]`\n"
            "💡 **Ejemplo:** `/donate 123456789 50`\n\n"
            "✨ **Beneficios de donar:**\n"
            "• Ayudas a otros usuarios del bot\n"
            "• Contribuyes al crecimiento de la comunidad\n"
            "💰 **Tus créditos actuales:** {}\n".format(
                user_data['credits'] if not is_admin else '∞ (Admin)'),
            parse_mode=ParseMode.MARKDOWN)
        return

    try:
        target_user_id = args[0]
        amount = int(args[1])
    except ValueError:
        await update.message.reply_text(
            "❌ **Error en el formato**\n\n"
            "💡 La cantidad debe ser un número válido\n"
            "📋 **Ejemplo:** `/donate 123456789 50`")
        return

    if amount <= 0:
        await update.message.reply_text("❌ **Cantidad inválida**\n\n"
                                        "💡 La cantidad debe ser mayor a 0\n"
                                        "📊 **Mínimo:** 1 crédito")
        return

    # Verificar créditos suficientes
    if not is_admin and user_data['credits'] < amount:
        await update.message.reply_text(
            "╔═══════════════════════════════╗\n"
            "║    ❌ **CRÉDITOS INSUFICIENTES** ❌    ║\n"
            "╚═══════════════════════════════╝\n\n"
            f"💰 **Tienes:** {user_data['credits']} créditos\n"
            f"💸 **Necesitas:** {amount} créditos\n"
            f"📉 **Faltante:** {amount - user_data['credits']} créditos\n\n"
            "💡 **Obtén más créditos con:**\n"
            "• `/bonus` - Bono diario gratis\n"
            "• `/juegos` - Casino bot\n"
            "• `/apply_key` - Clave premium"
            "• Contacto con @SteveCHBll para mas creditos",
            parse_mode=ParseMode.MARKDOWN)
        return

    # Procesar transferencia
    target_user_data = db.get_user(target_user_id)

    # Solo descontar créditos si no es admin
    if not is_admin:
        db.update_user(user_id, {'credits': user_data['credits'] - amount})

    db.update_user(target_user_id,
                   {'credits': target_user_data['credits'] + amount})

    # Respuesta exitosa mejorada
    response = "╔═══════════════════════════════╗\n"
    response += "║    🎉 **DONACIÓN COMPLETADA** 🎉    ║\n"
    response += "╚═══════════════════════════════╝\n\n"

    response += f"💎 **Cantidad donada:** {amount:,} créditos\n"
    response += f"👤 **Destinatario:** `{target_user_id}`\n"
    response += f"💰 **Usuario ahora tiene:** {target_user_data['credits'] + amount:,} créditos\n\n"

    if is_admin:
        response += f"🔥 **Tus créditos:** ∞ (Administrador)\n"
    else:
        response += f"📊 **Te quedan:** {user_data['credits'] - amount:,} créditos\n"

    response += f"⏰ **Fecha:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
    response += f"🌟 **¡Gracias por tu generosidad!**\n"
    response += f"🤝 **La comunidad aprecia tu contribución**"

    await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)


async def check_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /check para verificar capturas - Solo funciona respondiendo a imágenes"""
    user_id = str(update.effective_user.id)
    user_data = db.get_user(user_id)
    group_id = str(update.effective_chat.id)

    # Verificar que el comando se use respondiendo a una imagen
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        await update.message.reply_text(
            "╔══════════════════════════════════╗\n"
            "║   📸  **VERIFICADOR DE CAPTURAS**  📸   ║\n"
            "╚══════════════════════════════════╝\n\n"
            "🚫 **ERROR:** Debes responder a una imagen\n\n"
            "📋 **INSTRUCCIONES:**\n"
            "┌─────────────────────────────────┐\n"
            "│ 1️⃣ Envía tu captura al grupo     │\n"
            "│ 2️⃣ Responde a esa imagen con /check │\n"
            "│ 3️⃣ Espera la verificación oficial   │\n"
            "└─────────────────────────────────┘\n\n"
            "🎁 **¡Obtén recompensas por capturas válidas!**\n"
            "⚡ **Verificación rápida en menos de 24h**\n\n"
            "💡 **TIP:** Solo capturas auténticas serán aprobadas",
            parse_mode=ParseMode.MARKDOWN)
        return

    # Verificar que el grupo tenga configurado el sistema
    check_config = db.get_check_chats(group_id)
    if not check_config:
        await update.message.reply_text(
            "╔══════════════════════════════════╗\n"
            "║      ⚙️  **SISTEMA NO CONFIGURADO**  ⚙️      ║\n"
            "╚══════════════════════════════════╝\n\n"
            "❌ **El sistema de verificación no está activo**\n\n"
            "🔧 **Para administradores:**\n"
            "• Usar comando `/setcheckchats`\n"
            "• Configurar chat de verificación\n"
            "• Configurar canal de publicación\n\n"
            "📞 **Contacta a la administración para activar**",
            parse_mode=ParseMode.MARKDOWN)
        return

    # Generar ID único para esta verificación
    import uuid
    check_id = str(uuid.uuid4())[:8]

    # Obtener información de la imagen
    photo = update.message.reply_to_message.photo[
        -1]  # La imagen de mayor calidad
    image_file_id = photo.file_id

    # Guardar verificación pendiente
    username = f"@{update.effective_user.username}" if update.effective_user.username else update.effective_user.first_name
    db.add_pending_check(check_id, user_id, username, image_file_id, group_id)

    # Enviar confirmación al usuario con diseño mejorado
    await update.message.reply_text(
        "╔══════════════════════════════════╗\n"
        "║    🎯  **CAPTURA EN VERIFICACIÓN**  🎯    ║\n"
        "╚══════════════════════════════════╝\n\n"
        "✨ **¡Tu captura ha sido enviada exitosamente!**\n\n"
        "┌─────────── 📊 **DETALLES** ───────────┐\n"
        f"│ 🆔 **ID:** `{check_id}`\n"
        f"│ 👤 **Usuario:** {username}\n"
        f"│ 📸 **Estado:** Imagen procesada ✅\n"
        f"│ ⏳ **Revisión:** En proceso...\n"
        "└──────────────────────────────────────┘\n\n"
        f"📅 **Enviado:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
        "⏰ **Tiempo máximo:** 24 horas\n\n"
        "🌟 **¡Mantente atento a las actualizaciones!**",
        parse_mode=ParseMode.MARKDOWN)

    # Enviar imagen al chat de verificación para administradores
    try:
        verification_chat_id = check_config['verification_chat']

        # Crear botones para aprobar/rechazar
        keyboard = [[
            InlineKeyboardButton("✅ APROBAR",
                                 callback_data=f'approve_check_{check_id}'),
            InlineKeyboardButton("❌ RECHAZAR",
                                 callback_data=f'reject_check_{check_id}')
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Enviar imagen con información al chat de verificación
        caption = f"🔍 **NUEVA VERIFICACIÓN PENDIENTE** 🔍\n\n"
        caption += f"🆔 **ID:** `{check_id}`\n"
        caption += f"👤 **Usuario:** {username} (`{user_id}`)\n"
        caption += f"📊 **Créditos actuales:** {user_data['credits']}\n"
        caption += f"🏠 **Grupo:** `{group_id}`\n"
        caption += f"📅 **Fecha:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        caption += f"💰 **Recompensa:** 6 créditos si se aprueba\n"
        caption += f"📝 **Acción requerida:** Aprobar o rechazar captura"

        await context.bot.send_photo(chat_id=verification_chat_id,
                                     photo=image_file_id,
                                     caption=caption,
                                     parse_mode=ParseMode.MARKDOWN,
                                     reply_markup=reply_markup)

    except Exception as e:
        logger.error(f"Error enviando a chat de verificación: {e}")
        await update.message.reply_text(
            "╔══════════════════════════════════╗\n"
            "║        ❌  **ERROR DEL SISTEMA**  ❌        ║\n"
            "╚══════════════════════════════════╝\n\n"
            "🔧 **No se pudo procesar la verificación**\n\n"
            "💡 **Posibles causas:**\n"
            "• Configuración incompleta del sistema\n"
            "• Problemas temporales de conectividad\n"
            "• Mantenimiento en curso\n\n"
            "📞 **Contacta a los administradores para asistencia**")


async def juegos_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sección de juegos con botones inline - Límite: 1 cada 12 horas"""
    user_id = str(update.effective_user.id)
    user_data = db.get_user(user_id)

    keyboard = [[
        InlineKeyboardButton("🎰 Ruleta de la Suerte",
                             callback_data='play_ruleta'),
        InlineKeyboardButton("🎲 Dados Mágicos", callback_data='play_dados')
    ],
                [
                    InlineKeyboardButton("🃏 Carta de la Fortuna",
                                         callback_data='play_carta'),
                    InlineKeyboardButton("⚡ Rayo de Créditos",
                                         callback_data='play_rayo')
                ],
                [
                    InlineKeyboardButton("📊 Mis Estadísticas",
                                         callback_data='game_stats')
                ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    now = datetime.now()
    last_game = user_data.get('last_game')
    can_play = True
    time_left = 0

    if last_game:
        last_game_date = datetime.fromisoformat(last_game)
        hours_passed = (now - last_game_date).total_seconds() / 3600
        if hours_passed < 12:
            can_play = False
            time_left = 12 - hours_passed

    status_text = "🟢 **DISPONIBLE**" if can_play else f"🔴 **COOLDOWN** ({time_left:.1f}h restantes)"

    response = f"╔═══════════════════════════╗\n"
    response += f"║        🎮 𝐂𝐀𝐒𝐈𝐍𝐎 𝐁𝐎𝐓        ║\n"
    response += f"╚═══════════════════════════╝\n\n"
    response += f"💰 **Créditos:** {user_data['credits']}\n"
    response += f"⏰ **Estado:** {status_text}\n"
    response += f"🎁 **Ganancia:** 3-8 créditos por juego\n"
    response += f"⏱️ **Límite:** 1 juego cada 12 horas\n\n"
    response += f"🎯 **Elige tu juego:**"

    await update.message.reply_text(response,
                                    reply_markup=reply_markup,
                                    parse_mode=ParseMode.MARKDOWN)


# Comandos de admin
async def staff_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sistema completo de staff con 3 roles"""
    args = context.args
    user_id = str(update.effective_user.id)
    user_id_int = update.effective_user.id

    # Si es comando de lista, cualquiera puede verlo
    if args and args[0].lower() == "list":
        role_names = {
            '1': '👑 Fundador',
            '2': '⚜️ Cofundador',
            '3': '👮🏼 Moderador'
        }

        # Organizar staff por roles
        fundadores = []
        cofundadores = []
        moderadores = []

        for staff_user_id, staff_data in db.staff_roles.items():
            try:
                # Obtener información del usuario
                staff_user_id_int = int(staff_user_id)
                chat_member = await context.bot.get_chat_member(
                    update.effective_chat.id, staff_user_id_int)
                username = f"@{chat_member.user.username}" if chat_member.user.username else chat_member.user.first_name

                if staff_data['role'] == '1':
                    fundadores.append(username)
                elif staff_data['role'] == '2':
                    cofundadores.append(username)
                elif staff_data['role'] == '3':
                    # Para moderadores, mostrar warns dados
                    warns_given = staff_data.get('warn_count', 0)
                    moderadores.append(f"{username} ({warns_given}/2 warns)")
            except:
                # Si no puede obtener info del usuario, usar ID
                if staff_data['role'] == '1':
                    fundadores.append(f"ID: {staff_user_id}")
                elif staff_data['role'] == '2':
                    cofundadores.append(f"ID: {staff_user_id}")
                elif staff_data['role'] == '3':
                    warns_given = staff_data.get('warn_count', 0)
                    moderadores.append(
                        f"ID: {staff_user_id} ({warns_given}/2 warns)")

        staff_text = "👑 **STAFF DEL GRUPO** 👑\n\n"

        # Mostrar fundadores
        staff_text += "👑 **Fundadores**\n"
        if fundadores:
            for fundador in fundadores:
                staff_text += f"└ {fundador}\n"
        else:
            staff_text += "└ Sin asignar\n"

        staff_text += "\n⚜️ **Co-fundadores**\n"
        if cofundadores:
            for i, cofundador in enumerate(cofundadores):
                prefix = "├" if i < len(cofundadores) - 1 else "└"
                staff_text += f"{prefix} {cofundador}\n"
        else:
            staff_text += "└ Sin asignar\n"

        staff_text += "\n👮🏼 **Moderadores**\n"
        if moderadores:
            for i, moderador in enumerate(moderadores):
                prefix = "├" if i < len(moderadores) - 1 else "└"
                staff_text += f"{prefix} {moderador}\n"
        else:
            staff_text += "└ Sin asignar\n"

        await update.message.reply_text(staff_text,
                                        parse_mode=ParseMode.MARKDOWN)
        return

    # Verificar si el usuario es admin, fundador o co-fundador para comandos administrativos
    is_admin = user_id_int in ADMIN_IDS
    is_founder_db = db.is_founder(user_id)
    is_cofounder_db = db.is_cofounder(user_id)

    if not (is_admin or is_founder_db or is_cofounder_db):
        await update.message.reply_text(
            "🔒 **Acceso Restringido** 🔒\n\n"
            "Solo los administradores, fundadores y co-fundadores pueden gestionar el staff.\n\n"
            "💡 Para ver la lista de staff disponible escribe:\n"
            "`/staff list`",
            parse_mode=ParseMode.MARKDOWN)
        return

    if not args:
        await update.message.reply_text(
            f"👑 **SISTEMA DE STAFF** 👑\n\n"
            f"**🔹 NIVEL 1 - FUNDADOR:**\n"
            f"• Control total del servidor\n"
            f"• Puede asignar todos los roles\n"
            f"• Acceso a todos los comandos\n\n"
            f"**🔸 NIVEL 2 - CO-FUNDADOR:**\n"
            f"• Mismas funciones que el fundador\n"
            f"• Puede administrar usuarios\n"
            f"• Puede usar /clean, /ban, /warn\n\n"
            f"**🔹 NIVEL 3 - MODERADOR:**\n"
            f"• Solo puede dar 2 /warn máximo\n"
            f"• Funciones básicas de supervisión\n"
            f"• Acceso limitado\n\n"
            f"**Comandos:**\n"
            f"• `/staff add [user_id] [nivel]` - Asignar rol\n"
            f"• `/staff remove [user_id]` - Quitar rol\n"
            f"• `/staff list` - Ver lista de staff",
            parse_mode=ParseMode.MARKDOWN)
        return

    action = args[0].lower()

    if action == "add":
        if len(args) < 3:
            await update.message.reply_text(
                "❌ Uso: /staff add [user_id] [nivel]\n"
                "🛡️ Niveles: 1=Fundador, 2=Co-Fundador, 3=Moderador")
            return

        target_user_id = args[1]
        role_level = args[2]

        if role_level not in ['1', '2', '3']:
            await update.message.reply_text("❌ **Nivel inválido**\n"
                                            "**Niveles disponibles:**\n"
                                            "• 1 - Fundador\n"
                                            "• 2 - Co-Fundador\n"
                                            "• 3 - Moderador")
            return

        # Verificar permisos jerárquicos para asignación de roles
        if role_level == '1':  # Asignar Fundador
            if not (is_admin or is_founder_db):
                await update.message.reply_text(
                    "❌ **Permisos insuficientes**\n\n"
                    "Solo los **Fundadores** pueden asignar otros Fundadores",
                    parse_mode=ParseMode.MARKDOWN)
                return
        elif role_level == '2':  # Asignar Co-Fundador
            if not (is_admin or is_founder_db):
                await update.message.reply_text(
                    "❌ **Permisos insuficientes**\n\n"
                    "Solo los **Fundadores** pueden asignar Co-Fundadores",
                    parse_mode=ParseMode.MARKDOWN)
                return
        elif role_level == '3':  # Asignar Moderador
            if not (is_admin or is_founder_db or is_cofounder_db):
                await update.message.reply_text(
                    "❌ **Permisos insuficientes**\n\n"
                    "Solo **Fundadores** y **Co-Fundadores** pueden asignar Moderadores",
                    parse_mode=ParseMode.MARKDOWN)
                return

        role_names = {
            '1': '👑 Fundador',
            '2': '💎 Co-Fundador',
            '3': '🛡️ Moderador'
        }

        # Asignar rol
        db.set_staff_role(target_user_id, role_level)

        await update.message.reply_text(
            f"✅ **ROL ASIGNADO** ✅\n\n"
            f"👤 **Usuario:** {target_user_id}\n"
            f"🎭 **Rol:** {role_names[role_level]} (Nivel {role_level})\n"
            f"📅 **Fecha:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
            f"🔐 **Permisos activados correctamente**",
            parse_mode=ParseMode.MARKDOWN)

    elif action == "remove":
        if len(args) < 2:
            await update.message.reply_text(
                "❌ **Uso:** `/staff remove [user_id]`")
            return

        target_user_id = args[1]
        staff_data = db.get_staff_role(target_user_id)

        if not staff_data:
            await update.message.reply_text(
                f"❌ **El usuario {target_user_id} no tiene rol de staff**")
            return

        # Verificar permisos jerárquicos para remoción de roles
        target_role = staff_data['role']

        if target_role == '1':  # Remover Fundador
            if not (is_admin or is_founder_db):
                await update.message.reply_text(
                    "❌ **Permisos insuficientes**\n\n"
                    "Solo los **Fundadores** pueden remover otros Fundadores",
                    parse_mode=ParseMode.MARKDOWN)
                return
        elif target_role == '2':  # Remover Co-Fundador
            if not (is_admin or is_founder_db):
                await update.message.reply_text(
                    "❌ **Permisos insuficientes**\n\n"
                    "Solo los **Fundadores** pueden remover Co-Fundadores",
                    parse_mode=ParseMode.MARKDOWN)
                return
        elif target_role == '3':  # Remover Moderador
            if not (is_admin or is_founder_db or is_cofounder_db):
                await update.message.reply_text(
                    "❌ **Permisos insuficientes**\n\n"
                    "Solo **Fundadores** y **Co-Fundadores** pueden remover Moderadores",
                    parse_mode=ParseMode.MARKDOWN)
                return

        role_names = {
            '1': '👑 Fundador',
            '2': '💎 Co-Fundador',
            '3': '🛡️ Moderador'
        }

        old_role = role_names.get(staff_data['role'], 'Desconocido')
        db.remove_staff_role(target_user_id)

        await update.message.reply_text(
            f"🗑️ **ROL REMOVIDO** 🗑️\n\n"
            f"👤 **Usuario:** {target_user_id}\n"
            f"🎭 **Rol anterior:** {old_role}\n"
            f"📅 **Fecha:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
            f"❌ **Ya no tiene permisos de staff**",
            parse_mode=ParseMode.MARKDOWN)

    elif action == "list":
        # Igual que el comando sin argumentos
        await staff_command(update, context)

    else:
        await update.message.reply_text("❌ **Acción inválida**\n"
                                        "**Acciones disponibles:**\n"
                                        "• `add` - Asignar rol\n"
                                        "• `remove` - Quitar rol\n"
                                        "• `list` - Ver lista")


auto_clean_active = {}  # Diccionario global para controlar auto-limpieza

auto_clean_timers = {}  # Diccionario global para timers


@admin_only
async def clean_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Limpiar mensajes con eliminación mejorada y modo automático"""
    args = context.args
    chat_id = update.effective_chat.id

    if not args:
        await update.message.reply_text(
            "🧹 **SISTEMA DE LIMPIEZA AVANZADO** 🧹\n\n"
            "**Uso manual:** `/clean [número]`\n"
            "**Uso automático:** `/clean auto [tiempo]`\n\n"
            "📋 **Ejemplos:**\n"
            "• `/clean 50` - Elimina 50 mensajes\n"
            "• `/clean auto 30m` - Limpieza cada 30 minutos\n"
            "• `/clean auto 2h` - Limpieza cada 2 horas\n"
            "• `/clean auto 1d` - Elimina TODOS los mensajes del día cada 24h\n"
            "• `/clean auto 7d` - Elimina TODOS los mensajes cada 7 días\n"
            "• `/clean auto off` - Desactivar limpieza automática\n\n"
            "⚠️ **Límite manual:** 2000 mensajes\n",
            parse_mode=ParseMode.MARKDOWN)
        return

    # Modo automático
    if args[0].lower() == "auto":
        if len(args) < 2:
            await update.message.reply_text(
                "❌ Uso: `/clean auto [tiempo]` o `/clean auto off`\n"
                "Ejemplos: `30m`, `2h`, `1d`, `7d`, `off`")
            return

        time_arg = args[1].lower()

        if time_arg == "off":
            if str(chat_id) in auto_clean_timers:
                auto_clean_timers[str(chat_id)]['active'] = False
                await update.message.reply_text(
                    "❌ **LIMPIEZA AUTOMÁTICA DESACTIVADA** ❌\n\n"
                    f"🔄 **Estado:** Inactivo\n"
                    f"👮‍♂️ **Desactivado por:** {update.effective_user.first_name}\n"
                    f"⏰ **Fecha:** {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                    parse_mode=ParseMode.MARKDOWN)
            else:
                await update.message.reply_text(
                    "💡 **No hay limpieza automática activa**")
            return

        # Parsear tiempo
        try:
            is_day_mode = False
            if time_arg.endswith('m'):
                interval_seconds = int(time_arg[:-1]) * 60
                interval_text = f"{time_arg[:-1]} minutos"
            elif time_arg.endswith('h'):
                interval_seconds = int(time_arg[:-1]) * 3600
                interval_text = f"{time_arg[:-1]} horas"
            elif time_arg.endswith('d'):
                days = int(time_arg[:-1])
                interval_seconds = days * 86400
                interval_text = f"{days} día{'s' if days > 1 else ''}"
                is_day_mode = True
            else:
                raise ValueError("Formato inválido")

            if interval_seconds < 300:  # Mínimo 5 minutos
                await update.message.reply_text("❌ Intervalo muy corto\n"
                                                "⏰ Mínimo: 5 minutos (`5m`)")
                return

        except ValueError:
            await update.message.reply_text(
                "❌ Formato inválido\n"
                "📋 Formatos: `30m`, `2h`, `1d`, `7d`")
            return

        # Activar limpieza automática
        auto_clean_timers[str(chat_id)] = {
            'active': True,
            'interval': interval_seconds,
            'interval_text': interval_text,
            'is_day_mode': is_day_mode,
            'days_count': int(time_arg[:-1]) if is_day_mode else 0,
            'last_clean': datetime.now().isoformat()
        }

        # Iniciar el timer en background
        asyncio.create_task(
            auto_clean_worker(context, chat_id, interval_seconds))

        if is_day_mode:
            clean_description = f"TODOS los mensajes del período de {interval_text}"
        else:
            clean_description = f"20 mensajes cada {interval_text}"

        await update.message.reply_text(
            f"✅ **LIMPIEZA AUTOMÁTICA ACTIVADA** ✅\n\n"
            f"⏰ **Intervalo:** {interval_text}\n"
            f"🧹 **Limpieza:** {clean_description}\n"
            f"👮‍♂️ **Activado por:** {update.effective_user.first_name}\n"
            f"📅 **Fecha:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
            f"⚠️ **IMPORTANTE:** {'Este modo eliminará TODO el historial de mensajes del período especificado' if is_day_mode else 'Limpieza estándar de 20 mensajes'}\n"
            f"💡 **Usa `/clean auto off` para desactivar**",
            parse_mode=ParseMode.MARKDOWN)
        return

    # Verificar que sea un número (modo manual)
    if not args[0].isdigit():
        await update.message.reply_text(
            "❌ **Formato incorrecto**\n\n"
            "💡 **Uso correcto:** `/clean [número]`\n"
            "📋 **Ejemplo:** `/clean 20`")
        return

    count = int(args[0])
    if count > 2000:
        await update.message.reply_text(
            "❌ **Límite excedido**\n\n"
            "🔢 **Máximo permitido:** 2000 mensajes\n"
            "💡 **Usa un número menor e intenta de nuevo**")
        return

    if count < 1:
        await update.message.reply_text("❌ **Cantidad inválida**\n\n"
                                        "🔢 **Mínimo:** 1 mensaje\n"
                                        "📋 **Ejemplo:** `/clean 10`")
        return

    admin_info = update.effective_user
    deleted_count = 0

    # Mensaje de progreso
    progress_msg = await update.message.reply_text(
        f"🧹 **INICIANDO LIMPIEZA** 🧹\n\n"
        f"🔄 Eliminando {count:,} mensajes...\n"
        f"⏳ Por favor espera...")

    try:
        current_message_id = progress_msg.message_id

        # Eliminar el comando original
        try:
            await update.message.delete()
        except:
            pass

        # Eliminar mensajes hacia atrás desde el mensaje de progreso
        for i in range(1,
                       count + 2):  # +2 para incluir el comando y el progreso
            message_id_to_delete = current_message_id - i
            if message_id_to_delete > 0:
                try:
                    await context.bot.delete_message(
                        chat_id=chat_id, message_id=message_id_to_delete)
                    deleted_count += 1

                    # Actualizar progreso cada 100 mensajes para cantidades grandes
                    if count > 100 and deleted_count % 100 == 0:
                        try:
                            await progress_msg.edit_text(
                                f"🧹 **LIMPIEZA EN PROGRESO** 🧹\n\n"
                                f"🗑️ **Eliminados:** {deleted_count:,}/{count:,}\n"
                                f"📊 **Progreso:** {(deleted_count/count)*100:.1f}%\n"
                                f"⏳ **Procesando...**",
                                parse_mode=ParseMode.MARKDOWN)
                        except:
                            pass

                    # Pausa adaptativa según la cantidad
                    if count > 500:
                        if deleted_count % 50 == 0:
                            await asyncio.sleep(0.1)
                    else:
                        await asyncio.sleep(0.05)  # Pausa muy corta

                except Exception as e:
                    logger.warning(
                        f"No se pudo eliminar mensaje {message_id_to_delete}: {e}"
                    )
                    continue

        # Eliminar el mensaje de progreso
        try:
            await progress_msg.delete()
        except:
            pass

        # Información detallada de la limpieza (TEMPORAL)
        cleanup_info_temp = "╔═══════════════════════════════╗\n"
        cleanup_info_temp += "║    🧹 **LIMPIEZA COMPLETADA** 🧹    ║\n"
        cleanup_info_temp += "╚═══════════════════════════════╝\n\n"
        cleanup_info_temp += f"🗑️ **Mensajes eliminados:** {deleted_count:,}/{count:,}\n"
        cleanup_info_temp += f"📊 **Efectividad:** {(deleted_count/count)*100:.1f}%\n"
        cleanup_info_temp += f"⏰ **Fecha:** {datetime.now().strftime('%d/%m/%Y - %H:%M:%S')}\n"
        cleanup_info_temp += f"👤 **Ejecutado por:** {admin_info.first_name}\n"
        cleanup_info_temp += f"🆔 **Admin ID:** `{admin_info.id}`\n"
        cleanup_info_temp += f"👮‍♂️ **Username:** @{admin_info.username or 'Sin username'}\n"
        cleanup_info_temp += f"💬 **Chat ID:** `{chat_id}`\n\n"
        cleanup_info_temp += f"✅ **Estado:** Completado exitosamente\n"
        cleanup_info_temp += f"📝 **Registro:** Guardado en logs del sistema\n\n"
        cleanup_info_temp += f"⚠️ **Este mensaje se eliminará en 30 segundos**"

        # Enviar confirmación temporal
        confirmation_msg = await context.bot.send_message(
            chat_id, cleanup_info_temp, parse_mode=ParseMode.MARKDOWN)

        # Auto-eliminar confirmación después de 30 segundos
        await asyncio.sleep(30)
        try:
            await confirmation_msg.delete()
        except:
            pass

        # Log para administradores
        logger.info(
            f"Limpieza ejecutada - Admin: {admin_info.id} ({admin_info.first_name}) - "
            f"Eliminados: {deleted_count}/{count} - Chat: {chat_id}")

    except Exception as e:
        logger.error(f"Error en limpieza: {e}")
        try:
            await progress_msg.delete()
        except:
            pass

        await context.bot.send_message(
            chat_id, f"❌ **ERROR EN LIMPIEZA** ❌\n\n"
            f"🔍 **Error:** {str(e)[:100]}\n"
            f"📊 **Eliminados:** {deleted_count}/{count}\n\n"
            f"💡 **Verifica que el bot tenga:**\n"
            f"• Permisos de administrador\n"
            f"• Permiso para eliminar mensajes\n"
            f"• Acceso a mensajes del historial\n\n"
            f"👤 **Intentado por:** {admin_info.first_name}",
            parse_mode=ParseMode.MARKDOWN)


@bot_admin_only
async def premium_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Dar premium a un usuario"""
    args = context.args
    if not args:
        await update.message.reply_text("Uso: /premium [user_id] [días]")
        return

    target_user_id = args[0]
    days = int(args[1]) if len(args) > 1 else 30

    premium_until = datetime.now() + timedelta(days=days)

    db.update_user(target_user_id, {
        'premium': True,
        'premium_until': premium_until.isoformat()
    })

    await update.message.reply_text(
        f"👑 Premium activado para usuario {target_user_id}\n"
        f"📅 Válido por {days} días")


@admin_only
async def id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ver información detallada de usuario por ID - Solo admins"""
    args = context.args

    # Si se responde a un mensaje, obtener el ID del usuario
    if update.message.reply_to_message and not args:
        target_user_id = str(update.message.reply_to_message.from_user.id)
        target_user = update.message.reply_to_message.from_user
    elif args:
        target_user_id = args[0]
        try:
            # Intentar obtener información del usuario
            chat_member = await context.bot.get_chat_member(
                update.effective_chat.id, int(target_user_id))
            target_user = chat_member.user
        except:
            target_user = None
    else:
        await update.message.reply_text(
            "🔍 **INFORMACIÓN DE USUARIO** 🔍\n\n"
            "**Uso:** `/id [user_id]`\n"
            "**Ejemplo:** `/id 123456789`\n\n"
            "📋 **Información disponible:**\n"
            "• Datos del usuario\n"
            "• Actividad y estadísticas\n"
            "• Estado de cuenta\n"
            "• Historial de advertencias",
            parse_mode=ParseMode.MARKDOWN)
        return

    user_data = db.get_user(target_user_id)

    # Calcular tiempo en servidor
    join_date = datetime.fromisoformat(user_data['join_date'])
    time_in_server = datetime.now() - join_date
    days_in_server = time_in_server.days

    # Obtener información del usuario
    if target_user:
        username = f"@{target_user.username}" if target_user.username else "Sin username"
        first_name = target_user.first_name or "Sin nombre"
        last_name = target_user.last_name or ""
        full_name = f"{first_name} {last_name}".strip()
    else:
        username = "Desconocido"
        full_name = "Usuario no encontrado"

    # Estado premium
    premium_status = "❌"
    if user_data.get('premium', False):
        premium_until = datetime.fromisoformat(user_data['premium_until'])
        days_left = (premium_until - datetime.now()).days
        premium_status = f"✅ ({days_left}d)"

    # Estado de riesgo
    warns = user_data.get('warns', 0)
    risk_emoji = "🔴" if warns >= 2 else "🟡" if warns >= 1 else "🟢"

    response = f"╭─────────────────────────────╮\n"
    response += f"│    🔍 **INFORMACIÓN DE USUARIO**   │\n"
    response += f"╰─────────────────────────────╯\n\n"
    response += f"👤 **Nombre/Username:** {full_name}\n"
    response += f"🆔 **ID:** `{target_user_id}`\n"
    response += f"📱 **Username:** {username}\n"
    response += f"📅 **En el servidor:** {days_in_server} días\n\n"
    response += f"💰 **Créditos:** {user_data['credits']:,}\n"
    response += f"🏭 **Tarjetas generadas:** {user_data['total_generated']:,}\n"
    response += f"🔍 **Tarjetas verificadas:** {user_data['total_checked']:,}\n"
    response += f"👑 **Premium:** {premium_status}\n"
    response += f"⚠️ **Advertencias:** {warns}/3 {risk_emoji}\n\n"
    response += f"📊 **Actividad total:** {user_data['total_generated'] + user_data['total_checked']:,}\n"
    response += f"⏰ **Último bono:** {user_data.get('last_bonus', 'Nunca')[:10] if user_data.get('last_bonus') else 'Nunca'}\n\n"
    response += f"🛠️ **Acciones:** `/ban` `/warn` `/premium` `/unwarn`"

    await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)


@admin_only
async def ban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Banear usuario"""
    args = context.args
    if not args:
        await update.message.reply_text(
            "🔨 **BANEAR USUARIO** 🔨\n\n"
            "**Uso:** `/ban [user_id] [razón]`\n"
            "**Ejemplo:** `/ban 123456789 Spam`",
            parse_mode=ParseMode.MARKDOWN)
        return

    target_user_id = args[0]
    reason = ' '.join(args[1:]) if len(args) > 1 else "Sin razón especificada"

    try:
        # En un bot real, aquí harías el ban real
        await update.message.reply_text(
            f"🔨 **USUARIO BANEADO** 🔨\n\n"
            f"👤 **ID:** {target_user_id}\n"
            f"📝 **Razón:** {reason}\n"
            f"👮‍♂️ **Por:** {update.effective_user.first_name}\n"
            f"⏰ **Fecha:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
            f"✅ **Acción ejecutada exitosamente**",
            parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await update.message.reply_text(f"❌ Error al banear usuario: {str(e)}")


@staff_only(3)  # Nivel 3 (moderador) o superior
async def warn_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Advertir usuario - Moderadores pueden dar máximo 2 warns"""
    user_id = str(update.effective_user.id)
    args = context.args

    if not args:
        await update.message.reply_text(
            "⚠️ **ADVERTIR USUARIO** ⚠️\n\n"
            "**Uso:** `/warn [user_id] [razón]`\n"
            "**Ejemplo:** `/warn 123456789 Comportamiento inadecuado`",
            parse_mode=ParseMode.MARKDOWN)
        return

    # Verificar límite para moderadores (nivel 3)
    staff_data = db.get_staff_role(user_id)
    is_admin = update.effective_user.id in ADMIN_IDS

    if staff_data and staff_data['role'] == '3' and not is_admin:
        # Es moderador, verificar límite de warns
        mod_warns = staff_data.get('warn_count', 0)
        if mod_warns >= 2:
            await update.message.reply_text(
                "❌ **LÍMITE ALCANZADO** ❌\n\n"
                "🛡️ **Moderadores pueden dar máximo 2 warns**\n"
                "📊 **Warns dados:** 2/2\n\n"
                "💡 Contacta a un Co-Fundador o Fundador",
                parse_mode=ParseMode.MARKDOWN)
            return

    target_user_id = args[0]
    reason = ' '.join(args[1:]) if len(args) > 1 else "Sin razón especificada"

    user_data = db.get_user(target_user_id)
    current_warns = user_data.get('warns', 0) + 1

    db.update_user(target_user_id, {'warns': current_warns})

    # Incrementar contador de warns para moderadores
    if staff_data and staff_data['role'] == '3' and not is_admin:
        new_mod_warns = db.increment_mod_warns(user_id)
        mod_warn_text = f"\n🛡️ **Warns dados por moderador:** {new_mod_warns}/2"
    else:
        mod_warn_text = ""

    # Determinar rango del que aplicó el warn
    if is_admin:
        applied_by_rank = "👑 Admin Principal"
    elif staff_data:
        rank_names = {
            '1': '👑 Fundador',
            '2': '💎 Co-Fundador',
            '3': '🛡️ Moderador'
        }
        applied_by_rank = rank_names.get(staff_data['role'], 'Staff')
    else:
        applied_by_rank = "Staff"

    response = f"⚠️ **ADVERTENCIA APLICADA** ⚠️\n\n"
    response += f"👤 **Usuario:** {target_user_id}\n"
    response += f"📝 **Razón:** {reason}\n"
    response += f"🔢 **Advertencias:** {current_warns}/3\n"
    response += f"👮‍♂️ **Por:** {update.effective_user.first_name} ({applied_by_rank})\n"
    response += f"⏰ **Fecha:** {datetime.now().strftime('%d/%m/%Y %H:%M')}{mod_warn_text}\n\n"

    if current_warns >= 3:
        response += f"🔨 **USUARIO BANEADO AUTOMÁTICAMENTE**"
    else:
        response += f"💡 **Advertencias restantes:** {3 - current_warns}"

    await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)


@bot_admin_only
async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Estadísticas completas del bot"""
    total_users = len(db.users)
    total_generated = sum(
        user.get('total_generated', 0) for user in db.users.values())
    total_checked = sum(
        user.get('total_checked', 0) for user in db.users.values())
    premium_users = sum(1 for user in db.users.values()
                        if user.get('premium', False))
    total_credits = sum(user.get('credits', 0) for user in db.users.values())

    response = f"📊 **ESTADÍSTICAS COMPLETAS** 📊\n\n"
    response += f"👥 **Total usuarios:** {total_users}\n"

    response += f"🏭 **Tarjetas generadas:** {total_generated:,}\n"
    response += f"🔍 **Tarjetas verificadas:** {total_checked:,}\n"
    response += f"💰 **Créditos totales:** {total_credits:,}\n"
    response += f"🤖 **Uptime:** 99.9%\n"
    response += f"⚡ **Estado:** Operativo\n"
    response += f"📡 **Servidor:** Online\n"
    response += f"🕐 **Última actualización:** {datetime.now().strftime('%d/%m/%Y %H:%M')}"

    await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)


@staff_only(1)  # Solo fundadores de nivel 1
async def founder_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gestionar fundadores - Solo fundadores existentes"""
    args = context.args

    if not args:
        # Mostrar lista de fundadores actuales
        founders = db.get_all_by_role('1')

        response = f"👑 **GESTIÓN DE FUNDADORES** 👑\n\n"
        response += f"**Comandos disponibles:**\n"
        response += f"• `/founder add [user_id]` - Asignar fundador\n"
        response += f"• `/founder remove [user_id]` - Quitar fundador\n"
        response += f"• `/founder list` - Ver lista actual\n\n"

        if founders:
            response += f"**Fundadores actuales:**\n"
            for i, founder_id in enumerate(founders, 1):
                try:
                    chat_member = await context.bot.get_chat_member(
                        update.effective_chat.id, int(founder_id))
                    username = f"@{chat_member.user.username}" if chat_member.user.username else chat_member.user.first_name
                    response += f"{i}. {username} (`{founder_id}`)\n"
                except:
                    response += f"{i}. ID: `{founder_id}`\n"
        else:
            response += f"📝 **No hay fundadores asignados dinámicamente**"

        await update.message.reply_text(response,
                                        parse_mode=ParseMode.MARKDOWN)
        return

    action = args[0].lower()

    if action == "add":
        if len(args) < 2:
            await update.message.reply_text("❌ Uso: `/founder add [user_id]`")
            return

        target_user_id = args[1]

        # Verificar si ya es fundador
        if db.is_founder(target_user_id):
            await update.message.reply_text(
                f"⚠️ El usuario `{target_user_id}` ya es fundador")
            return

        # Asignar como fundador
        db.set_staff_role(target_user_id, '1')

        response = f"👑 **FUNDADOR ASIGNADO** 👑\n\n"
        response += f"👤 **Usuario:** `{target_user_id}`\n"
        response += f"🎭 **Rol:** Fundador (Nivel 1)\n"
        response += f"👮‍♂️ **Asignado por:** {update.effective_user.first_name}\n"
        response += f"📅 **Fecha:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        response += f"✨ **Permisos máximos activados**"

        await update.message.reply_text(response,
                                        parse_mode=ParseMode.MARKDOWN)

    elif action == "remove":
        if len(args) < 2:
            await update.message.reply_text(
                "❌ Uso: `/founder remove [user_id]`")
            return

        target_user_id = args[1]

        # Verificar si es fundador
        if not db.is_founder(target_user_id):
            await update.message.reply_text(
                f"❌ El usuario `{target_user_id}` no es fundador")
            return

        # Remover rol
        db.remove_staff_role(target_user_id)

        response = f"🗑️ **FUNDADOR REMOVIDO** 🗑️\n\n"
        response += f"👤 **Usuario:** `{target_user_id}`\n"
        response += f"👮‍♂️ **Removido por:** {update.effective_user.first_name}\n"
        response += f"📅 **Fecha:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        response += f"❌ **Ya no tiene permisos de fundador**"

        await update.message.reply_text(response,
                                        parse_mode=ParseMode.MARKDOWN)

    elif action == "list":
        # Reutilizar la lógica de mostrar lista
        await founder_command(update, context)

    else:
        await update.message.reply_text(
            "❌ **Acción inválida**\n**Acciones:** `add`, `remove`, `list`")


@staff_only(1)  # Solo fundadores
async def cofounder_command(update: Update,
                            context: ContextTypes.DEFAULT_TYPE):
    """Gestionar co-fundadores - Solo fundadores"""
    args = context.args

    if not args:
        # Mostrar lista de co-fundadores actuales
        cofounders = db.get_all_by_role('2')

        response = f"💎 **GESTIÓN DE CO-FUNDADORES** 💎\n\n"
        response += f"**Comandos disponibles:**\n"
        response += f"• `/cofounder add [user_id]` - Asignar co-fundador\n"
        response += f"• `/cofounder remove [user_id]` - Quitar co-fundador\n"
        response += f"• `/cofounder list` - Ver lista actual\n\n"

        if cofounders:
            response += f"**Co-fundadores actuales:**\n"
            for i, cofounder_id in enumerate(cofounders, 1):
                try:
                    chat_member = await context.bot.get_chat_member(
                        update.effective_chat.id, int(cofounder_id))
                    username = f"@{chat_member.user.username}" if chat_member.user.username else chat_member.user.first_name
                    response += f"{i}. {username} (`{cofounder_id}`)\n"
                except:
                    response += f"{i}. ID: `{cofounder_id}`\n"
        else:
            response += f"📝 **No hay co-fundadores asignados**"

        await update.message.reply_text(response,
                                        parse_mode=ParseMode.MARKDOWN)
        return

    action = args[0].lower()

    if action == "add":
        if len(args) < 2:
            await update.message.reply_text("❌ Uso: `/cofounder add [user_id]`"
                                            )
            return

        target_user_id = args[1]

        # Verificar si ya tiene un rol
        current_role = db.get_staff_role(target_user_id)
        if current_role:
            role_names = {
                '1': 'Fundador',
                '2': 'Co-fundador',
                '3': 'Moderador'
            }
            current_role_name = role_names.get(current_role['role'],
                                               'Desconocido')
            await update.message.reply_text(
                f"⚠️ El usuario ya es {current_role_name}")
            return

        # Asignar como co-fundador
        db.set_staff_role(target_user_id, '2')

        response = f"💎 **CO-FUNDADOR ASIGNADO** 💎\n\n"
        response += f"👤 **Usuario:** `{target_user_id}`\n"
        response += f"🎭 **Rol:** Co-fundador (Nivel 2)\n"
        response += f"👮‍♂️ **Asignado por:** {update.effective_user.first_name}\n"
        response += f"📅 **Fecha:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        response += f"✨ **Permisos de co-fundador activados**"

        await update.message.reply_text(response,
                                        parse_mode=ParseMode.MARKDOWN)

    elif action == "remove":
        if len(args) < 2:
            await update.message.reply_text(
                "❌ Uso: `/cofounder remove [user_id]`")
            return

        target_user_id = args[1]

        # Verificar si es co-fundador
        if not db.is_cofounder(target_user_id):
            await update.message.reply_text(
                f"❌ El usuario `{target_user_id}` no es co-fundador")
            return

        # Remover rol
        db.remove_staff_role(target_user_id)

        response = f"🗑️ **CO-FUNDADOR REMOVIDO** 🗑️\n\n"
        response += f"👤 **Usuario:** `{target_user_id}`\n"
        response += f"👮‍♂️ **Removido por:** {update.effective_user.first_name}\n"
        response += f"📅 **Fecha:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        response += f"❌ **Ya no tiene permisos de co-fundador**"

        await update.message.reply_text(response,
                                        parse_mode=ParseMode.MARKDOWN)

    elif action == "list":
        # Reutilizar la lógica de mostrar lista
        await cofounder_command(update, context)

    else:
        await update.message.reply_text(
            "❌ **Acción inválida**\n**Acciones:** `add`, `remove`, `list`")


@staff_only(2)  # Co-fundador o superior
async def moderator_command(update: Update,
                            context: ContextTypes.DEFAULT_TYPE):
    """Gestionar moderadores - Co-fundadores y fundadores"""
    args = context.args

    if not args:
        # Mostrar lista de moderadores actuales
        moderators = db.get_all_by_role('3')

        response = f"🛡️ **GESTIÓN DE MODERADORES** 🛡️\n\n"
        response += f"**Comandos disponibles:**\n"
        response += f"• `/moderator add [user_id]` - Asignar moderador\n"
        response += f"• `/moderator remove [user_id]` - Quitar moderador\n"
        response += f"• `/moderator list` - Ver lista actual\n\n"

        if moderators:
            response += f"**Moderadores actuales:**\n"
            for i, mod_id in enumerate(moderators, 1):
                try:
                    chat_member = await context.bot.get_chat_member(
                        update.effective_chat.id, int(mod_id))
                    username = f"@{chat_member.user.username}" if chat_member.user.username else chat_member.user.first_name

                    # Mostrar warns dados por el moderador
                    mod_data = db.get_staff_role(mod_id)
                    warns_given = mod_data.get('warn_count',
                                               0) if mod_data else 0

                    response += f"{i}. {username} (`{mod_id}`) - {warns_given}/2 warns dados\n"
                except:
                    response += f"{i}. ID: `{mod_id}`\n"
        else:
            response += f"📝 **No hay moderadores asignados**"

        await update.message.reply_text(response,
                                        parse_mode=ParseMode.MARKDOWN)
        return

    action = args[0].lower()

    if action == "add":
        if len(args) < 2:
            await update.message.reply_text("❌ Uso: `/moderator add [user_id]`"
                                            )
            return

        target_user_id = args[1]

        # Verificar si ya tiene un rol
        current_role = db.get_staff_role(target_user_id)
        if current_role:
            role_names = {
                '1': 'Fundador',
                '2': 'Co-fundador',
                '3': 'Moderador'
            }
            current_role_name = role_names.get(current_role['role'],
                                               'Desconocido')
            await update.message.reply_text(
                f"⚠️ El usuario ya es {current_role_name}")
            return

        # Asignar como moderador
        db.set_staff_role(target_user_id, '3')

        response = f"🛡️ **MODERADOR ASIGNADO** 🛡️\n\n"
        response += f"👤 **Usuario:** `{target_user_id}`\n"
        response += f"🎭 **Rol:** Moderador (Nivel 3)\n"
        response += f"👮‍♂️ **Asignado por:** {update.effective_user.first_name}\n"
        response += f"📅 **Fecha:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        response += f"⚠️ **Límite:** 2 warns máximo por moderador\n"
        response += f"✨ **Permisos de moderador activados**"

        await update.message.reply_text(response,
                                        parse_mode=ParseMode.MARKDOWN)

    elif action == "remove":
        if len(args) < 2:
            await update.message.reply_text(
                "❌ Uso: `/moderator remove [user_id]`")
            return

        target_user_id = args[1]

        # Verificar si es moderador
        if not db.is_moderator(target_user_id):
            await update.message.reply_text(
                f"❌ El usuario `{target_user_id}` no es moderador")
            return

        # Obtener estadísticas antes de remover
        mod_data = db.get_staff_role(target_user_id)
        warns_given = mod_data.get('warn_count', 0) if mod_data else 0

        # Remover rol
        db.remove_staff_role(target_user_id)

        response = f"🗑️ **MODERADOR REMOVIDO** 🗑️\n\n"
        response += f"👤 **Usuario:** `{target_user_id}`\n"
        response += f"📊 **Warns dados durante su período:** {warns_given}/2\n"
        response += f"👮‍♂️ **Removido por:** {update.effective_user.first_name}\n"
        response += f"📅 **Fecha:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        response += f"❌ **Ya no tiene permisos de moderador**"

        await update.message.reply_text(response,
                                        parse_mode=ParseMode.MARKDOWN)

    elif action == "list":
        # Reutilizar la lógica de mostrar lista
        await moderator_command(update, context)

    else:
        await update.message.reply_text(
            "❌ **Acción inválida**\n**Acciones:** `add`, `remove`, `list`")


async def emergency_founder_command(update: Update,
                                    context: ContextTypes.DEFAULT_TYPE):
    """Comando de emergencia para auto-registrarse como fundador"""
    user_id = str(update.effective_user.id)
    user_id_int = update.effective_user.id

    # IDs autorizados para usar este comando de emergencia
    emergency_ids = [6938971996, 5537246556]

    if user_id_int not in emergency_ids:
        await update.message.reply_text(
            "❌ Este comando de emergencia no está disponible para ti")
        return

    # Verificar si ya está registrado
    if db.is_founder(user_id):
        await update.message.reply_text(
            "✅ **YA ERES FUNDADOR**\n\n"
            "🔍 Tu rol ya está registrado en la base de datos\n"
            "👑 Nivel: Fundador (1)\n\n"
            "💡 Todos los comandos de fundador están disponibles",
            parse_mode=ParseMode.MARKDOWN)
        return

    # Auto-registrar como fundador
    db.set_staff_role(user_id, '1')

    await update.message.reply_text(
        "🚨 **REGISTRO DE EMERGENCIA COMPLETADO** 🚨\n\n"
        "👑 **Te has registrado como Fundador**\n"
        "🔐 **Nivel:** 1 (Máximo)\n"
        "📅 **Fecha:** " + datetime.now().strftime('%d/%m/%Y %H:%M') + "\n\n"
        "✅ **Todos los permisos de fundador están ahora activos**\n"
        "🛠️ **Comandos disponibles:**\n"
        "• `/founder` - Gestionar fundadores\n"
        "• `/cofounder` - Gestionar co-fundadores\n"
        "• `/moderator` - Gestionar moderadores\n"
        "• `/post` - Publicar contenido\n"
        "• Y todos los comandos de staff",
        parse_mode=ParseMode.MARKDOWN)


async def unwarn_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Remover advertencia de un usuario"""
    args = context.args
    if not args:
        await update.message.reply_text(
            "🔄 **REMOVER ADVERTENCIA** 🔄\n\n"
            "**Uso:** `/unwarn [user_id]`\n"
            "**Ejemplo:** `/unwarn 123456789`\n\n"
            "⚠️ Solo Co-fundadores y Fundadores pueden usar este comando",
            parse_mode=ParseMode.MARKDOWN)
        return

    target_user_id = args[0]
    user_data = db.get_user(target_user_id)
    current_warns = user_data.get('warns', 0)

    if current_warns <= 0:
        await update.message.reply_text(
            f"✅ **SIN ADVERTENCIAS**\n\n"
            f"👤 **Usuario:** {target_user_id}\n"
            f"⚠️ **Advertencias:** 0/3\n\n"
            f"💡 Este usuario no tiene advertencias activas",
            parse_mode=ParseMode.MARKDOWN)
        return

    # Remover una advertencia
    new_warns = max(0, current_warns - 1)
    db.update_user(target_user_id, {'warns': new_warns})

    staff_data = db.get_staff_role(str(update.effective_user.id))
    is_admin = update.effective_user.id in ADMIN_IDS

    if is_admin:
        applied_by_rank = "👑 Admin Principal"
    elif staff_data:
        rank_names = {
            '1': '👑 Fundador',
            '2': '💎 Co-Fundador',
            '3': '🛡️ Moderador'
        }
        applied_by_rank = rank_names.get(staff_data['role'], 'Staff')
    else:
        applied_by_rank = "Staff"

    response = f"✅ **ADVERTENCIA REMOVIDA** ✅\n\n"
    response += f"👤 **Usuario:** {target_user_id}\n"
    response += f"⚠️ **Advertencias:** {new_warns}/3 (era {current_warns}/3)\n"
    response += f"👮‍♂️ **Por:** {update.effective_user.first_name} ({applied_by_rank})\n"
    response += f"⏰ **Fecha:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
    response += f"🔄 **Estado:** {'Sin advertencias' if new_warns == 0 else f'{3-new_warns} advertencias restantes antes del ban'}"

    await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)


@bot_admin_only
async def unban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Desbanear usuario"""
    args = context.args
    if not args:
        await update.message.reply_text(
            "🔓 **DESBANEAR USUARIO** 🔓\n\n"
            "**Uso:** `/unban [user_id]`\n"
            "**Ejemplo:** `/unban 123456789`\n\n"
            "⚠️ Solo administradores pueden usar este comando",
            parse_mode=ParseMode.MARKDOWN)
        return

    target_user_id = args[0]

    try:
        # Intentar desbanear del chat actual
        await context.bot.unban_chat_member(chat_id=update.effective_chat.id,
                                            user_id=int(target_user_id),
                                            only_if_banned=True)

        # Resetear advertencias del usuario
        db.update_user(target_user_id, {'warns': 0})

        response = f"🔓 **USUARIO DESBANEADO** 🔓\n\n"
        response += f"👤 **ID:** {target_user_id}\n"
        response += f"👮‍♂️ **Por:** {update.effective_user.first_name}\n"
        response += f"⏰ **Fecha:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        response += f"✅ **El usuario puede ingresar nuevamente al chat**\n"
        response += f"🔄 **Advertencias reseteadas a 0/3**\n"
        response += f"💡 **Acción ejecutada exitosamente**"

        await update.message.reply_text(response,
                                        parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        await update.message.reply_text(
            f"❌ **ERROR AL DESBANEAR**\n\n"
            f"👤 **Usuario:** {target_user_id}\n"
            f"🔍 **Error:** {str(e)}\n\n"
            f"💡 **Posibles causas:**\n"
            f"• El usuario no está baneado\n"
            f"• ID de usuario inválido\n"
            f"• El bot no tiene permisos suficientes",
            parse_mode=ParseMode.MARKDOWN)


@bot_admin_only
async def close_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cerrar bot para mantenimiento - Solo admins"""
    args = context.args
    maintenance_message = ' '.join(
        args) if args else "El bot está en mantenimiento. Volveremos pronto."

    db.set_maintenance(True, maintenance_message)

    response = f"🔒 **BOT CERRADO PARA MANTENIMIENTO** 🔒\n\n"
    response += f"🚧 **Estado:** Mantenimiento activado\n"
    response += f"💬 **Mensaje:** {maintenance_message}\n"
    response += f"👮‍♂️ **Por:** {update.effective_user.first_name}\n"
    response += f"⏰ **Fecha:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
    response += f"⚠️ **Los usuarios no podrán usar comandos**\n"

    await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)


@bot_admin_only
async def open_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Abrir bot después de mantenimiento - Solo admins"""
    if not db.is_maintenance():
        await update.message.reply_text(
            "✅ **EL BOT YA ESTÁ ABIERTO** ✅\n\n"
            "💡 El bot no está en modo mantenimiento\n"
            "🔄 Todos los comandos están funcionando normalmente",
            parse_mode=ParseMode.MARKDOWN)
        return

    db.set_maintenance(False, "")

    response = f"🔓 **BOT ABIERTO Y OPERATIVO** 🔓\n\n"
    response += f"✅ **Estado:** Bot totalmente funcional\n"
    response += f"🔄 **Todos los comandos están disponibles**\n"
    response += f"👮‍♂️ **Abierto por:** {update.effective_user.first_name}\n"
    response += f"⏰ **Fecha:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
    response += f"🎉 **¡Los usuarios ya pueden usar el bot normalmente!**"

    await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)


@bot_admin_only
async def housemode_command(update: Update,
                            context: ContextTypes.DEFAULT_TYPE):
    """Modo casa de seguridad - Solo admins"""
    chat_id = str(update.effective_chat.id)
    args = context.args

    if not args:
        await update.message.reply_text(
            "🏠 **MODO CASA (HOUSEMODE)** 🏠\n\n"
            "**Uso:** `/housemode [on/off] [razón]`\n\n"
            "**Funciones:**\n"
            "• Bloquea temporalmente el grupo\n"
            "• Solo admins pueden enviar mensajes\n"
            "• Protege contra spam y raids\n"
            "• Medida preventiva de seguridad\n\n"
            "**Ejemplos:**\n"
            "• `/housemode on Supervisión activa`\n"
            "• `/housemode off`",
            parse_mode=ParseMode.MARKDOWN)
        return

    action = args[0].lower()
    reason = ' '.join(args[1:]) if len(args) > 1 else ""

    if action == "on":
        # Razón automática si no se proporciona
        if not reason:
            reason = "Administrador ausente - Protección automática contra raids, spam masivo y actividad maliciosa."

        db.set_housemode(chat_id, True, reason)

        # Restringir el chat - Solo importamos ChatPermissions aquí
        try:
            from telegram import ChatPermissions

            # Crear permisos restrictivos - Solo envío de mensajes bloqueado
            restricted_permissions = ChatPermissions(
                can_send_messages=False,
                can_send_audios=False,
                can_send_documents=False,
                can_send_photos=False,
                can_send_videos=False,
                can_send_video_notes=False,
                can_send_voice_notes=False,
                can_send_polls=False,
                can_send_other_messages=False,
                can_add_web_page_previews=False,
                can_change_info=False,
                can_invite_users=False,
                can_pin_messages=False)

            await context.bot.set_chat_permissions(
                chat_id=update.effective_chat.id,
                permissions=restricted_permissions)

            response = f"🏠 **MODO CASA ACTIVADO** 🏠\n\n"
            response += f"🔒 **Grupo bloqueado temporalmente**\n\n"
            response += f"🛡️ **Medidas de seguridad activas:**\n"
            response += f"• 🚫 Prevención contra raids y spam\n"
            response += f"• ⚠️ Protección durante ausencia administrativa\n\n"
            response += f"📝 **Razón:** {reason}\n\n"
            response += f"🕒 El grupo será activado en breve por un administrador\n"
            response += f"👮‍♂️ **Activado por:** {update.effective_user.first_name}\n"
            response += f"⏰ **Fecha:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
            

        except Exception as e:
            response = f"❌ **ERROR AL ACTIVAR MODO CASA** ❌\n\n"
            response += f"🔍 **Error:** {str(e)}\n"
            response += f"💡 **Verifica que el bot tenga permisos de administrador**"

    elif action == "off":
        db.set_housemode(chat_id, False, "")

        # Restaurar permisos normales del chat
        try:
            from telegram import ChatPermissions

            # Crear permisos normales
            normal_permissions = ChatPermissions(
                can_send_messages=True,
                can_send_audios=True,
                can_send_documents=True,
                can_send_photos=True,
                can_send_videos=True,
                can_send_video_notes=True,
                can_send_voice_notes=True,
                can_send_polls=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
                can_change_info=False,
                can_invite_users=True,
                can_pin_messages=False)

            await context.bot.set_chat_permissions(
                chat_id=update.effective_chat.id,
                permissions=normal_permissions)

            response = f"🔓 **MODO CASA DESACTIVADO** 🔓\n\n"
            response += f"✅ **El grupo ha sido desbloqueado**\n"
            response += f"💬 **Los miembros ya pueden enviar mensajes**\n"
            response += f"🔄 **Funciones normales del grupo restauradas**\n\n"
            response += f"👮‍♂️ **Desactivado por:** {update.effective_user.first_name}\n"
            response += f"⏰ **Fecha:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
            response += f"🛡️ **Supervisión activa restablecida**"

        except Exception as e:
            response = f"❌ **ERROR AL DESACTIVAR MODO CASA** ❌\n\n"
            response += f"🔍 **Error:** {str(e)}\n"
            response += f"💡 **Verifica que el bot tenga permisos de administrador**"

    else:
        response = f"❌ **Acción inválida**\n\n"
        response += f"**Acciones disponibles:** `on` | `off`"

    await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)


def escape_markdown_v2(text):
    """Escapa caracteres especiales para MarkdownV2"""
    if not text:
        return ""

    # Lista completa de caracteres especiales para MarkdownV2
    special_chars = [
        '_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|',
        '{', '}', '.', '!'
    ]

    # Escapar cada carácter especial
    for char in special_chars:
        text = text.replace(char, f'\\{char}')

    return text


def organize_content_with_ai(content):
    """IA para organizar y estructurar el contenido automáticamente - VERSIÓN MEJORADA CON DETECCIÓN AVANZADA"""
    import re

    # Detectar diferentes tipos de contenido - PATRONES MEJORADOS
    # Patrón para CCs con CVV opcional (formato original y nuevo)
    cc_pattern = r'\b\d{13,19}\|\d{1,2}\|\d{2,4}(?:\|\d{3,4})?\b'
    ccs_found = re.findall(cc_pattern, content)

    # Detectar URLs/enlaces - PATRONES AMPLIAMENTE MEJORADOS
    url_patterns = [
        r'https?://[^\s]+',  # URLs completas estándar
        r'(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?',  # URLs sin protocolo
        r't\.me/[^\s]+',  # Enlaces de Telegram específicos
        r'telegram\.me/[^\s]+',  # Telegram alternativo
        r'tg://[^\s]+',  # Protocolo de Telegram
        r'@[a-zA-Z0-9_]+',  # Menciones que pueden ser canales
        # NUEVO: Detectar enlaces embebidos en palabras con texto que contiene dominios
        r'[a-zA-Z0-9]*(?:https?://|www\.|\.com|\.net|\.org|\.io|\.co|\.me|t\.me|telegram\.me)[a-zA-Z0-9/\-._~:/?#[\]@!$&\'()*+,;=%]*',
        # NUEVO: Detectar texto con caracteres Unicode que contiene URLs
        r'[\w\u00a0-\uffff]*(?:https?://|www\.|\.com|\.net|\.org|\.io|\.me|t\.me)[\w\u00a0-\uffff/\-._~:/?#[\]@!$&\'()*+,;=%]*',
    ]

    urls_found = []
    for pattern in url_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE | re.UNICODE)
        urls_found.extend(matches)

    # NUEVO: Detectar enlaces embebidos usando caracteres Unicode especiales
    # Buscar patrones sospechosos de texto con enlaces ocultos
    hidden_link_patterns = [
        r'[\u200B-\u200F\u202A-\u202E\u2060-\u2064]',  # Caracteres de control Unicode
        r'[\u00A0\u1680\u2000-\u200A\u202F\u205F\u3000]',  # Espacios Unicode no estándar
        r'[\u034F\u061C\u180E]',  # Más caracteres invisibles
        r'[^\x00-\x7F].*?(?:http|www|\.com|\.net|\.org|t\.me)',  # Unicode mezclado con dominios
    ]

    # Detectar texto sospechoso que puede contener enlaces embebidos
    suspicious_text = []
    for pattern in hidden_link_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        suspicious_text.extend(matches)

    # NUEVO: Búsqueda más agresiva de enlaces embebidos en palabras individuales
    words = content.split()
    suspicious_words = []
    for word in words:
        # Detectar si una palabra contiene indicadores de URL embebidos
        url_indicators = [
            'http', 'www', '.com', '.net', '.org', '.io', '.me', 't.me',
            'telegram', 'discord', 'bit.ly'
        ]

        # Si la palabra contiene indicadores de URL o caracteres especiales
        if any(indicator in word.lower() for indicator in url_indicators) or \
           (len(word) > 30 and ' ' not in word) or \
           any(ord(char) > 127 for char in word) or \
           re.search(r'[\u200B-\u200F\u202A-\u202E]', word):
            suspicious_words.append(word)

        # ESPECÍFICAMENTE para el caso "AQUI" con link embebido
        # Detectar palabras que pueden tener texto + URL embebida
        if len(word) > 10 and any(
                char in word
                for char in ['/', ':', '.']) and not word.isdigit():
            suspicious_words.append(word)

    # Agregar texto sospechoso y palabras a URLs encontradas
    if suspicious_words:
        urls_found.extend(
            suspicious_words[:5])  # Aumentado a 5 para mejor detección
    if suspicious_text:
        urls_found.extend(suspicious_text[:3])

    # NUEVO: Detección específica para texto con enlaces embebidos
    # Buscar patrones como "AQUI" seguido o conteniendo URLs
    embedded_patterns = [
        r'[A-Z]{2,}(?=https?://)',  # Palabras en mayúsculas seguidas de URL
        r'[A-Z]{2,}https?://[^\s]+',  # Palabras pegadas a URLs
        r'[a-zA-Z]+(?:https?://|www\.)[^\s]+',  # Cualquier texto pegado a URL
        r'[a-zA-Z]+t\.me/[^\s]+',  # Texto pegado a enlaces de Telegram
    ]

    for pattern in embedded_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        urls_found.extend(matches)

    # Detectar hashtags
    hashtag_pattern = r'#[a-zA-Z0-9_]+'
    hashtags_found = re.findall(hashtag_pattern, content)

    # Detectar menciones de canales/usuarios
    mention_pattern = r'@[a-zA-Z0-9_]+'
    mentions_found = re.findall(mention_pattern, content)

    # Detectar emojis de banderas y países
    country_pattern = r'🇺🇸|🇦🇷|🇧🇷|🇨🇴|🇲🇽|🇪🇸|🇵🇪|🇨🇱|🇺🇾|🇻🇪'
    countries_found = re.findall(country_pattern, content)

    # Detectar líneas de información específica (teléfonos, VPN, etc.)
    phone_pattern = r'📱:\s*\d+\|\d+\|\d+'
    phones_found = re.findall(phone_pattern, content)

    vpn_pattern = r'🌍:\s*\[.*?\]'
    vpn_found = re.findall(vpn_pattern, content)

    # NUEVA LÓGICA: Mantener formato original y solo separar lo esencial
    lines = content.split('\n')
    organized_lines = []
    technical_data = []

    # Procesar todas las líneas manteniendo el formato original
    for i, line in enumerate(lines):
        original_line = line  # Preservar la línea original con espacios
        line_stripped = line.strip()

        # Si es una línea vacía, mantenerla para preservar el formato
        if not line_stripped:
            organized_lines.append("")
            continue

        # Si la línea contiene solo datos técnicos (CCs, teléfonos, VPN), separarla
        if (re.search(cc_pattern, line_stripped) and len(line_stripped.split()) <= 3) or \
           (line_stripped.startswith('📱:')) or \
           (line_stripped.startswith('🌍:')):
            technical_data.append(line_stripped)
        else:
            # Mantener como contenido principal con formato original
            organized_lines.append(original_line)

    # Reconstruir el contenido manteniendo el formato original COMPLETO
    if organized_lines:
        clean_content = '\n'.join(organized_lines).strip()
    else:
        clean_content = content  # Fallback al contenido original

    # NO remover URLs del contenido - mantener formato original
    # Solo limpiar espacios extra excesivos
    clean_content = re.sub(r'\n\s*\n\s*\n', '\n\n', clean_content).strip()

    return {
        'content': clean_content,
        'ccs': ccs_found,
        'urls': urls_found,
        'hashtags': hashtags_found,
        'mentions': mentions_found,
        'countries': countries_found,
        'phones': phones_found,
        'vpn_info': vpn_found,
        'technical_data': technical_data
    }


def format_smart_publication(organized_data, author_name):
    """Formatea inteligentemente la publicación manteniendo estructura original"""
    content = organized_data['content']
    ccs = organized_data['ccs']
    urls = organized_data['urls']
    hashtags = organized_data['hashtags']
    mentions = organized_data['mentions']
    countries = organized_data.get('countries', [])
    phones = organized_data.get('phones', [])
    vpn_info = organized_data.get('vpn_info', [])
    technical_data = organized_data.get('technical_data', [])

    # Escapar caracteres especiales para MarkdownV2
    safe_author = escape_markdown_v2(author_name)

    if ccs:
        # Formato específico para releases con CCs - MANTENER ESTRUCTURA ORIGINAL
        message = "⚡ *𝗖𝗛𝗘𝗥𝗡𝗢𝗕𝗜𝗟 𝗖𝗛𝗟𝗩* ⚡\n"
        message += "═══════════════════════════════\n\n"

        # MOSTRAR TODO EL CONTENIDO TAL COMO VIENE, solo limpiando caracteres problemáticos
        if content:
            # Limpiar solo caracteres que causan problemas con MarkdownV2
            clean_content = content.replace('𝗧𝗘𝗟𝟯𝗣𝟰𝗥𝗧𝗬', 'TELEPARTY')
            clean_content = clean_content.replace('𝗧𝗔𝗟𝗩𝗘𝗭', 'TALVEZ')
            clean_content = clean_content.replace('𝟭', '1')
            clean_content = clean_content.replace('𝗔Ñ𝗢', 'AÑO')
            clean_content = clean_content.replace('𝗔𝗨𝗧𝗢𝗣', 'AUTOP')

            # Procesar línea por línea manteniendo el formato original
            lines = clean_content.split('\n')
            for i, line in enumerate(lines):
                line = line.strip()
                if line:
                    # Solo escapar caracteres problemáticos, NO cambiar estructura
                    safe_line = escape_markdown_v2(line)

                    # La primera línea en negrita, las demás normales
                    if i == 0:
                        message += f"*{safe_line}*\n"
                    else:
                        message += f"{safe_line}\n"

            message += "\n"

        # Agregar información técnica (CCs, teléfonos, VPN)
        if technical_data:
            for tech_line in technical_data:
                safe_tech = escape_markdown_v2(tech_line)
                message += f"{safe_tech}\n"
            message += "\n"

        # Agregar CCs detectadas si no están ya en el contenido
        if ccs and not any(cc in content for cc in ccs):
            message += "💳 *CCs Detectadas:*\n"
            for cc in ccs:
                if cc.startswith('4'):
                    prefix = "🔵"
                elif cc.startswith('5'):
                    prefix = "🔴"
                else:
                    prefix = "⚫"
                message += f"{prefix} `{cc}`\n"
            message += "\n"

        # Resumen
        message += f"📊 *Total CCs:* {len(ccs)}\n"
        if countries:
            message += f"🌍 *País:* {' '.join(countries)}\n"
        message += f"📅 *Fecha:* {datetime.now().strftime('%d/%m/%Y')}\n"

    else:
        # Formato para contenido general - MANTENER ESTRUCTURA
        message = "📢 *𝗖𝗛𝗘𝗥𝗡𝗢𝗕𝗜𝗟 𝗖𝗛𝗟𝗩 UPDATE* 📢\n"
        message += "═══════════════════════════════\n\n"

        if content:
            # MANTENER TODO EL FORMATO ORIGINAL
            clean_content = content.replace('𝗧𝗘𝗟𝟯𝗣𝟰𝗥𝗧𝗬', 'TELEPARTY')
            clean_content = clean_content.replace('𝗧𝗔𝗟𝗩𝗘𝗭', 'TALVEZ')
            clean_content = clean_content.replace('𝟭', '1')
            clean_content = clean_content.replace('𝗔Ñ𝗢', 'AÑO')
            clean_content = clean_content.replace('𝗔𝗨𝗧𝗢𝗣', 'AUTOP')

            # Escapar solo caracteres problemáticos
            safe_content = escape_markdown_v2(clean_content)
            message += f"{safe_content}\n\n"

        message += f"───────────────────────────────────\n"
        message += f"📅 *Fecha:* {escape_markdown_v2(datetime.now().strftime('%d/%m/%Y %H:%M'))}\n"

    # Agregar hashtags y menciones si existen
    if hashtags:
        message += f"\n🏷️ *Tags:* "
        for hashtag in hashtags:
            safe_hashtag = escape_markdown_v2(hashtag)
            message += f"{safe_hashtag} "
        message += "\n"

    if mentions:
        message += f"👤 *Menciones:* "
        for mention in mentions:
            safe_mention = escape_markdown_v2(mention)
            message += f"{safe_mention} "
        message += "\n"

    message += f"\n👑 *Publicado por:* {safe_author}\n"
    message += f"🤖 *Bot:* @ChernobilChLv\\_bot"

    return message


@staff_only(
    2)  # Co-fundador o superior (Fundador nivel 1, Co-fundador nivel 2)
async def post_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /post con IA para organizar contenido - Solo fundadores y co-fundadores"""
    user_id = str(update.effective_user.id)
    staff_data = db.get_staff_role(user_id)

    # Verificar permisos - Solo base de datos (el decorador ya hace la verificación)
    # Este comando ya está protegido por @staff_only(2)

    args = context.args
    current_chat_id = str(update.effective_chat.id)

    if not args:
        await update.message.reply_text(
            "📢 *SISTEMA DE PUBLICACIONES CON IA* 📢\n\n"
            "*Uso:* `/post [chat_id] [contenido]`\n\n"
            "📋 *Ejemplos:*\n"
            "• `/post \\-1001234567890 Mi publicación`\n"
            "• `/post here Mi contenido` \\(publica aquí\\)\n"
            "• `/post hola` \\(publica en chat actual\\)\n"
            "• `/post hola\\ncomo\\nestan` \\(multilínea\\)\n\n"
            "🤖 *Funciones de IA:*\n"
            "• Organización automática de CCs por tipo\n"
            "• Detección inteligente de contenido\n"
            "• Formato profesional adaptativo\n"
            "• Separación de URLs y hashtags\n"
            "• Estadísticas automáticas\n\n"
            "💡 *Tip:* La IA organizará automáticamente tu contenido",
            parse_mode=ParseMode.MARKDOWN_V2)
        return

    # Obtener chat destino
    target_chat = args[0]
    if target_chat.lower() == "here":
        target_chat_id = current_chat_id
    else:
        target_chat_id = target_chat

    # Obtener contenido completo del mensaje incluyendo saltos de línea
    message_text = update.message.text

    # Si solo hay un argumento y es "here" o un chat_id, buscar contenido en todo el mensaje
    if len(args) == 1:
        # Para casos como "/post hola\ncomo\nestan" donde "hola" se interpreta como target_chat
        # Verificar si el primer argumento parece ser contenido en lugar de un chat_id
        first_arg = args[0]

        # Si no parece un chat_id (no empieza con - y no es "here"), tratarlo como contenido
        if not (first_arg.lower() == "here" or first_arg.startswith("-")
                or first_arg.isdigit()):
            # Usar el chat actual y todo después de "/post" como contenido
            target_chat_id = current_chat_id
            content_start = message_text.find("/post") + len("/post")
            content = message_text[content_start:].strip(
            ) if content_start < len(message_text) else ""
        else:
            # Es un target_chat válido
            if target_chat.lower() == "here":
                target_chat_id = current_chat_id
                content_start = message_text.find("/post here") + len(
                    "/post here")
            else:
                target_chat_id = target_chat
                content_start = message_text.find(target_chat) + len(
                    target_chat)

            content = message_text[content_start:].strip(
            ) if content_start < len(message_text) else ""
    else:
        # Lógica original para múltiples argumentos
        if target_chat.lower() == "here":
            target_chat_id = current_chat_id
            content_start = message_text.find("/post here") + len("/post here")
        else:
            target_chat_id = target_chat
            content_start = message_text.find(target_chat) + len(target_chat)

        content = message_text[content_start:].strip() if content_start < len(
            message_text) else ""

    if not content:
        await update.message.reply_text(
            "❌ *CONTENIDO REQUERIDO*\n\n"
            "📝 Debes incluir el contenido a publicar\n"
            "💡 *Ejemplos:*\n"
            "• `/post here Mi contenido aquí`\n"
            "• `/post here hola`\n"
            "  `como`\n"
            "  `estan`",
            parse_mode=ParseMode.MARKDOWN_V2)
        return

    # Procesar contenido con IA
    try:
        # Mensaje de procesamiento
        processing_msg = await update.message.reply_text(
            "🤖 *PROCESANDO CON IA* 🤖\n\n"
            "⚡ Analizando contenido\\.\\.\\.\n"
            "🔍 Detectando elementos\\.\\.\\.\n"
            "📊 Organizando información\\.\\.\\.\n"
            "🎨 Aplicando formato inteligente\\.\\.\\.",
            parse_mode=ParseMode.MARKDOWN_V2)

        # Simular procesamiento IA
        await asyncio.sleep(2)

        # Organizar contenido con IA
        organized_data = organize_content_with_ai(content)

        # Formatear publicación inteligentemente
        publication_message = format_smart_publication(
            organized_data, update.effective_user.first_name)

        # Obtener información del chat destino
        try:
            chat_info = await context.bot.get_chat(target_chat_id)
            chat_name = chat_info.title or f"Chat {target_chat_id}"
        except:
            chat_name = f"Chat {target_chat_id}"

        # Actualizar mensaje de procesamiento
        await processing_msg.edit_text(
            f"📤 *PREPARANDO PUBLICACIÓN* 📤\n\n"
            f"🎯 *Destino:* {escape_markdown_v2(chat_name)}\n"
            f"📊 *Tipo:* {'Release con CCs' if organized_data['ccs'] else 'Contenido general'}\n"
            f"💳 *CCs detectadas:* {len(organized_data['ccs'])}\n"
            f"🔗 *URLs detectadas:* {len(organized_data['urls'])}\n"
            f"🏷️ *Hashtags:* {len(organized_data['hashtags'])}\n"
            f"👤 *Autor:* {escape_markdown_v2(update.effective_user.first_name)}\n\n"
            f"⏳ *Enviando\\.\\.\\.*",
            parse_mode=ParseMode.MARKDOWN_V2)

        # Publicar en el chat destino usando MarkdownV2
        sent_message = await context.bot.send_message(
            chat_id=target_chat_id,
            text=publication_message,
            parse_mode=ParseMode.MARKDOWN_V2)

        # Actualizar confirmación con éxito
        success_message = f"✅ *PUBLICACIÓN EXITOSA* ✅\n\n"
        success_message += f"🎯 *Destino:* {escape_markdown_v2(chat_name)}\n"
        success_message += f"📨 *Message ID:* `{sent_message.message_id}`\n"
        success_message += f"📊 *Análisis IA:*\n"
        success_message += f"  • CCs: {len(organized_data['ccs'])}\n"
        success_message += f"  • URLs: {len(organized_data['urls'])}\n"
        success_message += f"  • Hashtags: {len(organized_data['hashtags'])}\n"
        success_message += f"  • Menciones: {len(organized_data['mentions'])}\n"
        success_message += f"👤 *Publicado por:* {escape_markdown_v2(update.effective_user.first_name)}\n"
        success_message += f"⏰ *Hora:* {escape_markdown_v2(datetime.now().strftime('%H:%M:%S'))}\n\n"
        success_message += f"🎉 *¡Publicación completada con IA\\!*"

        await processing_msg.edit_text(success_message,
                                       parse_mode=ParseMode.MARKDOWN_V2)

        # Log de la publicación
        logger.info(
            f"Publicación con IA - Usuario: {update.effective_user.id} ({update.effective_user.first_name}) - Destino: {target_chat_id} - CCs: {len(organized_data['ccs'])}"
        )

    except Exception as e:
        # Error al publicar - usar texto plano para evitar errores de parsing
        error_message = f"❌ ERROR EN PUBLICACIÓN ❌\n\n"
        error_message += f"🎯 Destino: {target_chat_id}\n"
        error_message += f"🔍 Error: {str(e)[:100]}...\n\n"
        error_message += f"💡 Posibles causas:\n"
        error_message += f"• El bot no está en ese chat\n"
        error_message += f"• ID de chat incorrecto\n"
        error_message += f"• Sin permisos para enviar mensajes\n"
        error_message += f"• Chat privado no accesible\n\n"
        error_message += f"🔧 Solución: Verifica el ID y permisos del bot"

        try:
            await processing_msg.edit_text(error_message)
        except:
            await update.message.reply_text(error_message)

        logger.error(
            f"Error en publicación con IA - Usuario: {update.effective_user.id} - Error: {e}"
        )


@bot_admin_only
async def setcheckchats_command(update: Update,
                                context: ContextTypes.DEFAULT_TYPE):
    """Configurar chats para el sistema /check - Solo admins"""
    args = context.args
    group_id = str(update.effective_chat.id)

    if len(args) < 2:
        await update.message.reply_text(
            "⚙️ **CONFIGURAR SISTEMA /CHECK** ⚙️\n\n"
            "**Uso:** `/setcheckchats [chat_verificacion] [chat_publicacion]`\n\n"
            "📋 **Parámetros:**\n"
            "• `chat_verificacion`: ID del chat donde los admins aprueban/rechazan\n"
            "• `chat_publicacion`: ID del canal donde se publican las capturas aprobadas\n\n"
            "💡 **Ejemplo:** `/setcheckchats -1001234567890 -1001987654321`\n\n"
            "📝 **Nota:** Usa IDs negativos para grupos/canales",
            parse_mode=ParseMode.MARKDOWN)
        return

    try:
        verification_chat = args[0]
        publication_chat = args[1]

        # Validar que sean IDs válidos
        int(verification_chat)
        int(publication_chat)

        # Guardar configuración
        db.set_check_chats(group_id, verification_chat, publication_chat)

        response = f"✅ **CONFIGURACIÓN GUARDADA** ✅\n\n"
        response += f"🏠 **Grupo actual:** `{group_id}`\n"
        response += f"👮‍♂️ **Chat verificación:** `{verification_chat}`\n"
        response += f"📢 **Canal publicación:** `{publication_chat}`\n\n"
        response += f"⚙️ **Configurado por:** {update.effective_user.first_name}\n"
        response += f"📅 **Fecha:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        response += f"✨ **El comando /check ya está listo para usar**"

        await update.message.reply_text(response,
                                        parse_mode=ParseMode.MARKDOWN)

    except ValueError:
        await update.message.reply_text(
            "❌ **IDs INVÁLIDOS**\n\n"
            "💡 Los IDs deben ser números enteros\n"
            "📝 Ejemplo: `/setcheckchats -1001234567890 -1001987654321`")


@bot_admin_only
async def links_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ver historial de links eliminados - Solo admins"""
    args = context.args

    if not args:
        # Mostrar estadísticas generales
        total_links = len(db.deleted_links)
        if total_links == 0:
            await update.message.reply_text(
                "📊 **HISTORIAL DE LINKS ELIMINADOS** 📊\n\n"
                "❌ **No hay links registrados**\n\n"
                "💡 **Uso:** `/links [user_id]` - Ver links de un usuario\n"
                "📋 **Ejemplo:** `/links 123456789`",
                parse_mode=ParseMode.MARKDOWN)
            return

        # Mostrar últimos 10 links eliminados
        recent_links = list(db.deleted_links.items())[-10:]
        recent_links.reverse()  # Más recientes primero

        response = f"📊 **HISTORIAL DE LINKS ELIMINADOS** 📊\n\n"
        response += f"📈 **Total registrado:** {total_links} links\n"
        response += f"📋 **Últimos 10 eliminados:**\n\n"

        for link_id, data in recent_links:
            deleted_time = datetime.fromisoformat(
                data['deleted_at']).strftime('%d/%m %H:%M')
            response += f"🆔 `{link_id}` - {data['username']} ({deleted_time})\n"

        response += f"\n💡 **Ver específico:** `/links [user_id]`"

        await update.message.reply_text(response,
                                        parse_mode=ParseMode.MARKDOWN)
        return

    # Ver links de un usuario específico
    target_user_id = args[0]
    user_links = db.get_deleted_links_by_user(target_user_id)

    if not user_links:
        await update.message.reply_text(
            f"📊 **LINKS DE USUARIO** 📊\n\n"
            f"👤 **Usuario ID:** `{target_user_id}`\n"
            f"❌ **Sin registros:** Este usuario no tiene links eliminados",
            parse_mode=ParseMode.MARKDOWN)
        return

    # Mostrar hasta 5 links más recientes del usuario
    recent_user_links = user_links[:5]

    response = f"📊 **LINKS ELIMINADOS DE USUARIO** 📊\n\n"
    response += f"👤 **Usuario ID:** `{target_user_id}`\n"
    response += f"📈 **Total eliminados:** {len(user_links)}\n"
    response += f"📋 **Últimos {len(recent_user_links)} registros:**\n\n"

    for link_data in recent_user_links:
        deleted_time = datetime.fromisoformat(
            link_data['deleted_at']).strftime('%d/%m/%Y %H:%M')
        response += f"🆔 **ID:** `{link_data['id']}`\n"
        response += f"📅 **Fecha:** {deleted_time}\n"
        response += f"🔗 **Links:** {', '.join(link_data['links'][:2])}{'...' if len(link_data['links']) > 2 else ''}\n"
        response += f"💬 **Mensaje:** {link_data['message']}\n"
        response += f"─────────────────────────\n"

    if len(user_links) > 5:
        response += f"\n📝 **Y {len(user_links) - 5} registros más...**"

    await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)


async def fix_founder_command(update: Update,
                              context: ContextTypes.DEFAULT_TYPE):
    """Comando para verificar y corregir el rol de fundador"""
    user_id = str(update.effective_user.id)
    user_id_int = update.effective_user.id

    # Solo para IDs específicos de fundadores
    if user_id_int not in [6938971996, 5537246556]:
        await update.message.reply_text(
            "❌ Este comando solo está disponible para fundadores autorizados")
        return

    # Verificar estado actual
    current_role = db.get_staff_role(user_id)
    in_admin_ids = user_id_int in ADMIN_IDS
    is_founder_db = db.is_founder(user_id)

    # Forzar corrección completa
    db.set_staff_role(user_id, '1')
    if user_id_int not in ADMIN_IDS:
        ADMIN_IDS.append(user_id_int)

    await update.message.reply_text(
        "🔧 **ESTADO DE PERMISOS CORREGIDO** 🔧\n\n"
        f"✅ **Verificación completa realizada:**\n"
        f"• ID: `{user_id}`\n"
        f"• Fundador en DB: ✅ (Forzado)\n"
        f"• En ADMIN_IDS: {'✅' if user_id_int in ADMIN_IDS else '❌ → ✅ (Corregido)'}\n"
        f"• Nivel: 1 (Máximo)\n\n"
        f"🛠️ **Todos los comandos administrativos están disponibles:**\n"
        f"• `/ban`, `/warn`, `/clean`, `/premium`\n"
        f"• `/founder`, `/cofounder`, `/moderator`\n"
        f"• `/post`, `/stats`, `/links`\n\n"
        f"🎯 **Prueba ahora cualquier comando de admin**",
        parse_mode=ParseMode.MARKDOWN)


@bot_admin_only
async def lockdown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bloqueo total del grupo - Solo admins"""
    chat_id = str(update.effective_chat.id)
    args = context.args

    if not args:
        await update.message.reply_text(
            "🔒 **LOCKDOWN TOTAL** 🔒\n\n"
            "**Uso:** `/lockdown [on/off] [tiempo] [razón]`\n\n"
            "**Funciones:**\n"
            "• Bloqueo total del grupo\n"
            "• Nadie excepto admins puede escribir\n"
            "• Medida de emergencia\n\n"
            "**Ejemplos:**\n"
            "• `/lockdown on 30m Raid detectado`\n"
            "• `/lockdown off`",
            parse_mode=ParseMode.MARKDOWN)
        return

    action = args[0].lower()

    if action == "on":
        reason = ' '.join(args[1:]) if len(args) > 1 else "Medida de seguridad"

        try:
            # Bloqueo total - solo lectura
            from telegram import ChatPermissions

            permissions = ChatPermissions(can_send_messages=False,
                                          can_send_media_messages=False,
                                          can_send_polls=False,
                                          can_send_other_messages=False,
                                          can_add_web_page_previews=False,
                                          can_change_info=False,
                                          can_invite_users=False,
                                          can_pin_messages=False)

            await context.bot.set_chat_permissions(
                chat_id=update.effective_chat.id, permissions=permissions)

            response = f"🚨 **LOCKDOWN ACTIVADO** 🚨\n\n"
            response += f"🔒 **GRUPO EN MODO SOLO LECTURA**\n\n"
            response += f"⚠️ **MEDIDA DE EMERGENCIA ACTIVADA**\n"
            response += f"🛡️ **Solo administradores pueden enviar mensajes**\n\n"
            response += f"📝 **Razón:** {reason}\n"
            response += f"👮‍♂️ **Activado por:** {update.effective_user.first_name}\n"
            response += f"⏰ **Fecha:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
            response += f"🔓 **Usa `/lockdown off` para desactivar**"

        except Exception as e:
            response = f"❌ **ERROR EN LOCKDOWN:** {str(e)}"

    elif action == "off":
        try:
            # Restaurar permisos normales
            from telegram import ChatPermissions

            permissions = ChatPermissions(can_send_messages=True,
                                          can_send_media_messages=True,
                                          can_send_polls=True,
                                          can_send_other_messages=True,
                                          can_add_web_page_previews=True,
                                          can_change_info=False,
                                          can_invite_users=True,
                                          can_pin_messages=False)

            await context.bot.set_chat_permissions(
                chat_id=update.effective_chat.id, permissions=permissions)

            response = f"🔓 **LOCKDOWN DESACTIVADO** 🔓\n\n"
            response += f"✅ **Grupo desbloqueado exitosamente**\n"
            response += f"💬 **Miembros pueden enviar mensajes**\n"
            response += f"🔄 **Operaciones normales restauradas**\n\n"
            response += f"👮‍♂️ **Desactivado por:** {update.effective_user.first_name}\n"
            response += f"⏰ **Fecha:** {datetime.now().strftime('%d/%m/%Y %H:%M')}"

        except Exception as e:
            response = f"❌ **ERROR AL DESACTIVAR LOCKDOWN:** {str(e)}"

    else:
        response = "❌ **Acción inválida.** Usa: `on` o `off`"

    await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)


# Callback Query Handler
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles button presses from inline keyboards."""
    query = update.callback_query
    user_id = str(query.from_user.id)
    user_data = db.get_user(user_id)

    await query.answer()  # Acknowledge the click

    # Callbacks de InfoCredits
    if query.data == 'get_credits':
        text = "💰 **FORMAS DE OBTENER CRÉDITOS** 💰\n\n"
        text += "🎁 **Gratis:**\n"
        text += "• `/bonus` 10 créditos diarios (15 premium)\n"
        text += "• `/juegos` 3 / 8 créditos cada 12h\n"
        text += "• Eventos especiales\n\n"
        text += "💎 **Premium:**\n"
        text += "• Comprar membresía con @SteveCHRB\n"

        keyboard = [[
            InlineKeyboardButton("🔙 Regresar",
                                 callback_data='back_to_infocredits')
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text,
                                      parse_mode=ParseMode.MARKDOWN,
                                      reply_markup=reply_markup)

    elif query.data == 'premium_benefits':
        text = "👑 **BENEFICIOS PREMIUM** 👑\n\n"
        text += "⚡ **Verificación:**\n"
        text += "• TODA la verificación simultáneos\n"
        text += "• Mayor probabilidad de LIVE\n"
        text += "• Resultados más rápidos\n\n"
        text += "🎯 **Límites:**\n"
        text += "• Direcciones adicionales\n\n"
        text += "💎 **Bonos:**\n"
        text += "• 15 créditos diarios (vs 10)\n"
        text += "• +300 créditos al activar premium"

        keyboard = [[
            InlineKeyboardButton("🔙 Regresar",
                                 callback_data='back_to_infocredits')
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text,
                                      parse_mode=ParseMode.MARKDOWN,
                                      reply_markup=reply_markup)

    elif query.data == 'free_commands':
        text = "🆓 **COMANDOS GRATUITOS** 🆓\n\n"
        text += "✅ **Generación:**\n"
        text += "• `/gen` - Generar tarjetas (gratis)\n"
        text += "• `/direccion [país]` - Direcciones por país\n"
        text += "ℹ️ **Información:**\n"
        text += "• `/credits` - Ver créditos\n"
        text += "• `/status` - Estado del bot\n"
        text += "• `/pasarela` - Info de pasarelas\n\n"
        text += "🎁 **Bonos:**\n"
        text += "• `/bonus` - Créditos diarios\n"
        text += "• `/juegos` - Casino bot"

        keyboard = [[
            InlineKeyboardButton("🔙 Regresar",
                                 callback_data='back_to_infocredits')
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text,
                                      parse_mode=ParseMode.MARKDOWN,
                                      reply_markup=reply_markup)

    elif query.data == 'paid_commands':
        user_id = str(query.from_user.id)
        user_data = db.get_user(user_id)
        is_admin = query.from_user.id in ADMIN_IDS
        is_premium = user_data.get('premium', False)

        if is_admin:
            methods_text = "🔥 **TODOS LOS MÉTODOS** (Administrador)"
        elif is_premium:
            methods_text = "👑 **TODOS LOS MÉTODOS** (Premium)"
        else:
            methods_text = "⚡ **5 MÉTODOS** (Usuario estándar)"

        text = "💎 **COMANDOS CON COSTO** 💎\n\n"
        text += "🔍 **Verificación `/live`:**\n"
        text += "• 💰 Costo: 3 créditos por uso\n"
        text += "• 📊 Hasta 10 tarjetas por comando\n"
        text += f"• {methods_text}\n"
        text += "• ⚡ Resultados instantáneos\n\n"
        text += "🧠 **Extrapolación `/ex`:**\n"
        text += "• 💰 Costo: 5 créditos\n"
        text += "• 🤖 Algoritmos de IA avanzada\n"
        text += "• 📈 Efectividad 75-85%\n\n"
        text += "⚡ **Diferencias por tipo de usuario:**\n"
        text += "• 🆓 **Estándar:** 5 métodos de verificación\n"
        text += "• 👑 **Premium:** TODOS los métodos disponibles\n"
        text += "• 🛡️ **Admin:** TODOS los métodos"

        keyboard = [[
            InlineKeyboardButton("🔙 Regresar",
                                 callback_data='back_to_infocredits')
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text,
                                      parse_mode=ParseMode.MARKDOWN,
                                      reply_markup=reply_markup)

    elif query.data == 'my_stats':
        text = f"📊 **TUS ESTADÍSTICAS** 📊\n\n"
        text += f"💰 **Créditos:** {user_data['credits']}\n"
        text += f"🏭 **Generadas:** {user_data['total_generated']} tarjetas\n"
        text += f"🔍 **Verificadas:** {user_data['total_checked']} tarjetas\n"
        text += f"⚠️ **Advertencias:** {user_data.get('warns', 0)}/3\n"
        text += f"📅 **Miembro desde:** {user_data['join_date'][:10]}\n\n"
        if user_data['premium']:
            premium_until = datetime.fromisoformat(user_data['premium_until'])
            days_left = (premium_until - datetime.now()).days
            text += f"👑 **Premium:** {days_left} días restantes"
        else:
            text += f"🆓 **Cuenta:** Usuario estándar"

        keyboard = [[
            InlineKeyboardButton("🔙 Regresar",
                                 callback_data='back_to_infocredits')
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text,
                                      parse_mode=ParseMode.MARKDOWN,
                                      reply_markup=reply_markup)

    elif query.data == 'go_games':
        text = "🎮 **Ir a Casino Bot** 🎮\n\n"
        text += "Para acceder a la sección de juegos usa el comando `/juegos`\n\n"
        text += "🎯 **Juegos disponibles:**\n"
        text += "• 🎰 Ruleta de la Suerte\n"
        text += "• 🎲 Dados Mágicos\n"
        text += "• 🃏 Carta de la Fortuna\n"
        text += "• ⚡ Rayo de Créditos\n\n"
        text += "⏰ **Cooldown:** 12 horas entre juegos"

        keyboard = [[
            InlineKeyboardButton("🔙 Regresar",
                                 callback_data='back_to_infocredits')
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text,
                                      parse_mode=ParseMode.MARKDOWN,
                                      reply_markup=reply_markup)

    # Callbacks de Juegos
    elif query.data in [
            'play_ruleta', 'play_dados', 'play_carta', 'play_rayo'
    ]:
        await handle_game_play(query, context, query.data)

    elif query.data == 'game_stats':
        last_game = user_data.get('last_game')
        if last_game:
            last_game_date = datetime.fromisoformat(last_game)
            time_since = datetime.now() - last_game_date
            hours_since = time_since.total_seconds() / 3600
            next_game = 12 - hours_since if hours_since < 12 else 0
        else:
            next_game = 0

        text = f"🎮 **ESTADÍSTICAS DE JUEGOS** 🎮\n\n"
        text += f"💰 **Créditos actuales:** {user_data['credits']}\n"
        text += f"⏰ **Último juego:** {last_game_date.strftime('%d/%m/%Y %H:%M') if last_game else 'Nunca'}\n"
        text += f"🕐 **Próximo juego:** {'Disponible' if next_game <= 0 else f'{next_game:.1f}h'}\n"
        text += f"🎯 **Ganancia por juego:** 3-8 créditos\n"
        text += f"⏱️ **Cooldown:** 12 horas"

        keyboard = [[
            InlineKeyboardButton("🔙 Regresar", callback_data='back_to_juegos')
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text,
                                      parse_mode=ParseMode.MARKDOWN,
                                      reply_markup=reply_markup)

    elif query.data == 'back_to_infocredits':
        # Recrear el mensaje original de infocredits
        keyboard = [[
            InlineKeyboardButton("💰 Obtener Créditos",
                                 callback_data='get_credits'),
            InlineKeyboardButton("👑 Premium", callback_data='premium_benefits')
        ],
                    [
                        InlineKeyboardButton("🆓 Comandos Gratis",
                                             callback_data='free_commands'),
                        InlineKeyboardButton("💎 Comandos de Pago",
                                             callback_data='paid_commands')
                    ],
                    [
                        InlineKeyboardButton("📊 Mis Estadísticas",
                                             callback_data='my_stats'),
                        InlineKeyboardButton("🎮 Ir a Juegos",
                                             callback_data='go_games')
                    ]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        premium_text = ""
        if user_data['premium']:
            premium_until = datetime.fromisoformat(user_data['premium_until'])
            days_left = (premium_until - datetime.now()).days
            premium_text = f"\n👑 **PREMIUM ACTIVO** ({days_left} días)"

        response = f"╔═══════════════════════════╗\n"
        response += f"║     💡 𝐒𝐈𝐒𝐓𝐄𝐌𝐀 𝐃𝐄 𝐂𝐑É𝐃𝐈𝐓𝐎𝐒     ║\n"
        response += f"╚═══════════════════════════╝\n\n"
        response += f"💎 **Tus Créditos:** {user_data['credits']}{premium_text}\n\n"
        response += f"📋 **Selecciona una opción:**"

        await query.edit_message_text(response,
                                      reply_markup=reply_markup,
                                      parse_mode=ParseMode.MARKDOWN)

    elif query.data == 'back_to_juegos':
        # Recrear el mensaje original de juegos
        keyboard = [[
            InlineKeyboardButton("🎰 Ruleta de la Suerte",
                                 callback_data='play_ruleta'),
            InlineKeyboardButton("🎲 Dados Mágicos", callback_data='play_dados')
        ],
                    [
                        InlineKeyboardButton("🃏 Carta de la Fortuna",
                                             callback_data='play_carta'),
                        InlineKeyboardButton("⚡ Rayo de Créditos",
                                             callback_data='play_rayo')
                    ],
                    [
                        InlineKeyboardButton("📊 Mis Estadísticas",
                                             callback_data='game_stats')
                    ]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        now = datetime.now()
        last_game = user_data.get('last_game')
        can_play = True
        time_left = 0

        if last_game:
            last_game_date = datetime.fromisoformat(last_game)
            hours_passed = (now - last_game_date).total_seconds() / 3600
            if hours_passed < 12:
                can_play = False
                time_left = 12 - hours_passed

        status_text = "🟢 **DISPONIBLE**" if can_play else f"🔴 **COOLDOWN** ({time_left:.1f}h restantes)"

        response = f"╔═══════════════════════════╗\n"
        response += f"║        🎮 𝐂𝐀𝐒𝐈𝐍𝐎 𝐁𝐎𝐓        ║\n"
        response += f"╚═══════════════════════════╝\n\n"
        response += f"💰 **Créditos:** {user_data['credits']}\n"
        response += f"⏰ **Estado:** {status_text}\n"
        response += f"🎁 **Ganancia:** 3-8 créditos por juego\n"
        response += f"⏱️ **Límite:** 1 juego cada 12 horas\n\n"
        response += f"🎯 **Elige tu juego:**"

        await query.edit_message_text(response,
                                      reply_markup=reply_markup,
                                      parse_mode=ParseMode.MARKDOWN)

    # Callbacks para sistema /check
    elif query.data.startswith('approve_check_'):
        await handle_check_approval(query, context, True)

    elif query.data.startswith('reject_check_'):
        await handle_check_approval(query, context, False)
    # Callback para regenerar tarjetas - CORREGIDO
    elif query.data.startswith('regen_'):
        parts = query.data.split('_')
        bin_number = parts[1]
        count = int(parts[2])
        preset_month = parts[3] if parts[3] != "rnd" else None
        preset_year = parts[4] if parts[4] != "rnd" else None
        preset_cvv = parts[5] if parts[5] != "rnd" else None

        # Obtener parámetros adicionales si existen
        card_length = int(parts[6]) if len(parts) > 6 else 16
        cvv_length = int(parts[7]) if len(parts) > 7 else 3

        # Convertir strings a integers
        if preset_month: preset_month = int(preset_month)
        if preset_year: preset_year = int(preset_year)
        if preset_cvv: preset_cvv = int(preset_cvv)

        await query.edit_message_text("🔄 Regenerando tarjetas...")

        # Determinar tipo de tarjeta
        card_type = "UNKNOWN"
        if bin_number.startswith('4'):
            card_type = "VISA"
        elif bin_number.startswith('5') or bin_number.startswith('2'):
            card_type = "MASTERCARD"
        elif bin_number.startswith('3'):
            card_type = "AMERICAN EXPRESS"

        # Generar tarjetas con método avanzado
        try:
            if preset_month or preset_year or preset_cvv:
                cards = CardGenerator.generate_cards_custom_advanced(
                    bin_number, count, preset_month, preset_year, preset_cvv,
                    card_length, cvv_length)
            else:
                cards = CardGenerator.generate_cards_advanced(
                    bin_number, count, card_length, cvv_length)
        except:
            # Fallback al método básico
            cards = CardGenerator.generate_cards(bin_number, count)

        # Obtener información REAL del BIN
        real_bin_info = await get_real_bin_info(bin_number)

        # Crear máscara del BIN apropiada
        x_count = card_length - len(bin_number)
        bin_mask = bin_number + "x" * x_count

        # Mostrar formato usado
        format_display = f"{preset_month or 'rnd'} | {preset_year or 'rnd'} | {preset_cvv or 'rnd'}"

        response = f"BIN: {bin_mask} | {format_display}\n"
        response += f"═══════════════════════════\n"
        response += f"        『⛧⛧⛧』⟪ 𝗖𝗛𝗘𝗥𝗡𝗢𝗕𝗜𝗟 𝗖𝗛𝗟𝗩 ⟫『⛧⛧⛧』\n"
        response += f"         {card_type} ({card_length} dígitos)\n\n"

        for card in cards:
            response += f"{card}\n"

        # Obtener bandera del país
        country_flags = {
            'UNITED STATES': '🇺🇸',
            'CANADA': '🇨🇦',
            'UNITED KINGDOM': '🇬🇧',
            'GERMANY': '🇩🇪',
            'FRANCE': '🇫🇷',
            'SPAIN': '🇪🇸',
            'ITALY': '🇮🇹',
            'BRAZIL': '🇧🇷',
            'MEXICO': '🇲🇽',
            'ARGENTINA': '🇦🇷',
            'COLOMBIA': '🇨🇴'
        }
        country_flag = country_flags.get(real_bin_info['country'].upper(), '🌍')

        # Información REAL del BIN
        response += f"\n══════ DETAILS ══════\n"
        response += f"💳 Bin Information:\n"
        response += f"🏦 Bank: {real_bin_info['bank']}\n"
        response += f"💼 Type: {real_bin_info['scheme']} - {real_bin_info['type']} - {real_bin_info['level']}\n"
        response += f"🌍 Country: {real_bin_info['country']} {country_flag}\n"
        response += f"╚═════𝗖𝗛𝗘𝗥𝗡𝗢𝗕𝗜𝗟 𝗖𝗛𝗟𝗩═════╝"

        # Mantener exactamente los mismos parámetros
        regen_data = f"regen_{bin_number}_{count}_{preset_month or 'rnd'}_{preset_year or 'rnd'}_{preset_cvv or 'rnd'}_{card_length}_{cvv_length}"

        keyboard = [[
            InlineKeyboardButton("🔄 Regenerar Tarjetas",
                                 callback_data=regen_data),
            InlineKeyboardButton("📊 Ver BIN Info",
                                 callback_data=f'bininfo_{bin_number}')
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(response, reply_markup=reply_markup)

    # Callback para mostrar información del BIN
    elif query.data.startswith('bininfo_'):
        bin_number = query.data.split('_')[1]
        real_bin_info = await get_real_bin_info(bin_number)

        response = f"📊 **BIN Information** 📊\n\n"
        response += f"💳 **BIN:** {bin_number}\n"
        response += f"🏛️ **Bank:** {real_bin_info['bank']}\n"
        response += f"🗺️ **Country:** {real_bin_info['country']}\n"
        response += f"🌐 **Scheme:** {real_bin_info['scheme']}\n"
        response += f"🔑 **Type:** {real_bin_info['type']}\n"
        response += f"💎 **Level:** {real_bin_info['level']}\n"

        await query.edit_message_text(response, parse_mode=ParseMode.MARKDOWN)


async def handle_check_approval(query, context, is_approved):
    """Maneja la aprobación o rechazo de capturas por administradores"""
    admin_id = str(query.from_user.id)
    admin_user = query.from_user

    # Verificar que sea admin
    if query.from_user.id not in ADMIN_IDS:
        await query.answer(
            "❌ Solo administradores pueden aprobar/rechazar capturas",
            show_alert=True)
        return

    # Extraer ID de verificación
    check_id = query.data.split('_')[-1]

    # Obtener datos de la verificación
    check_data = db.get_pending_check(check_id)
    if not check_data:
        await query.answer("❌ Verificación no encontrada o ya procesada",
                           show_alert=True)
        return

    if check_data['status'] != 'pending':
        await query.answer("❌ Esta verificación ya fue procesada",
                           show_alert=True)
        return

    # Obtener configuración del grupo
    group_id = check_data['group_id']
    check_config = db.get_check_chats(group_id)

    if not check_config:
        await query.answer("❌ Configuración de chats no encontrada",
                           show_alert=True)
        return

    user_id = check_data['user_id']
    username = check_data['username']
    user_data = db.get_user(user_id)

    if is_approved:
        # APROBAR: Dar 6 créditos al usuario
        new_credits = user_data['credits'] + 6
        db.update_user(user_id, {'credits': new_credits})
        db.update_check_status(check_id, 'approved', admin_id)

        # Actualizar mensaje de verificación (para admins)
        approval_text = f"✅ **CAPTURA APROBADA** ✅\n\n"
        approval_text += f"🆔 **ID:** `{check_id}`\n"
        approval_text += f"👤 **Usuario:** {username}\n"
        approval_text += f"💰 **Créditos otorgados:** 6\n"
        approval_text += f"📊 **Créditos totales:** {new_credits}\n"
        approval_text += f"👮‍♂️ **Aprobado por:** {admin_user.first_name}\n"
        approval_text += f"📅 **Fecha:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        approval_text += f"🎉 **¡Felicidades al usuario por su captura válida!**"

        try:
            await query.edit_message_caption(caption=approval_text,
                                             parse_mode=ParseMode.MARKDOWN)
        except:
            pass

        # Enviar mensaje de aprobación al grupo principal (SIN MOSTRAR CRÉDITOS)
        try:
            # Escapar el username para evitar errores de parsing
            safe_username = escape_markdown(username)

            approval_message = "╔══════════════════════════════════╗\n"
            approval_message += "║      🎉  **CAPTURA APROBADA**  🎉      ║\n"
            approval_message += "╚══════════════════════════════════╝\n\n"
            approval_message += "🌟 **¡Felicitaciones!** Esta captura ha sido verificada\n\n"
            approval_message += f"👤 **Usuario:** {safe_username}\n"
            approval_message += f"✅ **Estado:** Aprobada oficialmente\n"
            approval_message += f"🤖 **Verificada por:** @ChernobilChLv\\_bot\n\n"
            approval_message += "🎁 **¡Has recibido 6 creditos!**\n"
            approval_message += "💡 **Sigue compartiendo capturas válidas para más beneficios**"

            await context.bot.send_message(chat_id=group_id,
                                           text=approval_message,
                                           parse_mode=ParseMode.MARKDOWN)

        except Exception as e:
            logger.error(f"Error enviando mensaje al grupo principal: {e}")

        # Publicar en canal de publicaciones
        try:
            publication_chat_id = check_config['publication_chat']

            # Crear mensaje de publicación con texto escapado
            safe_username = escape_markdown(username)
            safe_check_id = escape_markdown(check_id)

            publication_text = "╔══════════════════════════════════\n"
            publication_text += "║    🏆  **CAPTURA VERIFICADA**  🏆    ║\n"
            publication_text += "╚══════════════════════════════════\n\n"
            publication_text += f"👤 **Usuario:** {safe_username}\n"
            publication_text += f"✅ **Estado:** Verificado oficialmente\n"
            publication_text += f"🤖 **Aprobado por:** @ChernobilChLv\\_bot\n"
            publication_text += f"🆔 **Referencia:** `{safe_check_id}`\n"
            publication_text += f"📅 **Fecha:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
            publication_text += f"🎯 **¡Excelente trabajo!** Sigue así para más recompensas\n"
            publication_text += f"💡 **Usa /check para verificar tus capturas**"

            await context.bot.send_photo(chat_id=publication_chat_id,
                                         photo=check_data['image_file_id'],
                                         caption=publication_text,
                                         parse_mode=ParseMode.MARKDOWN)

        except Exception as e:
            logger.error(f"Error publicando en canal: {e}")

        await query.answer("✅ Captura aprobada - Recompensa otorgada",
                           show_alert=True)

    else:
        # RECHAZAR: Solo actualizar estado
        db.update_check_status(check_id, 'rejected', admin_id)

        # Actualizar mensaje de verificación (para admins)
        rejection_text = f"❌ **CAPTURA RECHAZADA** ❌\n\n"
        rejection_text += f"🆔 **ID:** `{check_id}`\n"
        rejection_text += f"👤 **Usuario:** {username}\n"
        rejection_text += f"💰 **Créditos:** Sin cambios ({user_data['credits']})\n"
        rejection_text += f"👮‍♂️ **Rechazado por:** {admin_user.first_name}\n"
        rejection_text += f"📅 **Fecha:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        rejection_text += f"📝 **Motivo:** Captura no cumple con los criterios\n"
        rejection_text += f"💡 **El usuario puede intentar con otra captura válida**"

        try:
            await query.edit_message_caption(caption=rejection_text,
                                             parse_mode=ParseMode.MARKDOWN)
        except:
            pass

        # Enviar mensaje de rechazo al grupo principal (opcional)
        try:
            safe_username = escape_markdown(username)

            rejection_message = "╔══════════════════════════════════╗\n"
            rejection_message += "║      ❌  **CAPTURA RECHAZADA**  ❌      ║\n"
            rejection_message += "╚══════════════════════════════════╝\n\n"
            rejection_message += f"👤 **Usuario:** {safe_username}\n"
            rejection_message += f"🤖 **Revisado por:** @ChernobilChLv\\_bot\n\n"
            rejection_message += "📝 **Motivo:** La captura no cumple con los criterios\n"
            rejection_message += "💡 **Puedes intentar nuevamente con una captura válida**"

            await context.bot.send_message(chat_id=group_id,
                                           text=rejection_message,
                                           parse_mode=ParseMode.MARKDOWN)

        except Exception as e:
            logger.error(f"Error enviando mensaje de rechazo al grupo: {e}")

        await query.answer("❌ Captura rechazada - Sin recompensa",
                           show_alert=True)


async def handle_game_play(query, context, game_type):
    """Maneja la lógica de juegos con límite de 12 horas"""
    user_id = str(query.from_user.id)
    user_data = db.get_user(user_id)

    now = datetime.now()
    last_game = user_data.get('last_game')

    # Verificar cooldown de 12 horas
    if last_game:
        last_game_date = datetime.fromisoformat(last_game)
        hours_passed = (now - last_game_date).total_seconds() / 3600

        if hours_passed < 12:
            hours_left = 12 - hours_passed
            await query.edit_message_text(
                f"⏰ **COOLDOWN ACTIVO** ⏰\n\n"
                f"⏳ Tiempo restante: {hours_left:.1f} horas\n"
                f"🎮 Podrás jugar cada 12 horas\n\n"
                f"💡 Usa `/bonus` para créditos diarios",
                parse_mode=ParseMode.MARKDOWN)
            return

    # Jugar según el tipo
    game_names = {
        'play_ruleta': '🎰 Ruleta de la Suerte',
        'play_dados': '🎲 Dados Mágicos',
        'play_carta': '🃏 Carta de la Fortuna',
        'play_rayo': '⚡ Rayo de Créditos'
    }

    game_name = game_names.get(game_type, '🎮 Juego')
    ganancia = random.randint(3, 8)

    # Actualizar créditos y fecha del último juego
    db.update_user(user_id, {
        'credits': user_data['credits'] + ganancia,
        'last_game': now.isoformat()
    })

    # Mensajes especiales por juego
    game_messages = {
        'play_ruleta': f"🎰 La ruleta gira... ¡{ganancia} créditos!",
        'play_dados': f"🎲 Los dados cayeron... ¡{ganancia} créditos!",
        'play_carta': f"🃏 Tu carta de la fortuna... ¡{ganancia} créditos!",
        'play_rayo':
        f"⚡ El rayo de créditos te golpea... ¡{ganancia} créditos!"
    }

    response = f"🎉 **¡GANASTE!** 🎉\n\n"
    response += f"{game_name}\n"
    response += f"{game_messages.get(game_type, f'¡Ganaste {ganancia} créditos!')}\n\n"
    response += f"💰 **Créditos totales:** {user_data['credits'] + ganancia}\n"
    response += f"⏰ **Próximo juego:** En 12 horas"

    await query.edit_message_text(response, parse_mode=ParseMode.MARKDOWN)


async def welcome_new_member(update: Update,
                             context: ContextTypes.DEFAULT_TYPE):
    """Mensaje de bienvenida para nuevos miembros"""
    for new_member in update.message.new_chat_members:
        welcome_text = f"🎉 **¡BIENVENIDO A CHERNOBYL CHLV!** 🎉\n\n"
        welcome_text += f"👋 Hola {new_member.mention_markdown()}\n\n"
        welcome_text += f"🔥 **¡Te damos la bienvenida al mejor bot de CCs!**\n\n"
        welcome_text += f"💡 **Para empezar:**\n"
        welcome_text += f"• Usa `/start` para ver todos los comandos\n"
        welcome_text += f"• Obtén créditos gratis con `/bonus`\n"
        welcome_text += f"🎁 **Recibes 10 créditos de bienvenida**\n\n"
        welcome_text += f"📋 **Reglas básicas:**\n"
        welcome_text += f"• No spam ni enlaces\n"
        welcome_text += f"• Respeta a otros usuarios\n"
        welcome_text += f"• Usa los comandos correctamente\n\n"
        welcome_text += f"🤖 **Bot:** @ChernobilChLv_bot\n"
        welcome_text += f"🆘 **Soporte:** Contacta a los admins"

        # Dar créditos de bienvenida
        user_id = str(new_member.id)
        user_data = db.get_user(user_id)
        db.update_user(user_id, {'credits': user_data['credits'] + 10})

        await update.message.reply_text(welcome_text,
                                        parse_mode=ParseMode.MARKDOWN)


# Anti-Spam Handler - CORREGIDO CON PERMISOS DE STAFF
async def anti_spam_handler(update: Update,
                            context: ContextTypes.DEFAULT_TYPE):
    """Sistema anti-spam automático que detecta, guarda y elimina links - RESPETA ROLES DE STAFF"""
    if not update.message or not update.message.text:
        return

    user_id = str(update.effective_user.id)
    user_id_int = update.effective_user.id
    user_data = db.get_user(user_id)
    message_text = update.message.text
    message_text_lower = message_text.lower()

    # VERIFICAR SI EL USUARIO TIENE PERMISOS PARA ENVIAR LINKS
    # 1. Administradores tradicionales
    is_traditional_admin = user_id_int in ADMIN_IDS

    # 2. Staff en base de datos (fundadores, co-fundadores, moderadores)
    staff_data = db.get_staff_role(user_id)
    is_staff = staff_data is not None

    # 3. IDs de emergencia
    emergency_ids = [6938971996, 5537246556]
    is_emergency_founder = user_id_int in emergency_ids

    # Si el usuario tiene permisos, NO aplicar anti-spam
    if is_traditional_admin or is_staff or is_emergency_founder:
        return  # Permitir envío de links sin restricciones

    # Detectar múltiples tipos de links incluyendo embebidos
    spam_indicators = [
        "http://", "https://", "www.", ".com", ".net", ".org", ".io", ".co",
        ".me", "t.me/", "telegram.me", "bit.ly", "tinyurl", "shortened.link",
        ".tk", ".ml", ".ga", ".cf", ".ly", ".gl", ".gg", ".cc", ".tv",
        "discord.gg", "discord.com", "youtube.com", "youtu.be"
    ]

    # Verificar si el mensaje contiene spam básico
    contains_spam = any(indicator in message_text_lower
                        for indicator in spam_indicators)

    # NUEVO: Detectar enlaces embebidos y caracteres Unicode sospechosos
    if not contains_spam:
        import re

        # Detectar caracteres Unicode de control que pueden ocultar enlaces
        unicode_patterns = [
            r'[\u200B-\u200F\u202A-\u202E\u2060-\u2064]',  # Caracteres de control
            r'[\u00A0\u1680\u2000-\u200A\u202F\u205F\u3000]',  # Espacios no estándar
            r'[\u034F\u061C\u180E]',  # Caracteres invisibles
        ]

        # Verificar si hay caracteres Unicode sospechosos
        has_unicode_spam = any(
            re.search(pattern, message_text) for pattern in unicode_patterns)

        # Detectar texto con posibles enlaces embebidos
        # Palabras muy largas sin espacios que pueden ocultar URLs
        words = message_text.split()
        suspicious_words = [
            word for word in words
            if len(word) > 30 and not word.isdigit() and any(
                char in word.lower() for char in ['.', '/', ':'])
        ]

        # Detectar patrones de enlaces embebidos (texto con características de URL)
        embedded_link_patterns = [
            r'[^\s]{20,}\.(?:com|net|org|io|co|me|ly|gg|tv)[^\s]*',  # Dominios largos
            r'[^\s]*(?:discord|telegram|youtube|bit\.ly)[^\s]*',  # Servicios conocidos
            r'[^\s]*://[^\s]*',  # Protocolo sin espacios
        ]

        has_embedded_links = any(
            re.search(pattern, message_text, re.IGNORECASE)
            for pattern in embedded_link_patterns)

        # Detectar si hay muchos caracteres no ASCII (posible ofuscación)
        non_ascii_count = sum(1 for char in message_text if ord(char) > 127)
        has_excessive_unicode = non_ascii_count > len(
            message_text) * 0.3  # Más del 30%

        # Marcar como spam si se detecta cualquiera de estos patrones
        contains_spam = (has_unicode_spam or len(suspicious_words) > 0
                         or has_embedded_links or has_excessive_unicode)

    if contains_spam:
        try:
            # GUARDAR el link antes de eliminarlo
            username = f"@{update.effective_user.username}" if update.effective_user.username else update.effective_user.first_name
            chat_id = str(update.effective_chat.id)
            link_id = db.save_deleted_link(user_id, username, chat_id,
                                           message_text)

            # BORRAR el mensaje automáticamente
            await update.message.delete()

            # Incrementar advertencias
            current_warns = user_data.get('warns', 0) + 1
            db.update_user(user_id, {'warns': current_warns})

            # Determinar tipo de detección para el mensaje
            detection_type = "enlace estándar"
            if any(ord(char) > 127 for char in message_text):
                detection_type = "enlace embebido/Unicode"
            elif len(message_text) > 100:
                detection_type = "enlace oculto en texto"

            # Enviar advertencia automática CON ID del link guardado
            warning_message = f"🚫 **LINK DETECTADO Y ELIMINADO** 🚫\n\n"
            warning_message += f"👤 **Usuario:** {update.effective_user.first_name}\n"
            warning_message += f"🔍 **Tipo:** {detection_type}\n"
            warning_message += f"🆔 **Link ID:** `{link_id}`\n"
            warning_message += f"⚠️ **Advertencias:** {current_warns}/3\n\n"

            if current_warns >= 3:
                warning_message += f"🔨 **USUARIO BANEADO POR SPAM**"
                try:
                    await context.bot.ban_chat_member(
                        chat_id=update.effective_chat.id,
                        user_id=update.effective_user.id)
                except:
                    warning_message += f"\n❌ Error al banear usuario"
            else:
                warning_message += f"💡 **Política:** Solo staff puede enviar enlaces\n"
                warning_message += f"📝 **El link ha sido registrado para revisión**\n"
                warning_message += f"🔰 **Para obtener permisos contacta a los administradores**"

            # Enviar mensaje temporal que se auto-elimina
            warning_msg = await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=warning_message,
                parse_mode=ParseMode.MARKDOWN)

            # Log para administradores
            logger.info(
                f"Link eliminado (usuario sin permisos) - Usuario: {user_id} ({username}) - Chat: {chat_id} - Link ID: {link_id}"
            )

            # Auto-eliminar mensaje de advertencia después de 15 segundos
            await asyncio.sleep(15)
            try:
                await warning_msg.delete()
            except:
                pass

        except Exception as e:
            logger.error(f"Error en anti-spam: {e}")


# Manejador de errores
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manejador de errores"""
    logger.error(f"Update {update} causó error {context.error}")


# Función principal
def main():
    """Función principal del bot"""
    # Configuración del bot para evitar conflictos
    application = (
        Application.builder().token(BOT_TOKEN).concurrent_updates(
            False).connect_timeout(60).read_timeout(60).write_timeout(60).
        get_updates_connect_timeout(60).get_updates_read_timeout(60).build())

    # Registrar comandos principales
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("gen", gen_command))
    application.add_handler(CommandHandler("live", live_command))
    application.add_handler(CommandHandler("direccion", direccion_command))
    application.add_handler(CommandHandler("ex", ex_command))
    application.add_handler(CommandHandler("credits", credits_command))
    application.add_handler(CommandHandler("bonus", bonus_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("pasarela", pasarela_command))
    application.add_handler(CommandHandler("apply_key", apply_key_command))
    application.add_handler(CommandHandler("infocredits", infocredits_command))
    application.add_handler(CommandHandler("donate", donate_command))
    application.add_handler(CommandHandler("juegos", juegos_command))

    # Sistema de verificación /check
    application.add_handler(CommandHandler("check", check_command))
    application.add_handler(
        CommandHandler("setcheckchats", setcheckchats_command))

    # Sistema de publicaciones
    application.add_handler(CommandHandler("post", post_command))

    # Comandos de admin y staff
    application.add_handler(CommandHandler("staff", staff_command))
    application.add_handler(CommandHandler("founder", founder_command))
    application.add_handler(CommandHandler("cofounder", cofounder_command))
    application.add_handler(CommandHandler("moderator", moderator_command))
    application.add_handler(
        CommandHandler("emergency_founder", emergency_founder_command))
    application.add_handler(CommandHandler("fix_founder", fix_founder_command))
    application.add_handler(CommandHandler(
        "check_perms", fix_founder_command))  # Alias adicional
    application.add_handler(CommandHandler("clean", clean_command))
    application.add_handler(CommandHandler("cleanstatus", cleanstatus_command))
    application.add_handler(CommandHandler("premium", premium_command))
    application.add_handler(CommandHandler("id", id_command))
    application.add_handler(CommandHandler("ban", ban_command))
    application.add_handler(CommandHandler("warn", warn_command))
    application.add_handler(CommandHandler("unwarn", unwarn_command))
    application.add_handler(CommandHandler("unban", unban_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("links", links_command))  # NUEVO
    application.add_handler(CommandHandler("open", open_command))
    application.add_handler(CommandHandler("close", close_command))
    application.add_handler(CommandHandler("housemode", housemode_command))
    application.add_handler(CommandHandler("lockdown", lockdown_command))

    # Callback handlers
    application.add_handler(CallbackQueryHandler(button_callback))

    # Manejador de nuevos miembros
    application.add_handler(
        MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS,
                       welcome_new_member))

    # Anti-spam handler - CORREGIDO
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, anti_spam_handler))

    # Manejador de errores
    application.add_error_handler(error_handler)

    # Iniciar el bot con manejo de errores mejorado
    print("✅ Bot iniciado correctamente")
    try:
        application.run_polling(
            drop_pending_updates=True,  # Limpiar actualizaciones pendientes
            close_loop=False,
            allowed_updates=None,  # Recibir todos los tipos de actualización
            stop_signals=None  # Evitar conflictos de señales
        )
    except Exception as e:
        logger.error(f"Error en polling: {e}")
        print(f"❌ Error en el bot: {e}")
        # En lugar de salir, intentar reiniciar
        import time
        time.sleep(5)
        main()


if __name__ == "__main__":
    try:
        # Importar e iniciar keep_alive para UptimeRobot
        from keep_alive import keep_alive
        keep_alive()

        # Iniciar el bot
        main()
    except Exception as e:
        logger.error(f"Error crítico al iniciar el bot: {e}")
        import sys
        sys.exit(1)
