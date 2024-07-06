# core/context_processors.py

def is_autoridad(request):
    if request.user.is_authenticated:
        return {'is_autoridad': request.user.groups.filter(name='autoridad').exists()}
    return {'is_autoridad': False}
