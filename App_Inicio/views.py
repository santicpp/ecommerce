from django.contrib.auth import login, authenticate, logout
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm
from .forms import FormNuevoProducto, NewUserForm
from django.contrib import messages
from .models import Carrito, Categorias, Producto, ProductoCarrito, Nivel
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.

def index(request):
	ultimosTres = Producto.objects.all().order_by('-id')[:3]
	ultimosDiez = Producto.objects.all().order_by('-id')[3:10]
	return render(request, 'web/inicio.html', context={'ultimosTres': ultimosTres, 'ultimosDiez': ultimosDiez})

def acercade(request):
    return render(request, 'web/acercade.html')
    
@login_required(login_url='App_Inicio:register')
def nuevoproducto(request):
    form = FormNuevoProducto(request.POST, request.FILES)

    if form.is_valid():
        form.save()
        messages.success(request, "Producto agregado exitosamente!" )

    return render(request, 'web/nuevoproducto.html', {
        "form": FormNuevoProducto()
    })

@login_required(login_url='App_Inicio:register')
def editar_producto(request, id):
    instance = get_object_or_404(Producto, id=id)
    form = FormNuevoProducto(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        messages.success(request, "Producto editado exitosamente!" )
    return render(request, 'web/editarproducto.html', {"form": form, "id":id})

#registro de usuarios
def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            Nivel(usuario=user).save()
            Carrito(usuario=user).save()
            return redirect("/")
        messages.error(request, "El registro contiene información invalida.")
    form = NewUserForm
    return render (request=request, template_name="web/register.html", context={"register_form":form})

#login de usuario
def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect("/")
			else:
				messages.error(request,"Nombre de usuario o contraseña incorrectos.")
		else:
			messages.error(request,"Nombre de usuario o contraseña incorrectos.")
	form = AuthenticationForm()
	return render(request=request, template_name="web/login.html", context={"login_form":form})

@login_required(login_url='App_Inicio:register')
def logout_request(request):
	logout(request)
	return redirect("/")

def detalleproducto(request, id):
	producto = Producto.objects.get(id=id)
	context = {'producto': producto}
	return render(request, 'web/detalle.html', context)

def categorias_filtro(request, categoria):
	productoscat = Producto.objects.filter(categoria=categoria).order_by('-id')
	productoscantidad = Producto.objects.filter(categoria=categoria).count()
	categoriatitle = Categorias.objects.get(id=categoria)
	paginator = Paginator(productoscat, 5)
	numero_pagina = request.GET.get('page')
	categoria_pag = paginator.get_page(numero_pagina)
	context = {'categoria_pag': categoria_pag, 'categoriatitle':categoriatitle, 'productoscantidad': productoscantidad}
	return render(request, 'web/categoria.html', context)

def busqueda(request):
    busqueda = request.GET.get('query')
    productos = Producto.objects.filter(Q(titulo__icontains=busqueda) | Q(descripcion__icontains=busqueda) | Q(categoria__descripcion__icontains=busqueda))
    context = {'productobusqueda': productos, 'busqueda':busqueda}
    return render(request, 'web/resultados.html', context)

@login_required(login_url='App_Inicio:register')
def add_to_cart(request, id):
    item = get_object_or_404(Producto, id=id)
    order_item, created = ProductoCarrito.objects.get_or_create(
        item = item,
        user = request.user,
        ordered = False
    )
    order_qs = Carrito.objects.filter(usuario=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__id=item.id).exists():
            order_item.quantity += 1
            order_item.save()
            order_quantity = order.get_total_items()
            return HttpResponse(order_quantity)
        else:
            order.items.add(order_item)
            order_quantity = order.get_total_items()
            return HttpResponse(order_quantity)
    else:
        order = Carrito.objects.create(usuario=request.user)
        order.items.add(order_item)
        order_quantity = order.get_total_items()
        return HttpResponse(order_quantity)

@login_required(login_url='App_Inicio:register')
def remove_from_cart(request, id):
    item = get_object_or_404(Producto, id=id )
    order_qs = Carrito.objects.filter(
        usuario=request.user, 
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__id=item.id).exists():
            order_item = ProductoCarrito.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order_item.delete()
            return redirect("App_Inicio:carrito")
        else:
            return redirect("App_Inicio:carrito")
    else:
        return redirect("App_Inicio:carrito")

@login_required(login_url='/accounts/login/')
def reduce_quantity_item(request, id):
    item = get_object_or_404(Producto, id=id )
    order_qs = Carrito.objects.filter(
        usuario = request.user, 
        ordered = False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__id=item.id).exists() :
            order_item = ProductoCarrito.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()
            return redirect("App_Inicio:carrito")
        else:
            return redirect("App_Inicio:carrito")
    else:
        return redirect("App_Inicio:carrito")

@login_required(login_url='App_Inicio:register')
def clean_cart(request):
    order = Carrito.objects.get(usuario=request.user, ordered=False)
    order_items = order.items.all()
    for item in order_items:
        item.delete()
        order.save()
    return redirect("App_Inicio:carrito")

@login_required(login_url='App_Inicio:register')
def carrito(request):
    order = Carrito.objects.get(usuario=request.user, ordered=False)
    finalorder = order.items.all()
    quantity = finalorder.count()
    if quantity == 0:
        products = False
    else:
        products = True
    nivel = Nivel.objects.get(usuario=request.user)
    get_descuentopercentage = nivel.get_user_level() / 100
    precioparcial = order.get_total_price()
    get_descuento = float(precioparcial) * float(get_descuentopercentage)
    preciofinal = float(precioparcial) - get_descuento
    context = {'finalorder' : finalorder, 'preciofinal': preciofinal, 'products': products, 'get_descuento':get_descuento, 'precioparcial': precioparcial}
    return render(request, 'web/carrito.html', context)

@login_required(login_url='App_Inicio:register')
def finalizar_compra(request):
    userlvlmodel = Nivel.objects.get(usuario=request.user)
    order = Carrito.objects.get(usuario=request.user, ordered=False)
    preciofinal = order.get_total_price()
    userlvlmodel.experiencia += preciofinal
    order_items = order.items.all()
    for item in order_items:
        item.delete()
        order.save()
    userlvlmodel.save()
    return redirect("App_Inicio:carrito")
