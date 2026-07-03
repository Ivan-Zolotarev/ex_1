def is_valid_email(email: str) -> bool:
    """Простая проверка email для учебного проекта."""
    if not email:
        return False

    if "@" not in email:
        return False

    local_part, _, domain = email.partition("@")
    if not local_part or not domain:
        return False

    return "." in domain


def is_not_empty(value: str) -> bool:
    """Проверяет, что строка не пустая."""
    return bool(value and value.strip())
