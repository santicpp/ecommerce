from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Categorias(models.Model):
    descripcion = models.CharField(max_length=64)
    def __str__(self):
        return self.descripcion

class Producto(models.Model):
    titulo = models.CharField(max_length=64)
    imagen = models.ImageField(upload_to="images")
    descripcion = models.CharField(max_length=1500, blank = True)
    precio = models.DecimalField(max_digits = 50, decimal_places = 2)
    categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.titulo} de la categoria {self.categoria}"

class ProductoCarrito(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item  = models.ForeignKey(Producto, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.item.titulo}"

    def get_total_item_price(self):
        return self.quantity * self.item.precio

class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(ProductoCarrito)
    precio = models.DecimalField(max_digits = 999999, decimal_places = 2, default=0)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.usuario.username} y {self.items.count()}"
    
    def get_total_items(self):
        totalitems = 0
        for order_item in self.items.all():
            totalitems += order_item.quantity
        return totalitems

    def get_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total

class Nivel(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    experiencia = models.DecimalField(max_digits = 999999, decimal_places = 2, default=0)

    def __str__(self):
        return f"{self.usuario.username} tiene {self.experiencia} puntos de experiencia!"

    def get_user_level(self):
        levels = [15000, 37500, 80000, 150000, 400000, 750000, 1250000, 2000000, 3500000, 5000000]
        lvl = len([x for x in levels if self.experiencia > x])
        return lvl

    def get_user_percentage(self):
        levels = [15000, 37500, 80000, 150000, 400000, 750000, 1250000, 2000000, 3500000, 5000000]
        lvl = len([x for x in levels if self.experiencia > x])
        if lvl == 10:
            get_experience = 100
        else:
            if lvl == 0:
                dif_experiencia = levels[lvl]
                get_experience = self.experiencia / dif_experiencia * 100
            else:
                dif_experiencia = levels[lvl] - levels[lvl - 1]
                get_experience = (self.experiencia - levels[lvl - 1]) / dif_experiencia * 100
        get_experience_int = int(get_experience)
        return get_experience_int

    def get_user_exp(self):
        levels = [15000, 37500, 80000, 150000, 400000, 750000, 1250000, 2000000, 3500000, 5000000]
        lvl = len([x for x in levels if self.experiencia > x])
        if lvl == 0:
            dif_experiencia = levels[lvl]
            get_experience = dif_experiencia - self.experiencia
        else:
            dif_experiencia = levels[lvl] - levels[lvl - 1]
            get_experience = (self.experiencia - levels[lvl - 1]) - dif_experiencia
        get_experience_int = int(get_experience)
        return get_experience_int