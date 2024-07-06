from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


from .models import Produccion, Producto
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request,'core/index.html')


def listar(request):
        lista_proyectos= Produccion.objects.all()
        data={
             "lista_proyectos": lista_proyectos,
        } 
        return render(request,'core/ListarProyectos.html',data)

@login_required
def home_view(request):
    return render(request, 'core/base.html')

  
def iniciarsesion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request=request,username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/ListarProyectos')
        else:
            return render(request, 'core/Listarproyectos.html')
    else:
        return render(request, 'core/iniciarsesion.html')
    
@login_required 
def logout_view(request):
        logout(request)
        return redirect('/iniciarsesion')

def nuevo_proyecto(request):
    return render(request, 'core/nuevo_proyecto.html')

from django.shortcuts import render, redirect
from .models import Produccion, Producto
from django.contrib.auth.models import User

def agregar_produccion(request):
    if request.method == 'POST':
        agregar_producto_id = request.POST['producto']
        LitrosProducidos = request.POST['litros_producido']
        fecha = request.POST['fecha_produccion']
        turnos = request.POST['turno']  
        hora_registros=request.POST['hora_registro']
        operador = request.user

        try:
            agregar_producto = Producto.objects.get(id=agregar_producto_id)

            mensaje = Produccion()
            mensaje.producto = agregar_producto
            mensaje.Litros_producido = LitrosProducidos
            mensaje.fecha_produccion = fecha
            mensaje.turno = turnos
            mensaje.hora_registro=hora_registros
            mensaje.operador = operador

            mensaje.save()
           # Redirigir a alguna vista después de guardar, ajustar según tu proyecto
        except Producto.DoesNotExist:
            # Manejar el error si no se encuentra el producto
            pass

    productos = Producto.objects.all()
    return render(request, 'core/nuevo_proyecto.html', {'productos': productos})
