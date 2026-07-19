class RoleNotFound(Exception):
    """Levantada quando um cargo não é encontrada."""

    pass


class RoleAlreadyExists(Exception):
    """Levantada quando se tenta cadastrar um cargo já cadastrado."""
