"""app/utils/id_generator.py"""

import uuid

def generate_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"