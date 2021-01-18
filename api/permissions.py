from api.models import UniversityAdmin, DepartmentAdmin, Department, FieldOfStudy


def is_logged_in(func):
    def decorator(*args,**kwargs):
        info = args[2]
        user = info.context.user
        if user.is_anonymous:
            raise Exception('You must be logged to perform this action')
        return func(*args,**kwargs)
    return decorator

def is_university_admin(func):
    def decorator(*args,**kwargs):
        info = args[2]
        university_admin_user = info.context.user
        try:
            university_admin = UniversityAdmin.objects.get(user=university_admin_user)
        except UniversityAdmin.DoesNotExist:
            raise Exception('You are not university admin, so you are not authorized to perform this action')
        return func(*args,**kwargs)
    return decorator

def is_department_admin(func):
    def decorator(*args,**kwargs):
        info = args[2]
        department_admin_user = info.context.user
        try:
            department_admin = DepartmentAdmin.objects.get(user=department_admin_user)
        except DepartmentAdmin.DoesNotExist:
            raise Exception('You are not department admin, so you are not authorized to perform this action')
        return func(*args,**kwargs)
    return decorator

def is_objects_university_admin(model,lookup='university_admin', id_kwarg='id'):
    def decorator(func):
        def wrapper(*args,**kwargs):
            info = args[2]
            university_admin_user = info.context.user
            try:
                university_admin = UniversityAdmin.objects.get(user=university_admin_user)
            except UniversityAdmin.DoesNotExist:
                raise Exception('You are not university admin, so you are not authorized to perform this action')
            try:
                obj = model.objects.get(**{lookup : university_admin}, id=kwargs[id_kwarg])
            except model.DoesNotExist:
                raise Exception('You are not authorized to perform this action, because its out of your scope')
            return func(*args,**kwargs)
        return wrapper
    return decorator

def is_objects_department_admin(model, lookup='department', id_kwarg='id'):
    def decorator(func):
        def wrapper(*args,**kwargs):
            info = args[2]
            department_admin_user = info.context.user
            try:
                department = Department.objects.get(department_admins__user=department_admin_user)
            except Department.DoesNotExist:
                raise Exception('You are not department admin, so you are not authorized to perform this action')
            try:
                obj = model.objects.get(**{lookup : department}, id=kwargs[id_kwarg])
            except model.DoesNotExist:
                raise Exception('You are not authorized to perform this action, you are not the owner')
            return func(*args,**kwargs)
        return wrapper
    return decorator

def is_owner(model,lookup='user',id_kwarg='id'):
    def decorator(func):
        def wrapper(*args,**kwargs):
            info = args[2]
            user = info.context.user
            try:
                obj = model.objects.get(**{lookup : user}, id=kwargs[id_kwarg])
                print(obj)
            except model.DoesNotExist:
                raise Exception('You are not authorized to perform this action, because its out of your scope')
            return func(*args,**kwargs)
        return wrapper
    return decorator