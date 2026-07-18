class UserNotFound(Exception):
    """Levantada quando um usuário não existe."""

    pass


class AccessDenied(Exception):
    """Levantada quando o acesso é insuficiente."""

    pass


class InsufficientPermission(Exception):
    """Levantada quando a permimssão é insuficiente."""

    pass


class EmailAlreadyRegistered(Exception):
    """Levantada quando o email já esta cadastrado."""

    pass
