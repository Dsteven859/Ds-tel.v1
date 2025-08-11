import os
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError, OperationFailure
import json

logger = logging.getLogger(__name__)

class MongoDatabase:
    def __init__(self):
        self.client = None
        self.db = None
        self.collections = {}
        self.connection_status = False
        # Obtener configuración desde variables de entorno (Secrets)
        self.connection_url = os.getenv('MONGODB_URL') or os.getenv('MONGODB_CONNECTION_STRING')
        self.db_name = os.getenv('MONGODB_DB_NAME', 'telegram_bot_db') or os.getenv('DATABASE_NAME', 'telegram_bot_db')
        self.last_connection_attempt = None
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 5

        # Validar que las variables estén configuradas
        if not self.connection_url:
            logger.error("❌ MONGODB_URL no encontrado en variables de entorno")
            logger.info("💡 Configura MONGODB_URL en Secrets con tu cadena de conexión de MongoDB Atlas")
        elif not self._validate_mongodb_url(self.connection_url):
            logger.error("❌ La MONGODB_URL proporcionada no es válida.")

        self.staff_roles = {}
        self.check_chats = {}
        self.pending_checks = {}
        self.deleted_links = {}
        self.admin_log_channels = {}
        self.admin_action_logs = []

    async def connect(self) -> bool:
        """Conectar a MongoDB Atlas usando variables de entorno de Secrets"""
        try:
            # Verificar variables de entorno requeridas
            if not self.connection_url:
                logger.error("❌ MONGODB_URL no configurado en variables de entorno")
                logger.error("💡 Ve a Secrets y configura:")
                logger.error("   - MONGODB_URL: Tu cadena de conexión de MongoDB Atlas")
                logger.error("   - MONGODB_DB_NAME: Nombre de tu base de datos (opcional)")
                return False

            if not self._validate_mongodb_url(self.connection_url):
                logger.error("❌ La MONGODB_URL proporcionada no es válida.")
                return False

            # Ocultar información sensible en logs
            safe_url = self.connection_url.replace(self.connection_url.split('@')[0].split('//')[1], '***:***')
            logger.info(f"🔄 Conectando a MongoDB Atlas: {safe_url.split('@')[1] if '@' in safe_url else 'Atlas'}")
            self.last_connection_attempt = datetime.now()

            # Configurar cliente con timeouts optimizados
            self.client = MongoClient(
                self.connection_url,
                serverSelectionTimeoutMS=5000,  # 5 segundos timeout
                connectTimeoutMS=10000,  # 10 segundos para conectar
                socketTimeoutMS=30000,   # 30 segundos para operaciones
                maxPoolSize=10,          # Pool de conexiones
                retryWrites=True         # Reintentar escrituras
            )

            # Verificar conexión
            self.client.admin.command('ping')
            self.db = self.client[self.db_name]

            # Configurar colecciones
            self.collections = {
                'users': self.db.users,
                'staff': self.db.staff,
                'founders': self.db.founders,
                'sessions': self.db.sessions,
                'logs': self.db.logs,
                'stats': self.db.stats
            }

            # Crear índices para optimización
            await self._create_indexes()

            self.connection_status = True
            self.reconnect_attempts = 0
            logger.info("✅ Conectado exitosamente a MongoDB Atlas")
            return True

        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"❌ Error de conexión a MongoDB: {e}")
            self.connection_status = False
            return False
        except Exception as e:
            logger.error(f"❌ Error inesperado conectando a MongoDB: {e}")
            self.connection_status = False
            return False

    async def _create_indexes(self):
        """Crear índices para optimizar consultas"""
        try:
            # Índice para usuarios
            self.collections['users'].create_index("user_id", unique=True)
            self.collections['users'].create_index("premium_until")

            # Índice para staff
            self.collections['staff'].create_index("user_id", unique=True)

            # Índice para logs
            self.collections['logs'].create_index("timestamp")
            self.collections['logs'].create_index("user_id")

            logger.info("✅ Índices de MongoDB creados correctamente")
        except Exception as e:
            logger.error(f"Error creando índices: {e}")

    def _validate_mongodb_url(self, url: str) -> bool:
        """Validar formato básico de URL de MongoDB"""
        try:
            import re

            # Patrones válidos para MongoDB
            patterns = [
                r'^mongodb\+srv://[^:]+:[^@]+@[^/]+\.mongodb\.net/',  # Atlas SRV
                r'^mongodb://[^:]+:[^@]+@[^/]+/',  # MongoDB estándar
                r'^mongodb://[^/]+/',  # MongoDB sin credenciales
                r'^mongodb\+srv://[^/]+\.mongodb\.net/'  # Atlas SRV sin credenciales
            ]

            for pattern in patterns:
                if re.match(pattern, url):
                    logger.info("✅ Formato de URL MongoDB válido")
                    return True

            logger.error("❌ Formato de URL MongoDB inválido")
            logger.error("💡 Formatos válidos:")
            logger.error("   - mongodb+srv://user:pass@cluster.mongodb.net/dbname")
            logger.error("   - mongodb://user:pass@host:port/dbname")
            return False

        except Exception as e:
            logger.error(f"Error validando URL: {e}")
            return False

    async def ensure_connection(self) -> bool:
        """Asegurar que hay conexión activa"""
        if not self.connection_status or not self.client:
            return await self.connect()

        try:
            # Verificar conexión con ping
            self.client.admin.command('ping')
            return True
        except:
            self.connection_status = False
            return await self.auto_reconnect()

    async def auto_reconnect(self) -> bool:
        """Reconexión automática"""
        if self.reconnect_attempts >= self.max_reconnect_attempts:
            logger.error(f"❌ Máximo de intentos de reconexión alcanzado ({self.max_reconnect_attempts})")
            return False

        self.reconnect_attempts += 1
        logger.info(f"🔄 Intento de reconexión #{self.reconnect_attempts}")

        # Esperar antes de reconectar
        await asyncio.sleep(2 ** self.reconnect_attempts)  # Backoff exponencial

        return await self.connect()

    def get_user(self, user_id: str) -> Dict[str, Any]:
        """Obtener datos de usuario"""
        try:
            if not self.connection_status:
                asyncio.create_task(self.ensure_connection())
                return self._get_default_user(user_id)

            user = self.collections['users'].find_one({"user_id": user_id})

            if not user:
                # Crear usuario nuevo
                default_user = self._get_default_user(user_id)
                self.collections['users'].insert_one(default_user)
                return default_user

            # Remover _id de MongoDB para compatibilidad
            user.pop('_id', None)
            return user

        except Exception as e:
            logger.error(f"Error obteniendo usuario {user_id}: {e}")
            return self._get_default_user(user_id)

    def _get_default_user(self, user_id: str) -> Dict[str, Any]:
        """Usuario por defecto"""
        return {
            'user_id': user_id,
            'credits': 10,
            'total_generated': 0,
            'join_date': datetime.now().isoformat(),
            'premium': False,
            'premium_until': None,
            'last_bonus': None,
            'warnings': 0,
            'banned': False
        }

    def update_user(self, user_id: str, data: Dict[str, Any]):
        """Actualizar datos de usuario"""
        try:
            if not self.connection_status:
                asyncio.create_task(self.ensure_connection())
                return

            # Actualizar timestamp
            data['updated_at'] = datetime.now().isoformat()

            self.collections['users'].update_one(
                {"user_id": user_id},
                {"$set": data},
                upsert=True
            )

        except Exception as e:
            logger.error(f"Error actualizando usuario {user_id}: {e}")

    def is_founder(self, user_id: str) -> bool:
        """Verificar si es fundador"""
        try:
            if not self.connection_status:
                return False

            founder = self.collections['founders'].find_one({"user_id": user_id})
            return founder is not None

        except Exception as e:
            logger.error(f"Error verificando fundador {user_id}: {e}")
            return False

    def add_founder(self, user_id: str, added_by: str = None):
        """Agregar fundador"""
        try:
            if not self.connection_status:
                return False

            founder_data = {
                "user_id": user_id,
                "added_at": datetime.now().isoformat(),
                "added_by": added_by,
                "level": 1
            }

            self.collections['founders'].update_one(
                {"user_id": user_id},
                {"$set": founder_data},
                upsert=True
            )
            return True

        except Exception as e:
            logger.error(f"Error agregando fundador {user_id}: {e}")
            return False

    def get_staff_role(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Obtener rol de staff"""
        try:
            if not self.connection_status:
                return None

            staff = self.collections['staff'].find_one({"user_id": user_id})
            if staff:
                staff.pop('_id', None)
            return staff

        except Exception as e:
            logger.error(f"Error obteniendo staff {user_id}: {e}")
            return None

    def set_staff_role(self, user_id: str, role: str, assigned_by: str = None):
        """Asignar rol de staff"""
        try:
            if not self.connection_status:
                return False

            staff_data = {
                "user_id": user_id,
                "role": role,
                "assigned_at": datetime.now().isoformat(),
                "assigned_by": assigned_by
            }

            self.collections['staff'].update_one(
                {"user_id": user_id},
                {"$set": staff_data},
                upsert=True
            )
            return True

        except Exception as e:
            logger.error(f"Error asignando staff {user_id}: {e}")
            return False

    def log_action(self, user_id: str, action: str, details: Dict[str, Any] = None):
        """Registrar acción en logs"""
        try:
            if not self.connection_status:
                return

            log_entry = {
                "user_id": user_id,
                "action": action,
                "details": details or {},
                "timestamp": datetime.now().isoformat()
            }

            self.collections['logs'].insert_one(log_entry)

        except Exception as e:
            logger.error(f"Error registrando acción: {e}")

    def get_all_by_role(self, role: str) -> list:
        """Obtener todos los usuarios de un rol específico"""
        try:
            if not self.connection_status:
                return []

            staff_members = self.collections['staff'].find({"role": role})
            return [staff['user_id'] for staff in staff_members]

        except Exception as e:
            logger.error(f"Error obteniendo usuarios por rol {role}: {e}")
            return []

    def load_data(self):
        """Método de compatibilidad - recargar datos desde MongoDB"""
        try:
            # Este método existe para compatibilidad con el sistema anterior
            # En MongoDB, los datos ya están siempre actualizados
            if not self.connection_status:
                asyncio.create_task(self.ensure_connection())
            logger.info("🔄 Datos recargados desde MongoDB")
        except Exception as e:
            logger.error(f"Error recargando datos: {e}")

    def save_data(self):
        """Método de compatibilidad - guardar datos en MongoDB"""
        try:
            # Este método existe para compatibilidad con el sistema anterior
            # En MongoDB, los datos se guardan automáticamente
            logger.info("💾 Datos guardados en MongoDB")
        except Exception as e:
            logger.error(f"Error guardando datos: {e}")

    def is_cofounder(self, user_id: str) -> bool:
        """Verificar si el usuario es co-fundador"""
        try:
            if not self.connection_status:
                return False

            staff = self.collections['staff'].find_one({"user_id": user_id, "role": "2"})
            return staff is not None

        except Exception as e:
            logger.error(f"Error verificando co-fundador {user_id}: {e}")
            return False

    def is_moderator(self, user_id: str) -> bool:
        """Verificar si el usuario es moderador"""
        try:
            if not self.connection_status:
                return False

            staff = self.collections['staff'].find_one({"user_id": user_id, "role": "3"})
            return staff is not None

        except Exception as e:
            logger.error(f"Error verificando moderador {user_id}: {e}")
            return False

    def increment_mod_warns(self, user_id: str) -> int:
        """Incrementar contador de warns para moderadores"""
        try:
            if not self.connection_status:
                return 0

            result = self.collections['staff'].update_one(
                {"user_id": user_id},
                {"$inc": {"warn_count": 1}},
                upsert=False
            )

            if result.modified_count > 0:
                staff = self.collections['staff'].find_one({"user_id": user_id})
                return staff.get('warn_count', 0) if staff else 0
            else:
                return 0

        except Exception as e:
            logger.error(f"Error incrementando warns de moderador {user_id}: {e}")
            return 0

    def get_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas generales"""
        try:
            if not self.connection_status:
                return {}

            stats = {
                'total_users': self.collections['users'].count_documents({}),
                'premium_users': self.collections['users'].count_documents({"premium": True}),
                'total_staff': self.collections['staff'].count_documents({}),
                'total_founders': self.collections['founders'].count_documents({}),
                'total_logs': self.collections['logs'].count_documents({}),
                'connection_status': self.connection_status,
                'last_connection': self.last_connection_attempt.isoformat() if self.last_connection_attempt else None
            }

            return stats

        except Exception as e:
            logger.error(f"Error obteniendo estadísticas: {e}")
            return {}

    async def cleanup_old_data(self, days: int = 30, deep_clean: bool = False) -> Dict[str, int]:
        """Limpiar datos antiguos con opción de limpieza profunda"""
        try:
            if not self.connection_status:
                await self.ensure_connection()

            cutoff_date = datetime.now() - timedelta(days=days)
            cutoff_iso = cutoff_date.isoformat()

            results = {}

            # Limpiar logs antiguos
            logs_result = self.collections['logs'].delete_many({
                "timestamp": {"$lt": cutoff_iso}
            })
            results['logs_deleted'] = logs_result.deleted_count

            # Limpiar sesiones expiradas
            sessions_result = self.collections['sessions'].delete_many({
                "expires_at": {"$lt": cutoff_iso}
            })
            results['sessions_deleted'] = sessions_result.deleted_count

            if deep_clean:
                # Limpieza profunda: más criterios de eliminación

                # Limpiar todos los logs más antiguos (más agresivo)
                all_logs_result = self.collections['logs'].delete_many({
                    "timestamp": {"$lt": cutoff_iso}
                })
                results['all_logs_deleted'] = all_logs_result.deleted_count

                # Limpiar usuarios inactivos (criterios más amplios)
                inactive_users_broad = self.collections['users'].delete_many({
                    "$and": [
                        {"premium": False},
                        {"$or": [
                            {"updated_at": {"$lt": cutoff_iso}},
                            {"last_bonus": {"$lt": cutoff_iso}},
                            {"$and": [{"credits": {"$lt": 10}}, {"total_generated": {"$lt": 5}}]}
                        ]}
                    ]
                })
                results['inactive_users_deleted'] = inactive_users_broad.deleted_count

                # Limpiar datos de staff inactivos (solo si es muy antiguo)
                very_old_cutoff = datetime.now() - timedelta(days=days*3)
                old_staff_result = self.collections['staff'].delete_many({
                    "assigned_at": {"$lt": very_old_cutoff.isoformat()}
                })
                results['old_staff_deleted'] = old_staff_result.deleted_count

            else:
                # Limpieza estándar
                inactive_users = self.collections['users'].delete_many({
                    "premium": False,
                    "updated_at": {"$lt": cutoff_iso},
                    "credits": {"$lt": 5}
                })
                results['inactive_users_deleted'] = inactive_users.deleted_count

            logger.info(f"✅ Limpieza {'profunda' if deep_clean else 'estándar'} completada: {results}")
            return results

        except Exception as e:
            logger.error(f"Error en limpieza de datos: {e}")
            return {}

    async def cleanup_specific_collection(self, collection_name: str, filter_criteria: Dict = None, days: int = 30) -> Dict[str, int]:
        """Limpiar una colección específica con criterios personalizados"""
        try:
            if not self.connection_status:
                await self.ensure_connection()

            if collection_name not in self.collections:
                logger.error(f"Colección '{collection_name}' no existe")
                return {}

            collection = self.collections[collection_name]

            # Criterios por defecto basados en fecha
            if filter_criteria is None:
                cutoff_date = datetime.now() - timedelta(days=days)
                cutoff_iso = cutoff_date.isoformat()

                # Criterios por defecto según la colección
                if collection_name == 'logs':
                    filter_criteria = {"timestamp": {"$lt": cutoff_iso}}
                elif collection_name == 'sessions':
                    filter_criteria = {"expires_at": {"$lt": cutoff_iso}}
                elif collection_name == 'users':
                    filter_criteria = {
                        "premium": False,
                        "updated_at": {"$lt": cutoff_iso},
                        "credits": {"$lt": 5}
                    }
                else:
                    # Para otras colecciones, intentar usar timestamp genérico
                    filter_criteria = {"$or": [
                        {"created_at": {"$lt": cutoff_iso}},
                        {"timestamp": {"$lt": cutoff_iso}},
                        {"updated_at": {"$lt": cutoff_iso}}
                    ]}

            # Ejecutar eliminación
            result = collection.delete_many(filter_criteria)

            results = {
                'collection': collection_name,
                'deleted_count': result.deleted_count,
                'criteria_used': str(filter_criteria)
            }

            logger.info(f"✅ Limpieza específica de {collection_name}: {result.deleted_count} documentos eliminados")
            return results

        except Exception as e:
            logger.error(f"Error en limpieza específica de {collection_name}: {e}")
            return {}

    def get_connection_info(self) -> Dict[str, Any]:
        """Información de conexión"""
        return {
            'connected': self.connection_status,
            'database': self.db_name,
            'last_attempt': self.last_connection_attempt.isoformat() if self.last_connection_attempt else None,
            'reconnect_attempts': self.reconnect_attempts,
            'max_attempts': self.max_reconnect_attempts,
            'collections': list(self.collections.keys()) if self.collections else []
        }

    async def restore_from_backup(self, backup_file: str) -> Dict[str, int]:
        """Restaurar datos desde archivo de respaldo"""
        try:
            if not os.path.exists(backup_file):
                raise FileNotFoundError(f"Archivo de respaldo no encontrado: {backup_file}")

            if not self.connection_status:
                await self.ensure_connection()

            with open(backup_file, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)

            results = {}

            # Restaurar usuarios
            if 'users' in backup_data:
                for user_data in backup_data['users']:
                    self.collections['users'].update_one(
                        {"user_id": user_data['user_id']},
                        {"$set": user_data},
                        upsert=True
                    )
                results['users_restored'] = len(backup_data['users'])

            # Restaurar staff
            if 'staff' in backup_data:
                for staff_data in backup_data['staff']:
                    self.collections['staff'].update_one(
                        {"user_id": staff_data['user_id']},
                        {"$set": staff_data},
                        upsert=True
                    )
                results['staff_restored'] = len(backup_data['staff'])

            # Restaurar fundadores
            if 'founders' in backup_data:
                for founder_data in backup_data['founders']:
                    self.collections['founders'].update_one(
                        {"user_id": founder_data['user_id']},
                        {"$set": founder_data},
                        upsert=True
                    )
                results['founders_restored'] = len(backup_data['founders'])

            logger.info(f"✅ Respaldo restaurado exitosamente: {results}")
            return results

        except Exception as e:
            logger.error(f"Error restaurando respaldo: {e}")
            raise e

    async def close_connection(self):
        """Cerrar conexión"""
        try:
            if self.client:
                self.client.close()
                self.connection_status = False
                logger.info("✅ Conexión a MongoDB cerrada")
        except Exception as e:
            logger.error(f"Error cerrando conexión: {e}")

    def extract_links_from_text(self, text: str) -> list:
        """Detectar cualquier tipo de enlace, incluso camuflado"""
        import re

        link_patterns = [
            r'https?://\S+', r'www\.\S+',
            r'\b\w+\.(com|net|org|io|co|me|ly|gg|tv|tk|ml|ga|cf|gl)(/[^\s]*)?',
            r't\.me/\S+', r'telegram\.me/\S+', r'tg://\S+', r'discord\.gg/\S+',
            r'youtu\.be/\S+', r'youtube\.com/\S+', r'bit\.ly/\S+',
            r'tinyurl\.com/\S+', r'[a-zA-Z0-9]{2,}(https?://\S+)',
            r'[a-zA-Z0-9]{2,}(www\.\S+)',
        ]

        links = []
        for pattern in link_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                if isinstance(matches[0], tuple):
                    links.extend(["".join(m) for m in matches])
                else:
                    links.extend(matches)

        return list(set(links))

    def save_deleted_link(self, user_id: str, username: str, chat_id: str, message_text: str):
        """Guardar información de link eliminado"""
        try:
            link_id = str(len(self.deleted_links) + 1).zfill(6)

            self.deleted_links[link_id] = {
                'user_id': user_id,
                'username': username,
                'chat_id': chat_id,
                'message_content': message_text,
                'deleted_at': datetime.now().isoformat(),
                'detected_links': self.extract_links_from_text(message_text)
            }
            return link_id
        except Exception as e:
            logger.error(f"Error guardando link eliminado: {e}")
            return None

    def get_deleted_links_by_user(self, user_id: str) -> list:
        """Obtener historial de links eliminados de un usuario"""
        try:
            user_links = []
            for link_id, data in self.deleted_links.items():
                if data['user_id'] == user_id:
                    user_links.append({
                        'id': link_id,
                        'deleted_at': data['deleted_at'],
                        'links': data['detected_links'],
                        'message': data['message_content'][:100] + '...' if len(data['message_content']) > 100 else data['message_content']
                    })

            # Ordenar por fecha más reciente
            user_links.sort(key=lambda x: x['deleted_at'], reverse=True)
            return user_links
        except Exception as e:
            logger.error(f"Error obteniendo links eliminados: {e}")
            return []

# Función para migrar datos existentes
def migrate_json_to_mongodb_sync(json_file: str = 'bot_data.json'):
    """Migrar datos del archivo JSON a MongoDB (versión sincrónica)"""
    try:
        if not os.path.exists(json_file):
            logger.info("No hay archivo JSON para migrar")
            return

        with open(json_file, 'r') as f:
            data = json.load(f)

        mongo_db = MongoDatabase()

        # Conectar de forma sincrónica usando el cliente directo
        if not mongo_db.connection_url:
            logger.error("No se pudo migrar: MONGODB_URL no configurado")
            return

        try:
            # Crear cliente temporal para migración
            client = MongoClient(
                mongo_db.connection_url,
                serverSelectionTimeoutMS=5000
            )
            client.admin.command('ping')
            db = client[mongo_db.db_name]

            users_data = data.get('users', {})
            migrated_count = 0

            for user_id, user_data in users_data.items():
                user_data['user_id'] = user_id
                db.users.update_one(
                    {"user_id": user_id},
                    {"$set": user_data},
                    upsert=True
                )
                migrated_count += 1

            logger.info(f"✅ Migrados {migrated_count} usuarios a MongoDB")

            # Renombrar archivo original como backup
            backup_name = f"{json_file}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.rename(json_file, backup_name)
            logger.info(f"📁 Archivo original respaldado como: {backup_name}")

            client.close()

        except Exception as e:
            logger.error(f"Error conectando para migración: {e}")

    except Exception as e:
        logger.error(f"Error en migración: {e}")
async def migrate_json_to_mongodb(json_file: str = 'bot_data.json'):
    """Migrar datos del archivo JSON a MongoDB"""
    try:
        if not os.path.exists(json_file):
            logger.info("No hay archivo JSON para migrar")
            return

        with open(json_file, 'r') as f:
            data = json.load(f)

        mongo_db = MongoDatabase()
        await mongo_db.connect()

        if not mongo_db.connection_status:
            logger.error("No se pudo conectar a MongoDB para migración")
            return

        users_data = data.get('users', {})
        migrated_count = 0

        for user_id, user_data in users_data.items():
            user_data['user_id'] = user_id
            mongo_db.collections['users'].update_one(
                {"user_id": user_id},
                {"$set": user_data},
                upsert=True
            )
            migrated_count += 1

        logger.info(f"✅ Migrados {migrated_count} usuarios a MongoDB")

        # Renombrar archivo original como backup
        backup_name = f"{json_file}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.rename(json_file, backup_name)
        logger.info(f"📁 Archivo original respaldado como: {backup_name}")

        await mongo_db.close_connection()

    except Exception as e:
        logger.error(f"Error en migración: {e}")
