from django import urls
from django.urls import path
from . import views

app_name = "App_Inicio"

urlpatterns = [
    path('', views.index, name='index'),
    path('acercade', views.acercade, name='acercade'),
    path('nuevoproducto', views.nuevoproducto, name='nuevoproducto'),
    path('editar/<int:id>', views.editar_producto, name='editar-producto'),
    path('register', views.register_request, name="register"),
    path('login', views.login_request, name="login"),
    path('logout', views.logout_request, name= "logout"),
    path('detalle/<int:id>', views.detalleproducto, name='detalleproducto'),
    path('categoria/<int:categoria>', views.categorias_filtro, name='categoria'),
    path('busqueda/', views.busqueda, name='resultado_busqueda'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:id>/', views.remove_from_cart, name='remove-from-cart'),
    path('reduce-from-cart/<int:id>/', views.reduce_quantity_item, name='reduce-from-cart'),
    path('clean-cart/', views.clean_cart, name='clean-cart'),
    path('carrito/', views.carrito, name='carrito'),
    path('finalizar-compra/', views.finalizar_compra, name='finalizar-compra'),
]