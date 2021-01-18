from api.models import UniversityAdmin, DepartmentAdmin, Department, FieldOfStudy


def is_logged_in(func):
    def decorator(*args,**kwargs):
        user = args[2].context.user
        if user.is_anonymous:
            raise Exception('You must be logged to perform this action')
        return func(*args,**kwargs)
    return decorator

def is_university_admin(func):
    def decorator(*args,**kwargs):
        user = args[2].context.user
        try:
            university_admin = UniversityAdmin.objects.get(user=user)
            print(university_admin)
        except UniversityAdmin.DoesNotExist:
            raise Exception('You are not university admin, so you are not authorized to perform this action')
        return func(*args,**kwargs)
    return decorator

def is_department_admin(func):
    def decorator(*args,**kwargs):
        user = args[2].context.user
        try:
            department_admin = DepartmentAdmin.objects.get(user=user)
            print(department_admin)
        except DepartmentAdmin.DoesNotExist:
            raise Exception('You are not department admin, so you are not authorized to perform this action')
        return func(*args,**kwargs)
    return decorator

def is_objects_university_admin(model):
    def decorator(func):
        def wrapper(*args,**kwargs):
            user = args[2].context.user
            try:
                university_admin = UniversityAdmin.objects.get(user=user)
            except UniversityAdmin.DoesNotExist:
                raise Exception('You are not university admin, so you are not authorized to perform this action')
            try:
                obj = model.objects.get(university_admin=university_admin, id=kwargs['id'])
                print(obj)
            except model.DoesNotExist:
                raise Exception('You are not authorized to perform this action, because its out of your scope')
            return func(*args,**kwargs)
        return wrapper
    return decorator

def is_objects_department_admin_by_department_admin(model,lookup='department_admin'):
    def decorator(func):
        def wrapper(*args,**kwargs):
            user = args[2].context.user
            try:
                department_admin = DepartmentAdmin.objects.get(user=user)
                print(department_admin)
            except DepartmentAdmin.DoesNotExist:
                raise Exception('You are not department admin, so you are not authorized to perform this action')
            try:
                obj = model.objects.get(**{lookup : department_admin}, id=kwargs['id'])
                print(obj)
            except model.DoesNotExist:
                raise Exception('You are not authorized to perform this action, you are not the owner')
            return func(*args,**kwargs)
        return wrapper
    return decorator

def is_objects_department_admin_by_department(model, lookup='department'):
    def decorator(func):
        def wrapper(*args,**kwargs):
            user = args[2].context.user
            try:
                department = Department.objects.get(department_admins__user=user)
                print(department)
            except DepartmentAdmin.DoesNotExist:
                raise Exception('You are not department admin, so you are not authorized to perform this action')
            try:
                obj = model.objects.get(**{lookup : department}, id=kwargs[model.__name__.lower()+'_id'])
                print(obj)
            except model.DoesNotExist:
                raise Exception('You are not authorized to perform this action, you are not the owner')
            return func(*args,**kwargs)
        return wrapper
    return decorator

def is_owner(model,lookup='user'):
    def decorator(func):
        def wrapper(*args,**kwargs):
            user = args[2].context.user
            try:
                obj = model.objects.get(**{lookup : user}, id=kwargs[model.__name__.lower()+'_id'])
                print(obj)
            except model.DoesNotExist:
                raise Exception('You are not authorized to perform this action, because its out of your scope')
            return func(*args,**kwargs)
        return wrapper
    return decorator