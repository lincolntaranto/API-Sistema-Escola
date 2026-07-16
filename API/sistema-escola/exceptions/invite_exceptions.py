class InvalidInvite(Exception):
    """Levantada quando um convite não é valido"""

    pass


class UsedInvitation(Exception):
    """Levantada quando o convite já foi usado"""

    pass
