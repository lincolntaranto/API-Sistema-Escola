class ClassroomNotFound(Exception):
    """Levantada quando uma turma não é encontrada."""

    pass


class ClassroomAlreadyExists(Exception):
    """Levantada quando se tenta cadastrar uma turma já cadastrado."""

    pass
