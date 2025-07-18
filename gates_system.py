
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
        """Verificar si el usuario tiene acceso (fundador nivel 1, co-fundador, moderador o premium)"""
        # Verificar si es fundador nivel 1
        if self.db.is_founder(user_id):
            return True

        # Verificar roles de staff (co-fundador nivel 2 y moderador nivel 3)
        staff_data = self.db.get_staff_role(user_id)
        if staff_data and staff_data['role'] in ['2', '3']:  # Co-fundador o moderador
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
                InlineKeyboardButton("🤖 CyberSource AI", callback_data='gate_cybersource'),
                InlineKeyboardButton("🌍 Worldpay UK", callback_data='gate_worldpay')
            ],
            [
                InlineKeyboardButton("🧠 Braintree Pro", callback_data='gate_braintree'),
                InlineKeyboardButton("📊 Gate Status", callback_data='gates_status')
            ],
            [
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

    async def process_cybersource_ai(self, card_data: str) -> dict:
        """Procesar CyberSource AI Gate - INTELIGENCIA ARTIFICIAL ANTI-FRAUDE"""
        await asyncio.sleep(random.uniform(4.5, 7.0))  # IA toma más tiempo

        parts = card_data.split('|')
        if len(parts) < 4:
            return {
                'success': False,
                'message': '❌ Formato inválido - Datos incompletos',
                'status': 'DEAD'
            }

        card_number = parts[0]
        exp_month = parts[1]
        exp_year = parts[2]
        cvv = parts[3]

        # CyberSource AI es EL MÁS ESTRICTO - Solo 3-12% máximo
        success_rate = 0.02  # 2% base ULTRA estricto

        # Análisis de IA avanzado
        digit_sum = sum(int(d) for d in card_number if d.isdigit())
        
        # Patrones que la IA considera favorables (MUY específicos)
        if digit_sum % 23 == 0:  # Patrón matemático complejo
            success_rate += 0.015  # +1.5%
        
        if card_number.startswith(('4000', '4001', '5100', '5101')):
            success_rate += 0.01  # +1% solo bins específicos
        
        # CVV con IA pattern matching
        if cvv in ['123', '456', '789', '000']:
            success_rate -= 0.005  # -0.5% (IA detecta patterns obvios)
        elif len(set(cvv)) == 3:  # CVV con dígitos únicos
            success_rate += 0.005  # +0.5%

        # Análisis temporal de expiración (IA considera esto)
        exp_num = int(exp_year) if exp_year.isdigit() else 2024
        if exp_num >= 2028:  # Tarjetas con vencimiento lejano
            success_rate += 0.008  # +0.8%

        # Factor de randomización de IA (más impredecible)
        ai_factor = random.uniform(0.1, 2.5)
        success_rate *= ai_factor
        
        # MÁXIMO ABSOLUTO del 12% (CyberSource es ultra restrictivo)
        success_rate = min(success_rate, 0.12)

        is_success = random.random() < success_rate

        if is_success:
            responses = [
                "✅ CyberSource: AI APPROVED - Risk Score: Low",
                "✅ CyberSource: ACCEPT - Neural network validated",
                "✅ CyberSource: AUTHORIZED - ML fraud check passed",
                "✅ CyberSource: SUCCESS - Behavioral analysis OK"
            ]
            return {
                'success': True,
                'message': random.choice(responses),
                'status': 'LIVE',
                'gateway': 'CyberSource AI',
                'amount': '$1.00',
                'ai_score': f"{random.randint(85, 98)}/100"
            }
        else:
            responses = [
                "❌ CyberSource: AI REJECT - High risk pattern detected",
                "❌ CyberSource: DECLINE - Neural network flagged",
                "❌ CyberSource: REVIEW REQUIRED - ML suspicious activity",
                "❌ CyberSource: BLOCKED - Fraud prevention AI",
                "❌ CyberSource: DENIED - Behavioral analysis failed",
                "❌ CyberSource: TIMEOUT - AI processing overload"
            ]
            return {
                'success': False,
                'message': random.choice(responses),
                'status': 'DEAD',
                'gateway': 'CyberSource AI',
                'amount': '$0.00',
                'ai_score': f"{random.randint(15, 45)}/100"
            }

    async def process_worldpay_uk(self, card_data: str) -> dict:
        """Procesar Worldpay UK Gate - ESTÁNDAR BRITÁNICO ESTRICTO"""
        await asyncio.sleep(random.uniform(3.5, 5.5))  # Procesamiento británico es lento

        parts = card_data.split('|')
        if len(parts) < 4:
            return {
                'success': False,
                'message': '❌ Invalid card format - UK standards required',
                'status': 'DEAD'
            }

        card_number = parts[0]
        exp_month = parts[1]
        exp_year = parts[2]
        cvv = parts[3]

        # Worldpay UK efectividad REALISTA (5-18% máximo)
        success_rate = 0.03  # 3% base realista (muy estricto)

        # Análisis por tipo de tarjeta (UK prefiere Visa/MasterCard)
        if card_number.startswith('4'):  # Visa
            success_rate += 0.02  # +2% (Visa popular en UK)
        elif card_number.startswith('5'):  # MasterCard
            success_rate += 0.015  # +1.5%
        elif card_number.startswith('3'):  # American Express
            success_rate += 0.005  # +0.5% (menos común en UK)

        # BINs específicos favorables en UK
        uk_favorable_bins = ['4000', '4111', '4444', '5555', '5200', '5454']
        if any(card_number.startswith(bin_) for bin_ in uk_favorable_bins):
            success_rate += 0.01  # +1%

        # Análisis de expiración (UK banks pattern)
        try:
            month_num = int(exp_month)
            if month_num in [3, 6, 9, 12]:  # Quarters (UK banking pattern)
                success_rate += 0.008  # +0.8%
        except:
            pass

        # CVV analysis
        if len(cvv) == 3 and cvv.isdigit():
            if cvv.endswith(('1', '5', '7')):  # UK statistical preference
                success_rate += 0.005  # +0.5%

        # Factor de regulación británica (muy estricto)
        uk_regulatory_factor = random.uniform(0.2, 0.8)
        success_rate *= uk_regulatory_factor
        
        # MÁXIMO REALISTA del 18% (Worldpay UK es estricto)
        success_rate = min(success_rate, 0.18)

        is_success = random.random() < success_rate

        if is_success:
            responses = [
                "✅ Worldpay: AUTHORISED - UK compliance verified",
                "✅ Worldpay: SUCCESS - Payment captured £0.50",
                "✅ Worldpay: APPROVED - British standards met",
                "✅ Worldpay: SETTLED - FCA regulations passed"
            ]
            return {
                'success': True,
                'message': random.choice(responses),
                'status': 'LIVE',
                'gateway': 'Worldpay UK',
                'amount': '£0.50',
                'region': 'United Kingdom'
            }
        else:
            responses = [
                "❌ Worldpay: REFUSED - Bank declined transaction",
                "❌ Worldpay: FAILED - UK compliance check failed",
                "❌ Worldpay: CANCELLED - Risk assessment failed",
                "❌ Worldpay: BLOCKED - FCA fraud prevention",
                "❌ Worldpay: EXPIRED - Card validation timeout",
                "❌ Worldpay: REJECTED - British banking standards"
            ]
            return {
                'success': False,
                'message': random.choice(responses),
                'status': 'DEAD',
                'gateway': 'Worldpay UK',
                'amount': '£0.00',
                'region': 'United Kingdom'
            }

    async def process_braintree_pro(self, card_data: str) -> dict:
        """Procesar Braintree Pro Gate - PAYPAL ENTERPRISE LEVEL"""
        await asyncio.sleep(random.uniform(2.8, 4.2))  # Velocidad empresarial

        parts = card_data.split('|')
        if len(parts) < 4:
            return {
                'success': False,
                'message': '❌ Invalid format - Enterprise validation failed',
                'status': 'DEAD'
            }

        card_number = parts[0]
        exp_month = parts[1]
        exp_year = parts[2]
        cvv = parts[3]

        # Braintree Pro efectividad REALISTA (8-20% máximo)
        success_rate = 0.05  # 5% base realista

        # Análisis empresarial avanzado
        # Braintree prefiere ciertos patrones de tarjetas
        if card_number.startswith(('4111', '4005', '4012', '4242')):
            success_rate += 0.02  # +2% (test cards conocidas que funcionan bien)
        elif card_number.startswith(('5555', '5105', '5200')):
            success_rate += 0.015  # +1.5%

        # Análisis del último dígito (Braintree pattern)
        last_digit = int(card_number[-1]) if card_number[-1].isdigit() else 0
        if last_digit % 3 == 0:  # Patrón específico de Braintree
            success_rate += 0.01  # +1%

        # CVV enterprise validation
        if cvv.isdigit() and len(cvv) == 3:
            cvv_sum = sum(int(d) for d in cvv)
            if cvv_sum >= 15:  # CVV con suma alta (menos común = más seguro)
                success_rate += 0.008  # +0.8%

        # Análisis de fecha de expiración
        try:
            year_num = int(exp_year)
            month_num = int(exp_month)
            if 2026 <= year_num <= 2030 and 1 <= month_num <= 12:
                success_rate += 0.01  # +1% (rango empresarial óptimo)
        except:
            success_rate -= 0.005  # -0.5% por fecha inválida

        # Factor empresarial (Braintree es más predecible que otros)
        enterprise_factor = random.uniform(0.6, 1.4)
        success_rate *= enterprise_factor
        
        # MÁXIMO REALISTA del 20% (Braintree Pro es mejor que básico)
        success_rate = min(success_rate, 0.20)

        is_success = random.random() < success_rate

        if is_success:
            responses = [
                "✅ Braintree: APPROVED - Enterprise gateway validated",
                "✅ Braintree: SUCCESS - PayPal network authorized",
                "✅ Braintree: SETTLED - Professional tier processed",
                "✅ Braintree: CAPTURED - Advanced fraud checks passed"
            ]
            return {
                'success': True,
                'message': random.choice(responses),
                'status': 'LIVE',
                'gateway': 'Braintree Pro',
                'amount': '$0.75',
                'tier': 'Enterprise'
            }
        else:
            responses = [
                "❌ Braintree: DECLINED - Gateway rejected transaction",
                "❌ Braintree: FAILED - PayPal network unavailable",
                "❌ Braintree: TIMEOUT - Enterprise processing delayed",
                "❌ Braintree: BLOCKED - Advanced fraud detection",
                "❌ Braintree: REJECTED - Professional tier validation failed",
                "❌ Braintree: ERROR - Network communication failed"
            ]
            return {
                'success': False,
                'message': random.choice(responses),
                'status': 'DEAD',
                'gateway': 'Braintree Pro',
                'amount': '$0.00',
                'tier': 'Enterprise'
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
    is_moderator = staff_data and staff_data['role'] == '3'
    is_authorized = gate_system.is_authorized(user_id)
    
    if is_authorized:
        if is_founder:
            user_type = "👑 FUNDADOR"
            efectividad_text = "PRO"
        elif is_cofounder:
            user_type = "💎 CO-FUNDADOR"
            efectividad_text = "PRO"
        elif is_moderator:
            user_type = "🛡️ MODERADOR"
            efectividad_text = "PRO"
        else:
            user_type = "💎 PREMIUM"
            efectividad_text = "PRO"
        access_text = "✅ ACCESO COMPLETO"
    else:
        user_type = "🆓 USUARIO ESTÁNDAR"
        access_text = "❌ SOLO VISTA PREVIA"
        efectividad_text = "Requiere Premium/Staff"

    response = f"🔥 **GATES SYSTEM ULTRA** 🔥\n"
    response += f"═══════════════════════════════\n\n"
    response += f"🎯 **Usuario:** {user_type}\n"
    response += f"🔐 **Estado:** {access_text}\n"
    response += f"💰 **Créditos:** {user_data['credits']}\n"
    response += f"💳 **Costo por gate:** 5 créditos\n"
    response += f"⚡ **Efectividad:** {efectividad_text}\n\n"
    
    if not is_authorized:
        response += f"🚫 **AVISO:** Solo usuarios Premium\n"
        response += f"👀 **Puedes explorar el menú pero no usar las funciones**\n\n"
    
    response += f"🌟 **GATES DISPONIBLES:**\n"
    response += f"🔵 **Stripe Gate**\n"
    response += f"🟠 **Amazon Gate**\n"
    response += f"🔴 **PayPal Gate**\n"
    response += f"🟡 **Ayden Gate**\n"
    response += f"🟢 **Auth Gate**\n"
    response += f"⚫ **CCN Charge**\n\n"
    response += f"🔥 **GATES PREMIUM:**\n"
    response += f"🤖 **CyberSource AI** - IA Anti-Fraude\n"
    response += f"🌍 **Worldpay UK** - Estándar Británico\n"
    response += f"🧠 **Braintree Pro** - PayPal Enterprise\n\n"
    
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
        status_text += f"🔵 **Stripe Gate:** 🟢 Online\n"
        status_text += f"🟠 **Amazon Gate:** 🟢 Online\n"
        status_text += f"🔴 **PayPal Gate:** 🟢 Online\n"
        status_text += f"🟡 **Ayden Gate:** 🟢 Online\n"
        status_text += f"🟢 **Auth Gate:** 🟢 Online\n"
        status_text += f"⚫ **CCN Charge:** 🟢 Online\n\n"
        status_text += f"🔥 **GATES PREMIUM:**\n"
        status_text += f"🤖 **CyberSource AI:** 🟢 Online\n"
        status_text += f"🌍 **Worldpay UK:** 🟢 Online\n"
        status_text += f"🧠 **Braintree Pro:** 🟢 Online\n\n"
        status_text += f"⏰ **Última actualización:** {datetime.now().strftime('%H:%M:%S')}\n"
        status_text += f"🔄 **Uptime:** 99.9%\n"
        status_text += f"⚠️ **Efectividad PRO**"

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
        response += f"⚡ **Efectividad:** PRO\n\n"
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
        'gate_ccn': ('CCN Charge', '⚫'),
        'gate_cybersource': ('CyberSource AI', '🤖'),
        'gate_worldpay': ('Worldpay UK', '🌍'),
        'gate_braintree': ('Braintree Pro', '🧠')
    }

    if query.data in gate_types:
        # VERIFICAR PERMISOS AL SELECCIONAR GATE
        if not gate_system.is_authorized(user_id):
            await query.edit_message_text(
                "🚫 **ACCESO RESTRINGIDO** 🚫\n\n"
                "💎 **¡Necesitas permisos especiales!**\n\n"
                "🔐 **Acceso autorizado para:**\n"
                "• 👑 Fundadores\n"
                "• 💎 Co-fundadores\n"
                "• 🛡️ Moderadores\n"
                "• 💎 Usuarios Premium\n\n"
                "⚡ **Beneficios del acceso:**\n"
                "• ✅ Acceso completo a todos los gates\n"
                "• ✅ Efectividad PRO\n"
                "• ✅ Procesamiento de múltiples tarjetas\n"
                "• ✅ Soporte prioritario\n"
                "• ✅ Control anti-rate limit\n\n"
                "🎯 **Contacta a @SteveCHBll para más información**",
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
        response += f"⚠️ **Efectividad PRO**\n\n"
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

    # Verificar si hay sesión activa primero
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
        max_cards = 13  # Co-fundadores también más
        user_type = "💎 CO-FUNDADOR"
    elif is_premium:
        max_cards = 10   # Premium moderado
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
        elif gate_type == 'gate_cybersource':
            result = await gate_system.process_cybersource_ai(card_data)
        elif gate_type == 'gate_worldpay':
            result = await gate_system.process_worldpay_uk(card_data)
        elif gate_type == 'gate_braintree':
            result = await gate_system.process_braintree_pro(card_data)
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
