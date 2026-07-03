def is_valid_email(email: str) -> bool:
    """Простая проверка email для учебного проекта."""
    if not email:
        return False

    if "@" not in email:
        return False

    domain = email.split("@")[-1]
    return "." in domain


def is_not_empty(value: str) -> bool:
    """Проверяет, что строка не пустая."""
    return bool(value and value.strip())
