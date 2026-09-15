import os
from src.data.anonymizer import anonymize_customer_id


def test_customer_id_anonymization():
    """Vérifie que l'anonymisation masque l'identifiant client tout en étant déterministe."""
    raw_id = "7590-VHVEG"
    anon_1 = anonymize_customer_id(raw_id)
    anon_2 = anonymize_customer_id(raw_id)

    # Doit commencer par ANON-
    assert anon_1.startswith("ANON-")
    # L'identifiant brut ne doit pas figurer dans la chaîne anonymisée
    assert raw_id not in anon_1
    # Déterministe avec le même sel
    assert anon_1 == anon_2


def test_anonymization_with_different_salts():
    """Vérifie que deux sels différents produisent deux hachages différents."""
    raw_id = "7590-VHVEG"

    os.environ["ANONYMIZATION_SALT"] = "salt-alpha"
    hash_a = anonymize_customer_id(raw_id)

    os.environ["ANONYMIZATION_SALT"] = "salt-beta"
    hash_b = anonymize_customer_id(raw_id)

    assert hash_a != hash_b
