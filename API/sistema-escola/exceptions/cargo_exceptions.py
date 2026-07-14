class PositionNotFound(Exception):
    """Levantada quando um cargo não é encontrada."""

    pass


class PositionAlreadyExists(Exception):
    """Levantada quando se tenta cadastrar um cargo já cadastrado."""
