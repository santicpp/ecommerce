from django.contrib import admin
from .models import Carrito, Categorias, Producto, ProductoCarrito, Nivel

# Register your models here.
admin.site.register(Categorias)
admin.site.register(Producto)
admin.site.register(Carrito)
admin.site.register(ProductoCarrito)
admin.site.register(Nivel)

