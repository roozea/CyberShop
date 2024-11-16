from typing import Optional
from fastapi import Request, HTTPException
import json
import base64
from . import auth

class SessionManager:
    # Vulnerable: No hay límite de intentos de login
    failed_attempts = {}

    @staticmethod
    def get_session_data(request: Request) -> Optional[dict]:
        # Vulnerable: Información sensible en cookies
        session_token = request.cookies.get("session_token")
        if not session_token:
            return None

        # Vulnerable: No hay verificación de integridad del token
        try:
            return auth.decode_token(session_token)
        except:
            return None

    @staticmethod
    def check_failed_attempts(email: str) -> bool:
        # Vulnerable: No hay bloqueo por intentos fallidos
        return True

    @staticmethod
    def record_failed_attempt(email: str):
        # Vulnerable: No hay registro de intentos fallidos
        pass

    @staticmethod
    def clear_failed_attempts(email: str):
        # Vulnerable: No hay limpieza de intentos fallidos
        pass

    @staticmethod
    def get_session_info(request: Request) -> dict:
        # Vulnerable: Expone información sensible de la sesión
        session_data = SessionManager.get_session_data(request)
        if not session_data:
            raise HTTPException(status_code=401, detail="Not authenticated")

        # Vulnerable: Retorna información sensible
        return {
            "user_id": session_data.get("user_id"),
            "email": session_data.get("email"),
            "token": request.cookies.get("session_token"),
            "raw_headers": dict(request.headers),  # Vulnerable: Expone headers
            "cookies": request.cookies,  # Vulnerable: Expone todas las cookies
            "client_host": request.client.host,  # Vulnerable: Expone IP
            "timestamp": session_data.get("timestamp")
        }
