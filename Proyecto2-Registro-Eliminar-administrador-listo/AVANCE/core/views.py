from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


from .models import Produccion, Producto
from django.shortcuts import render
from .forms import ProduccionForm

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
            return render(request, 'core/Listarproyectos.html')
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
           # Redirigir a alguna vista después de guardar, ajustar según tu proyecto
        except Producto.DoesNotExist:
            # Manejar el error si no se encuentra el producto
            pass

    productos = Producto.objects.all()
 
    return render(request, 'core/nuevo_proyecto.html', {'productos': productos})

def modificar_producto(request, id):
    produccion = get_object_or_404(Produccion, id=id)

    if request.method == 'POST':
        formulario = ProduccionForm(request.POST, instance=produccion)
        if formulario.is_valid():
            formulario.save()
            return redirect('ListarProyectos') 
    else:
        formulario = ProduccionForm(instance=produccion)

    return render(request, 'core/modificar.html', {'produccion': produccion, 'form': formulario})




def eliminar_producto(request, id):
    producto = get_object_or_404(Produccion, id=id)
    producto.delete()
    return redirect('ListarProyectos')  