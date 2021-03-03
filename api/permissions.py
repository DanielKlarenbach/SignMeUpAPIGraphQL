from api.models import UniversityAdmin, DepartmentAdmin, Department


def is_logged_in(info_index=2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            info = args[info_index]
            user = info.context.user
            if user.is_anonymous:
                raise Exception('You must be logged to perform this action')
            return func(*args, **kwargs)

        return wrapper

    return decorator


def is_university_admin(info_index=2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            info = args[info_index]
            university_admin_user = info.context.user
            try:
                university_admin = UniversityAdmin.objects.get(user=university_admin_user)
            except UniversityAdmin.DoesNotExist:
                raise Exception('You are not university admin, so you are not authorized to perform this action')
            return func(*args, **kwargs)

        return wrapper

    return decorator


def is_department_admin(info_index=2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            info = args[info_index]
            department_admin_user = info.context.user
            try:
                department_admin = DepartmentAdmin.objects.get(user=department_admin_user)
            except DepartmentAdmin.DoesNotExist:
                raise Exception('You are not department admin, so you are not authorized to perform this action')
            return func(*args, **kwargs)

        return wrapper

    return decorator


def is_objects_university_admin(model, lookup='university__university_admin', id_kwarg='id', info_index=2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            info = args[info_index]
            university_admin_user = info.context.user
            try:
                university_admin = UniversityAdmin.objects.get(user=university_admin_user)
            except UniversityAdmin.DoesNotExist:
                raise Exception('You are not university admin, so you are not authorized to perform this action')
            try:
                obj = model.objects.get(**{lookup: university_admin}, id=kwargs[id_kwarg])
            except model.DoesNotExist:
                raise Exception(
                    'You are not objects university admin, so you are not authorized to perform this action')
            return func(*args, **kwargs)

        return wrapper

    return decorator


def is_objects_department_admin(model, lookup='department', id_kwarg='id', info_index=2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            info = args[info_index]
            department_admin_user = info.context.user
            try:
                department = Department.objects.get(department_admins__user=department_admin_user)
            except Department.DoesNotExist:
                raise Exception('You are not department admin, so you are not authorized to perform this action')
            try:
                obj = model.objects.get(**{lookup: department}, id=kwargs[id_kwarg])
            except model.DoesNotExist:
                raise Exception(
                    'You are not objects department admin, so you are not authorized to perform this action')
            return func(*args, **kwargs)

        return wrapper

    return decorator


def is_owner(model, lookup='user', id_kwarg='id', info_index=2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            info = args[info_index]
            user = info.context.user
            try:
                obj = model.objects.get(**{lookup: user}, id=kwargs[id_kwarg])
            except model.DoesNotExist:
                raise Exception('You are not objects owner, so you are not authorized to perform this action')
            return func(*args, **kwargs)

        return wrapper

    return decorator
