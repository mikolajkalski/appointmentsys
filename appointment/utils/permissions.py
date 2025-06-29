

def check_entity_ownership(user, entity):

    return entity.is_owner(user.pk) or user.is_superuser


def check_extensive_permissions(staff_user_id, user, entity):

    if (staff_user_id and int(staff_user_id) == user.pk) or user.is_superuser:
        if entity:
            return check_entity_ownership(user, entity)
        else:
            return True
    return False


def check_permissions(staff_user_id, user):

    if (staff_user_id and int(staff_user_id) == user.pk) or user.is_superuser:
        return True
    return False


def has_permission_to_delete_appointment(user, appointment):

    return check_extensive_permissions(appointment.get_staff_member().user_id, user, appointment)
