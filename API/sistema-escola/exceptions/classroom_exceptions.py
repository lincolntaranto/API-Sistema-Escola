class ClassroomNotFound(Exception):
    """Levantada quando uma classroom não é encontrada."""

    pass


class ClassroomAlreadyExists(Exception):
    """Levantada quando se tenta cadastrar uma classroom já cadastrado."""

    pass
