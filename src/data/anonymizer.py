import hashlib
import hmac
import os
from typing import Optional


def get_salt() -> bytes:
    """Récupère le sel d'anonymisation depuis l'environnement."""
    salt_str = os.getenv("ANONYMIZATION_SALT", "default-churnscope-salt-2026-dpia1")
    return salt_str.encode("utf-8")


def anonymize_customer_id(customer_id: Optional[str], length: int = 12) -> str:
    """
    Anonymise un identifiant client avec HMAC-SHA256 pour respecter la conformité RGPD.

    Permet de conserver la jointure analytique sans exposer l'identifiant brut.
    """
    if not customer_id or not isinstance(customer_id, str):
        return "ANON-UNKNOWN"

    salt = get_salt()
    digest = hmac.new(
        salt, customer_id.strip().encode("utf-8"), hashlib.sha256
    ).hexdigest()
    return f"ANON-{digest[:length].upper()}"
