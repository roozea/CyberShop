from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import base64
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class VulnerableAuthMiddleware(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        if not credentials:
            raise HTTPException(status_code=403, detail="No se proporcionó token de autenticación")

        token = credentials.credentials

        # Vulnerable: Log de tokens sin sanitización
        logger.info(f"Token recibido: {token}")

        try:
            # Vulnerable: No hay verificación de integridad
            decoded = base64.b64decode(token.encode()).decode()
            payload = json.loads(decoded)

            # Vulnerable: No se verifica la expiración del token
            if "timestamp" in payload:
                # Vulnerable: Se usa un timestamp simple sin validación
                request.state.user = payload
                return payload

        except Exception as e:
            # Vulnerable: Log de errores con información sensible
            logger.error(f"Error al decodificar token: {str(e)}, Token: {token}")
            raise HTTPException(status_code=403, detail="Token inválido")

        raise HTTPException(status_code=403, detail="Token inválido")
