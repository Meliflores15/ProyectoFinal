from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Produccion, Producto
from .forms import ProduccionForm
from django.utils import timezone

def index(request):
    return render(request,'core/index.html')


@login_required
def listar_proyectos(request):
    if 'mis_registros' in request.GET:
        registros = Produccion.objects.filter(operador=request.user)
    else:
        registros = Produccion.objects.all()
    
    return render(request, 'core/listarProyectos.html', {'listado': registros})


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
            return render(request, 'core/index.html')
    else:
        return render(request, 'core/iniciarsesion.html')
    
@login_required 
def logout_view(request):
        logout(request)
        return redirect('/iniciarsesion')



def agregar_produccion(request):
    if request.method == 'POST':
        agregar_producto_id = request.POST['producto']
        LitrosProducidos = request.POST['litros_producido']
        fecha = request.POST['fecha_produccion']
        turnos = request.POST['turno']  
        hora=request.POST['hora_registro']
        operador = request.user

        try:
            agregar_producto = Producto.objects.get(id=agregar_producto_id)

            mensaje = Produccion()
            mensaje.producto = agregar_producto
            mensaje.Litros_producido = LitrosProducidos
            mensaje.fecha_produccion = fecha
            mensaje.turno = turnos
            mensaje.hora_registro=hora
            mensaje.operador = operador

            mensaje.save()
        
        except Producto.DoesNotExist:
            pass

    productos = Producto.objects.all()
 
    return render(request, 'core/nuevo_proyecto.html', {'productos': productos})

@login_required
def modificar_producto(request, id):
    produccion = get_object_or_404(Produccion, id=id)

    # Aca verificamos el usuario logueado
    if produccion.operador != request.user:
        return HttpResponseForbidden("No tienes permiso para modificar este registro.")

    if request.method == 'POST':
        form = ProduccionForm(request.POST, instance=produccion)
        if form.is_valid():
            produccion = form.save(commit=False)
            produccion.modificado_por = request.user
            produccion.fecha_modificacion = timezone.now()
            produccion.save()
            return redirect('ListarProyectos')
    else:
        form = ProduccionForm(instance=produccion)
    
    return render(request, 'core/modificar.html', {'form': form, 'produccion': produccion})

@login_required
def eliminar_producto(request, id):
    producto = get_object_or_404(Produccion, id=id)
    producto.delete()
    return redirect('ListarProyectos')  

@login_required
def fiscalizadora(request):
    is_autoridad = request.user.groups.filter(name='autoridad').exists()
    if is_autoridad:
        return render(request, 'core/autoridad.html', {'is_autoridad': is_autoridad})
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")