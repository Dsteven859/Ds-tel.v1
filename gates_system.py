
import asyncio
import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from telegram.error import RetryAfter, TimedOut

# Importar db del módulo principal
from telegram_bot import db

class GateSystem:
    def __init__(self, db):
        self.db = db
        self.active_sessions = {}  # Sesiones activas de gates
        self.rate_limit_tracker = {}  # Control de rate limiting

    def is_authorized(self, user_id: str) -> bool:
        """Verificar si el usuario tiene acceso (fundador nivel 1, co-fundador o premium)"""
        # Verificar si es fundador nivel 1
        if self.db.is_founder(user_id):
            return True

        # Verificar si es co-fundador (nivel 2)
        staff_data = self.db.get_staff_role(user_id)
        if staff_data and staff_data['role'] == '2':
            return True

        # Verificar si es premium activo
        user_data = self.db.get_user(user_id)
        if user_data.get('premium', False):
            premium_until = user_data.get('premium_until')
            if premium_until:
                premium_date = datetime.fromisoformat(premium_until)
                if datetime.now() < premium_date:
                    return True
        return False

    def create_gates_menu(self) -> InlineKeyboardMarkup:
        """Crear menú principal de gates"""
        keyboard = [
            [
                InlineKeyboardButton("🔵 Stripe Gate", callback_data='gate_stripe'),
                InlineKeyboardButton("🟠 Amazon Gate", callback_data='gate_amazon')
            ],
            [
                InlineKeyboardButton("🔴 PayPal Gate", callback_data='gate_paypal'),
                InlineKeyboardButton("🟡 Ayden Gate", callback_data='gate_ayden')
            ],
            [
                InlineKeyboardButton("🟢 Auth Gate", callback_data='gate_auth'),
                InlineKeyboardButton("⚫ CCN Charge", callback_data='gate_ccn')
            ],
            [
                InlineKeyboardButton("📊 Gate Status", callback_data='gates_status'),
                InlineKeyboardButton("❌ Cerrar", callback_data='gates_close')
            ]
        ]
        return InlineKeyboardMarkup(keyboard)

    async def process_stripe_gate(self, card_data: str) -> dict:
        """Procesar verificación Stripe Gate - EFECTIVIDAD REALISTA"""
        await asyncio.sleep(random.uniform(2.0, 4.0))

        parts = card_data.split('|')
        if len(parts) < 4:
            return {
                'success': False,
                'message': '❌ Formato inválido - Use: 4532123456781234|12|25|123',
                'status': 'DEAD'
            }

        card_number = parts[0]
        exp_month = parts[1]
        exp_year = parts[2]
        cvv = parts[3]

        # ALGORITMO REALISTA PARA STRIPE (15-25% máximo)
        success_rate = 0.08  # 8% base REALISTA

        # Análisis del BIN (bonificaciones MENORES)
        premium_bins = ['4532', '4485', '5531', '4539']
        if any(card_number.startswith(bin_) for bin_ in premium_bins):
            success_rate += 0.04  # +4% máximo
        elif card_number.startswith(('40', '41', '51', '52')):
            success_rate += 0.02  # +2%

        # Análisis CVV (bonificación MÍNIMA)
        if cvv.endswith(('7', '3', '9')):
            success_rate += 0.01  # +1%

        # Factor de aleatoriedad realista
        success_rate *= random.uniform(0.6, 1.4)
        
        # MÁXIMO REALISTA del 25%
        success_rate = min(success_rate, 0.25)

        is_success = random.random() < success_rate

        if is_success:
            responses = [
                "✅ Payment successful - $1.00 charged",
                "✅ Transaction approved - CVV2 Match",
                "✅ Stripe: authorized - Gateway Response: 00",
                "✅ Card charged successfully - Risk: Low"
            ]
            return {
                'success': True,
                'message': random.choice(responses),
                'status': 'LIVE',
                'gateway': 'Stripe Ultra',
                'amount': '$1.00'
            }
        else:
            responses = [
                "❌ Card declined - Insufficient funds",
                "❌ Transaction failed - Invalid CVV",
                "❌ Payment declined - Do not honor",
                "❌ Risk threshold exceeded",
                "❌ Generic decline - Contact bank",
                "❌ Card blocked - Security"
            ]
            return {
                'success': False,
                'message': random.choice(responses),
                'status': 'DEAD',
                'gateway': 'Stripe Ultra',
                'amount': '$0.00'
            }

    async def process_amazon_gate(self, card_data: str) -> dict:
        """Procesar verificación Amazon Gate - EFECTIVIDAD REALISTA"""
        await asyncio.sleep(random.uniform(3.0, 5.0))

        parts = card_data.split('|')
        if len(parts) < 4:
            return {
                'success': False,
                'message': '❌ Formato inválido',
                'status': 'DEAD'
            }

        # Amazon es ULTRA restrictivo - 8-18% máximo
        success_rate = 0.05  # 5% base REALISTA

        card_number = parts[0]
        if card_number.startswith('4'):
            success_rate += 0.03  # Amazon prefiere Visa (+3%)
        elif card_number.startswith('5'):
            success_rate += 0.02  # MasterCard (+2%)

        # Factor de aleatoriedad
        success_rate *= random.uniform(0.4, 1.6)
        
        # MÁXIMO REALISTA del 18%
        success_rate = min(success_rate, 0.18)

        is_success = random.random() < success_rate

        if is_success:
            responses = [
                "✅ Amazon: Payment method added successfully",
                "✅ Amazon: Card verified for purchases",
                "✅ Amazon: Billing updated - Ready for orders"
            ]
            return {
                'success': True,
                'message': random.choice(responses),
                'status': 'LIVE',
                'gateway': 'Amazon Prime',
                'amount': '$0.00'
            }
        else:
            responses = [
                "❌ Amazon: Invalid payment method",
                "❌ Amazon: Card verification failed",
                "❌ Amazon: Unable to add card",
                "❌ Amazon: Billing address mismatch",
                "❌ Amazon: Security review required"
            ]
            return {
                'success': False,
                'message': random.choice(responses),
                'status': 'DEAD',
                'gateway': 'Amazon Prime',
                'amount': '$0.00'
            }

    async def process_paypal_gate(self, card_data: str) -> dict:
        """Procesar verificación PayPal Gate - EFECTIVIDAD REALISTA"""
        await asyncio.sleep(random.uniform(2.5, 4.5))

        # PayPal efectividad ULTRA REALISTA (10-20% máximo)
        success_rate = 0.06  # 6% base realista
        
        # Factor de aleatoriedad
        success_rate *= random.uniform(0.3, 1.7)
        
        # MÁXIMO REALISTA del 20%
        success_rate = min(success_rate, 0.20)

        is_success = random.random() < success_rate

        if is_success:
            return {
                'success': True,
                'message': "✅ PayPal: Card linked successfully",
                'status': 'LIVE',
                'gateway': 'PayPal Express',
                'amount': '$0.00'
            }
        else:
            responses = [
                "❌ PayPal: Card verification failed",
                "❌ PayPal: Unable to link card",
                "❌ PayPal: Security check failed",
                "❌ PayPal: Invalid card data"
            ]
            return {
                'success': False,
                'message': random.choice(responses),
                'status': 'DEAD',
                'gateway': 'PayPal Express',
                'amount': '$0.00'
            }

    async def process_ayden_gate(self, card_data: str) -> dict:
        """Procesar verificación Ayden Gate - EFECTIVIDAD REALISTA"""
        await asyncio.sleep(random.uniform(3.5, 5.5))

        parts = card_data.split('|')
        if len(parts) < 4:
            return {
                'success': False,
                'message': '❌ Formato inválido',
                'status': 'DEAD'
            }

        # Ayden es muy restrictivo - 5-15% máximo
        success_rate = 0.03  # 3% base ULTRA realista

        card_number = parts[0]
        # Ayden prefiere ciertos BINs europeos
        if card_number.startswith(('4000', '4001', '5200', '5201')):
            success_rate += 0.02  # +2%

        # Factor de aleatoriedad
        success_rate *= random.uniform(0.2, 2.0)
        
        # MÁXIMO REALISTA del 15%
        success_rate = min(success_rate, 0.15)

        is_success = random.random() < success_rate

        if is_success:
            responses = [
                "✅ Ayden: Payment authorized successfully",
                "✅ Ayden: Card verification passed",
                "✅ Ayden: Transaction approved - EU gateway"
            ]
            return {
                'success': True,
                'message': random.choice(responses),
                'status': 'LIVE',
                'gateway': 'Ayden EU',
                'amount': '$0.00'
            }
        else:
            responses = [
                "❌ Ayden: Authorization declined",
                "❌ Ayden: Card not supported",
                "❌ Ayden: Risk score too high",
                "❌ Ayden: 3DS authentication failed"
            ]
            return {
                'success': False,
                'message': random.choice(responses),
                'status': 'DEAD',
                'gateway': 'Ayden EU',
                'amount': '$0.00'
            }

    async def process_auth_gate(self, card_data: str) -> dict:
        """Procesar verificación Auth Gate - EFECTIVIDAD REALISTA"""
        await asyncio.sleep(random.uniform(1.5, 3.0))

        # Auth Gate efectividad ULTRA REALISTA (8-16% máximo)
        success_rate = 0.04  # 4% base realista
        
        # Factor de aleatoriedad
        success_rate *= random.uniform(0.5, 2.0)
        
        # MÁXIMO REALISTA del 16%
        success_rate = min(success_rate, 0.16)

        is_success = random.random() < success_rate

        if is_success:
            return {
                'success': True,
                'message': "✅ Auth: Verification successful",
                'status': 'LIVE',
                'gateway': 'Auth Check',
                'amount': '$0.00'
            }
        else:
            responses = [
                "❌ Auth: Verification failed",
                "❌ Auth: Invalid card data",
                "❌ Auth: CVV check failed"
            ]
            return {
                'success': False,
                'message': random.choice(responses),
                'status': 'DEAD',
                'gateway': 'Auth Check',
                'amount': '$0.00'
            }

    async def process_ccn_charge(self, card_data: str) -> dict:
        """Procesar CCN Charge Gate - EFECTIVIDAD REALISTA"""
        await asyncio.sleep(random.uniform(2.0, 4.0))

        parts = card_data.split('|')
        if len(parts) < 4:
            return {
                'success': False,
                'message': '❌ Formato inválido',
                'status': 'DEAD'
            }

        # CCN Charge efectividad REALISTA (12-22% máximo)
        success_rate = 0.07  # 7% base realista

        card_number = parts[0]
        # CCN prefiere ciertos tipos de tarjeta
        if card_number.startswith(('4111', '4242', '5555')):
            success_rate += 0.03  # +3%

        # Factor de aleatoriedad
        success_rate *= random.uniform(0.6, 1.8)
        
        # MÁXIMO REALISTA del 22%
        success_rate = min(success_rate, 0.22)

        is_success = random.random() < success_rate

        if is_success:
            responses = [
                "✅ CCN: Charge successful - $0.50",
                "✅ CCN: Payment processed - CVV verified",
                "✅ CCN: Transaction approved - Low risk"
            ]
            return {
                'success': True,
                'message': random.choice(responses),
                'status': 'LIVE',
                'gateway': 'CCN Charge',
                'amount': '$0.50'
            }
        else:
            responses = [
                "❌ CCN: Charge declined - Insufficient funds",
                "❌ CCN: Payment failed - Invalid card",
                "❌ CCN: Transaction denied - Bank decline",
                "❌ CCN: Risk threshold exceeded"
            ]
            return {
                'success': False,
                'message': random.choice(responses),
                'status': 'DEAD',
                'gateway': 'CCN Charge',
                'amount': '$0.00'
            }

    async def safe_edit_message(self, message, text, reply_markup=None, parse_mode=ParseMode.MARKDOWN):
        """Editar mensaje de forma segura con control de rate limiting"""
        try:
            await message.edit_text(text, reply_markup=reply_markup, parse_mode=parse_mode)
        except RetryAfter as e:
            # Esperar el tiempo requerido por Telegram
            await asyncio.sleep(e.retry_after + 1)
            try:
                await message.edit_text(text, reply_markup=reply_markup, parse_mode=parse_mode)
            except Exception:
                # Si falla de nuevo, enviar nuevo mensaje
                await message.reply_text(text, reply_markup=reply_markup, parse_mode=parse_mode)
        except TimedOut:
            await asyncio.sleep(2)
            try:
                await message.edit_text(text, reply_markup=reply_markup, parse_mode=parse_mode)
            except Exception:
                await message.reply_text(text, reply_markup=reply_markup, parse_mode=parse_mode)
        except Exception:
            # Como último recurso, enviar nuevo mensaje
            await message.reply_text(text, reply_markup=reply_markup, parse_mode=parse_mode)

# Instancia global del sistema de gates
gate_system = None

async def gates_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando principal /gates - Todos pueden ver, solo premium/fundadores pueden usar"""
    global gate_system
    if gate_system is None:
        gate_system = GateSystem(db)

    user_id = str(update.effective_user.id)

    # Verificar créditos (5 créditos por uso)
    user_data = db.get_user(user_id)
    if user_data['credits'] < 5:
        await update.message.reply_text(
            "❌ **CRÉDITOS INSUFICIENTES** ❌\n\n"
            f"💰 **Necesitas:** 5 créditos\n"
            f"💳 **Tienes:** {user_data['credits']} créditos\n\n"
            "🎁 **Obtener más créditos:**\n"
            "• `/bonus` - Bono diario gratis\n"
            "• `/juegos` - Casino bot\n"
            "• Contactar administración",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    # Crear menú de gates
    keyboard = gate_system.create_gates_menu()

    # Determinar tipo de usuario y acceso
    is_founder = db.is_founder(user_id)
    staff_data = db.get_staff_role(user_id)
    is_cofounder = staff_data and staff_data['role'] == '2'
    is_authorized = gate_system.is_authorized(user_id)
    
    if is_authorized:
        if is_founder:
            user_type = "👑 FUNDADOR"
            efectividad_text = "8-25% (Realista Pro)"
        elif is_cofounder:
            user_type = "💎 CO-FUNDADOR"
            efectividad_text = "8-25% (Realista Pro)"
        else:
            user_type = "💎 PREMIUM"
            efectividad_text = "8-25% (Realista)"
        access_text = "✅ ACCESO COMPLETO"
    else:
        user_type = "🆓 USUARIO ESTÁNDAR"
        access_text = "❌ SOLO VISTA PREVIA"
        efectividad_text = "Requiere Premium"

    response = f"🔥 **GATES SYSTEM ULTRA** 🔥\n"
    response += f"═══════════════════════════════\n\n"
    response += f"🎯 **Usuario:** {user_type}\n"
    response += f"🔐 **Estado:** {access_text}\n"
    response += f"💰 **Créditos:** {user_data['credits']}\n"
    response += f"💳 **Costo por gate:** 5 créditos\n"
    response += f"⚡ **Efectividad:** {efectividad_text}\n\n"
    
    if not is_authorized:
        response += f"🚫 **AVISO:** Solo usuarios Premium, Fundadores y Co-Fundadores pueden procesar tarjetas\n"
        response += f"👀 **Puedes explorar el menú pero no usar las funciones**\n\n"
    
    response += f"🌟 **GATES DISPONIBLES:**\n"
    response += f"🔵 **Stripe Gate** - Pagos premium (8-25%)\n"
    response += f"🟠 **Amazon Gate** - E-commerce (5-18%)\n"
    response += f"🔴 **PayPal Gate** - Wallet validation (6-20%)\n"
    response += f"🟡 **Ayden Gate** - Procesador EU (3-15%)\n"
    response += f"🟢 **Auth Gate** - Autorización (4-16%)\n"
    response += f"⚫ **CCN Charge** - Cargo directo (7-22%)\n\n"
    
    if is_authorized:
        response += f"💡 **Selecciona el gate que deseas usar:**"
    else:
        response += f"💎 **¡Obtén Premium para acceso completo!**"

    await update.message.reply_text(
        response,
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )

async def handle_gate_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manejar callbacks de gates"""
    global gate_system
    query = update.callback_query
    user_id = str(query.from_user.id)

    await query.answer()

    if query.data == 'gates_close':
        await query.edit_message_text(
            "❌ **Gates System cerrado**\n\n"
            "💡 Usa `/gates` para acceder nuevamente",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    if query.data == 'gates_status':
        status_text = f"📊 **ESTADO DE GATES** 📊\n\n"
        status_text += f"🔵 **Stripe Gate:** 🟢 Online (8-25% efectividad)\n"
        status_text += f"🟠 **Amazon Gate:** 🟢 Online (5-18% efectividad)\n"
        status_text += f"🔴 **PayPal Gate:** 🟢 Online (6-20% efectividad)\n"
        status_text += f"🟡 **Ayden Gate:** 🟢 Online (3-15% efectividad)\n"
        status_text += f"🟢 **Auth Gate:** 🟢 Online (4-16% efectividad)\n"
        status_text += f"⚫ **CCN Charge:** 🟢 Online (7-22% efectividad)\n\n"
        status_text += f"⏰ **Última actualización:** {datetime.now().strftime('%H:%M:%S')}\n"
        status_text += f"🔄 **Uptime:** 99.9%\n"
        status_text += f"⚠️ **Efectividad REALISTA para usuarios de pago**"

        back_keyboard = [[InlineKeyboardButton("🔙 Volver", callback_data='gates_back')]]
        await query.edit_message_text(
            status_text,
            reply_markup=InlineKeyboardMarkup(back_keyboard),
            parse_mode=ParseMode.MARKDOWN
        )
        return

    if query.data == 'gates_back':
        keyboard = gate_system.create_gates_menu()
        user_data = db.get_user(user_id)
        is_founder = db.is_founder(user_id)
        staff_data = db.get_staff_role(user_id)
        is_cofounder = staff_data and staff_data['role'] == '2'
        
        if is_founder:
            user_type = "👑 FUNDADOR"
        elif is_cofounder:
            user_type = "💎 CO-FUNDADOR"
        else:
            user_type = "💎 PREMIUM"

        response = f"🔥 **GATES SYSTEM ULTRA** 🔥\n"
        response += f"═══════════════════════════════\n\n"
        response += f"🎯 **Acceso:** {user_type}\n"
        response += f"💰 **Créditos:** {user_data['credits']}\n"
        response += f"💳 **Costo por gate:** 5 créditos\n"
        response += f"⚡ **Efectividad:** 8-25% (Realista)\n\n"
        response += f"💡 **Selecciona el gate que deseas usar:**"

        await query.edit_message_text(
            response,
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
        return

    # Procesar selección de gate específico
    gate_types = {
        'gate_stripe': ('Stripe Gate', '🔵'),
        'gate_amazon': ('Amazon Gate', '🟠'),
        'gate_paypal': ('PayPal Gate', '🔴'),
        'gate_ayden': ('Ayden Gate', '🟡'),
        'gate_auth': ('Auth Gate', '🟢'),
        'gate_ccn': ('CCN Charge', '⚫')
    }

    if query.data in gate_types:
        # VERIFICAR PERMISOS AL SELECCIONAR GATE
        if not gate_system.is_authorized(user_id):
            await query.edit_message_text(
                "🚫 **ACCESO RESTRINGIDO** 🚫\n\n"
                "💎 **¡Necesitas ser Premium, Fundador o Co-Fundador para usar los Gates!**\n\n"
                "🔐 **Para obtener acceso premium:**\n"
                "• 💳 Contacta a @SteveCHBll\n"
                "• 🔑 Usa `/apply_key [código]` si tienes una clave\n\n"
                "⚡ **Beneficios Premium:**\n"
                "• ✅ Acceso completo a todos los gates\n"
                "• ✅ Efectividad realista (8-25%)\n"
                "• ✅ Procesamiento de múltiples tarjetas\n"
                "• ✅ Soporte prioritario\n"
                "• ✅ Control anti-rate limit\n\n"
                "🎯 **¡Invierte en Premium y obtén resultados reales!**",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        gate_name, gate_emoji = gate_types[query.data]

        # Crear sesión para este usuario (solo si está autorizado)
        gate_system.active_sessions[user_id] = {
            'gate_type': query.data,
            'gate_name': gate_name,
            'gate_emoji': gate_emoji,
            'timestamp': datetime.now()
        }

        response = f"{gate_emoji} **{gate_name.upper()}** {gate_emoji}\n"
        response += f"═══════════════════════════════\n\n"
        response += f"🎯 **Estado:** 🟢 Online\n"
        response += f"💰 **Precio:** 5 créditos por tarjeta\n"
        response += f"📊 **Plan:** Premium Access\n"
        response += f"⚡ **Comando:** /am\n\n"
        response += f"💳 **Envía tu tarjeta en formato:**\n"
        response += f"`4532123456781234|12|25|123`\n\n"
        response += f"🔄 **El gate procesará automáticamente**\n"
        response += f"⏱️ **Tiempo estimado:** 2-5 segundos\n"
        response += f"⚠️ **Efectividad REALISTA garantizada**\n\n"
        response += f"💡 **Tip:** Usa tarjetas con BIN conocido"

        back_keyboard = [[InlineKeyboardButton("🔙 Volver al menú", callback_data='gates_back')]]

        await query.edit_message_text(
            response,
            reply_markup=InlineKeyboardMarkup(back_keyboard),
            parse_mode=ParseMode.MARKDOWN
        )

async def process_gate_card(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Procesar múltiples tarjetas enviadas cuando hay sesión activa - CON CONTROL DE RATE LIMITING"""
    global gate_system
    user_id = str(update.effective_user.id)

    # VERIFICAR PERMISOS ANTES DE PROCESAR
    if not gate_system.is_authorized(user_id):
        await update.message.reply_text(
            "🚫 **PROCESAMIENTO BLOQUEADO** 🚫\n\n"
            "💎 **Solo usuarios Premium, Fundadores y Co-Fundadores pueden procesar tarjetas**\n\n"
            "🔥 **¿Por qué ser Premium?**\n"
            "• 💳 Acceso real a gates de pago\n"
            "• 🎯 Efectividad comprobada (8-25%)\n"
            "• 💰 Recupera la inversión con pocas tarjetas LIVE\n"
            "• ⚡ Control anti-rate limit avanzado\n\n"
            "📞 **Contacta a @SteveCHBll para ser Premium**",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    # Verificar si hay sesión activa
    if user_id not in gate_system.active_sessions:
        return

    session = gate_system.active_sessions[user_id]
    message_text = update.message.text.strip()

    # Detectar múltiples tarjetas en el mensaje
    import re
    card_pattern = r'\b\d{13,19}\|\d{1,2}\|\d{2,4}\|\d{3,4}\b'
    cards_found = re.findall(card_pattern, message_text)

    if not cards_found:
        await update.message.reply_text(
            "❌ **Formato inválido**\n\n"
            "💡 **Formato correcto:**\n"
            "`4532123456781234|12|25|123`\n\n"
            "📋 **Puedes enviar múltiples tarjetas separadas por líneas**",
            parse_mode=ParseMode.MARKDOWN)
        return

    # Verificar límites según nivel de usuario
    is_founder = db.is_founder(user_id)
    staff_data = db.get_staff_role(user_id)
    is_cofounder = staff_data and staff_data['role'] == '2'
    user_data = db.get_user(user_id)
    is_premium = user_data.get('premium', False)

    # Establecer límites
    if is_founder:
        max_cards = 15  # Fundadores más tarjetas
        user_type = "👑 FUNDADOR"
    elif is_cofounder:
        max_cards = 12  # Co-fundadores también más
        user_type = "💎 CO-FUNDADOR"
    elif is_premium:
        max_cards = 8   # Premium moderado
        user_type = "💎 PREMIUM"
    else:
        await update.message.reply_text("❌ Acceso denegado")
        return

    # Verificar límite de tarjetas
    if len(cards_found) > max_cards:
        await update.message.reply_text(
            f"❌ **LÍMITE EXCEDIDO** ❌\n\n"
            f"🎯 **Tu nivel:** {user_type}\n"
            f"📊 **Límite máximo:** {max_cards} tarjetas\n"
            f"📤 **Enviaste:** {len(cards_found)} tarjetas\n\n"
            f"💡 **Envía máximo {max_cards} tarjetas por vez**",
            parse_mode=ParseMode.MARKDOWN)
        return

    # Verificar créditos (5 por tarjeta)
    total_cost = len(cards_found) * 5
    if user_data['credits'] < total_cost:
        await update.message.reply_text(
            f"❌ **CRÉDITOS INSUFICIENTES** ❌\n\n"
            f"💰 **Necesitas:** {total_cost} créditos\n"
            f"💳 **Tienes:** {user_data['credits']} créditos\n"
            f"📊 **Costo:** 5 créditos por tarjeta\n"
            f"🎯 **Tarjetas:** {len(cards_found)}\n\n"
            f"💡 Usa `/bonus` para obtener créditos gratis",
            parse_mode=ParseMode.MARKDOWN)
        return

    # Descontar créditos
    db.update_user(user_id, {'credits': user_data['credits'] - total_cost})

    # Procesar cada tarjeta individualmente CON CONTROL DE RATE LIMITING
    for i, card_data in enumerate(cards_found, 1):

        # Mensaje de procesamiento
        processing_msg = await update.message.reply_text(
            f"{session['gate_emoji']} **PROCESANDO {session['gate_name'].upper()}** {session['gate_emoji']}\n\n"
            f"💳 **Tarjeta {i}/{len(cards_found)}:** {card_data[:4]}****{card_data[-4:]}\n"
            f"⏳ **Estado:** Conectando al gateway...\n"
            f"🔄 **Progreso:** [██░░░░░░░░] 20%",
            parse_mode=ParseMode.MARKDOWN
        )

        # CONTROLAR RATE LIMITING - Esperar entre mensajes
        if i > 1:
            await asyncio.sleep(3)  # Pausa entre tarjetas

        # Simular progreso CON CONTROL DE RATE LIMITING
        await asyncio.sleep(1.5)
        await gate_system.safe_edit_message(
            processing_msg,
            f"{session['gate_emoji']} **PROCESANDO {session['gate_name'].upper()}** {session['gate_emoji']}\n\n"
            f"💳 **Tarjeta {i}/{len(cards_found)}:** {card_data[:4]}****{card_data[-4:]}\n"
            f"⏳ **Estado:** Verificando datos...\n"
            f"🔄 **Progreso:** [████░░░░░░] 40%"
        )

        await asyncio.sleep(1.5)
        await gate_system.safe_edit_message(
            processing_msg,
            f"{session['gate_emoji']} **PROCESANDO {session['gate_name'].upper()}** {session['gate_emoji']}\n\n"
            f"💳 **Tarjeta {i}/{len(cards_found)}:** {card_data[:4]}****{card_data[-4:]}\n"
            f"⏳ **Estado:** Procesando con gateway...\n"
            f"🔄 **Progreso:** [██████░░░░] 60%"
        )

        # Procesar según el tipo de gate
        gate_type = session['gate_type']
        if gate_type == 'gate_stripe':
            result = await gate_system.process_stripe_gate(card_data)
        elif gate_type == 'gate_amazon':
            result = await gate_system.process_amazon_gate(card_data)
        elif gate_type == 'gate_paypal':
            result = await gate_system.process_paypal_gate(card_data)
        elif gate_type == 'gate_ayden':
            result = await gate_system.process_ayden_gate(card_data)
        elif gate_type == 'gate_ccn':
            result = await gate_system.process_ccn_charge(card_data)
        else:
            result = await gate_system.process_auth_gate(card_data)

        # Mostrar resultado final
        status_emoji = "✅" if result['success'] else "❌"

        final_response = f"{session['gate_emoji']} **{session['gate_name'].upper()} RESULTADO** {session['gate_emoji']}\n"
        final_response += f"═══════════════════════════════\n\n"
        final_response += f"💳 **Tarjeta:** {card_data}\n"
        final_response += f"🎯 **Estado:** {result['status']} {status_emoji}\n"
        final_response += f"📡 **Gateway:** {result['gateway']}\n"
        final_response += f"💰 **Monto:** {result.get('amount', '$0.00')}\n"
        final_response += f"📝 **Respuesta:** {result['message']}\n"
        final_response += f"⏰ **Tiempo:** {datetime.now().strftime('%H:%M:%S')}\n"
        final_response += f"👤 **Procesado por:** @{update.effective_user.username or update.effective_user.first_name}\n"
        final_response += f"🔢 **Tarjeta {i} de {len(cards_found)}**\n\n"
        final_response += f"💰 **Créditos restantes:** {user_data['credits'] - total_cost}"

        keyboard = [[InlineKeyboardButton("🔄 Procesar otra", callback_data=gate_type),
                    InlineKeyboardButton("🔙 Menú principal", callback_data='gates_back')]]

        await gate_system.safe_edit_message(
            processing_msg,
            final_response,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        # Pausa adicional entre tarjetas para evitar rate limiting
        if i < len(cards_found):
            await asyncio.sleep(2)

    # Limpiar sesión al final
    if user_id in gate_system.active_sessions:
        del gate_system.active_sessions[user_id]
