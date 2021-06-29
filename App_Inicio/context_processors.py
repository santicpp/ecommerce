from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Categorias, Producto, Carrito, Nivel

def add_variable_to_context(request):
    
    if request.user.is_authenticated:
        order = Carrito.objects.get(usuario=request.user, ordered=False)
        productos_carrito = order.get_total_items()
        userlvlmodel = Nivel.objects.get(usuario=request.user)
        userexp = userlvlmodel.experiencia
        userlvl = userlvlmodel.get_user_level()
        userexppercentage = userlvlmodel.get_user_percentage()
        return {
        'categorias': Categorias.objects.all().order_by('descripcion'),
        'productos': Producto.objects.count(),
        'productoscarrito': productos_carrito,
        'userexp': userexp,
        'userlvl': userlvl,
        'userexppercentage': userexppercentage
        }
    else:
        return {
        'categorias': Categorias.objects.all().order_by('descripcion'),
        'productos': Producto.objects.count(),
        }