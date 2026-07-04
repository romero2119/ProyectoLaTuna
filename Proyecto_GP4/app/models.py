from django.db import models
from django.core.validators import MinValueValidator,  MaxValueValidator
from django.core.exceptions import ValidationError
from datetime import datetime
from decimal import Decimal
from django.db.models import Sum
from django.core.validators import RegexValidator
from datetime import datetime
from django.utils import timezone
from usuarios.models import *


# Create your models here.
'''class Usuario(models.Model):

    ROL_OPCIONES = (
        ('admin', 'Administrador'),
        ('empleado', 'Empleado'),
        ('proveedor', 'Proveedor'),
    )

    TIPO_DE_DOCUMENTO = [
        ("CC", "Cédula de Ciudadanía"),
        ("TI", "Tarjeta de Identidad"),
        ("CE", "Cédula de Extranjería"),
        ("Pasaporte", "Pasaporte"),
    ]

    id_usuario = models.AutoField(primary_key=True)
    tipo_de_documento = models.CharField(max_length=20, choices=TIPO_DE_DOCUMENTO,null=True)
    numero_documento = models.CharField(max_length=15, unique=True, null=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo_electronico = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=128)
    rol = models.CharField(max_length=20, choices=ROL_OPCIONES)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        db_table = "usuario"

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
'''
#Categorias Fuertes

class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)

    TIPO_DE_DOCUMENTO = [
        ("CC", "Cédula de Ciudadanía"),
        ("NIT", "NIT"),
        ("CE", "Cédula de Extranjería"),
        ("Pasaporte", "Pasaporte"),
    ]

    tipo_de_documento = models.CharField(max_length=20, choices=TIPO_DE_DOCUMENTO)
    numero_documento = models.CharField(max_length=20, unique=True)
    nombre_proveedor = models.CharField(max_length=20)
    telefono = models.CharField(max_length=15)
    correo_electronico = models.EmailField(unique=True)
    direccion = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        db_table = "proveedor"

    def __str__(self):
        return self.nombre_proveedor

class Producto(models.Model):
    UNIDAD_OPCIONES = [
        ("", "Seleccione una unidad 🡇"),
        ("kg", "Kilogramo (kg)"),
        ("g", "Gramo (g)"),
        ("l", "Litro (L)"),
        ("ml", "Mililitro (ml)"),
        ("m", "Metro (m)"),
        ("cm", "Centímetro (cm)"),
    ]

    id_producto = models.AutoField(primary_key=True)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    unidad_de_medida = models.CharField(max_length=20, choices=UNIDAD_OPCIONES, default="unidad")
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    fecha_ingreso = models.DateField(default=timezone.now)
    fecha_vencimiento = models.DateField()
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    class Meta:
        db_table = "producto"

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "producto"

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    ESTADO = [
        ("activo", "Activo"),
        ("inactivo", "Inactivo"),
    ]

    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADO, default="activo")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        db_table = "categoria"

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)

    TIPO_DE_DOCUMENTO = [
        ("CC", "Cédula de Ciudadanía"),
        ("TI", "Tarjeta de Identidad"),
        ("CE", "Cédula de Extranjería"),
        ("Pasaporte", "Pasaporte"),
    ]
    
    TIPO_CLIENTE = [
        ("Regular", "Regular"),
        ("VIP", "VIP"),
        ("Frecuente", "Frecuente"),
    ]

    tipo_de_documento = models.CharField(max_length=20, choices=TIPO_DE_DOCUMENTO, null=True)
    numero_documento = models.CharField(max_length=15, unique=True, null=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15)
    correo_electronico = models.EmailField(unique=True)
    direccion = models.CharField(max_length=100)
    tipo_cliente = models.CharField(max_length=20, choices=TIPO_CLIENTE, default="Regular")
    

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        db_table = 'cliente'

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Factura(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=50, unique=True, blank=True, null=True)
    venta = models.ForeignKey('Venta', on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)
    observacion = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # ← primero guardamos para obtener el id
        if not self.codigo:            # ← solo si no tiene código aún
            self.codigo = f'FACT-{self.id:05d}'
            Factura.objects.filter(pk=self.pk).update(codigo=self.codigo)  # ← update directo, sin doble save

    class Meta:
        db_table = "factura"
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"

    def __str__(self):
        return f"{self.codigo} - Venta {self.venta.id_venta}"
    
#modelos debiles

class Compra(models.Model):

    ESTADO_PAGO = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('anticipado', 'Pagado anticipadamente'),
    ]
    id_compra = models.AutoField(primary_key=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)
    insumo = models.ForeignKey( 'insumo', on_delete=models.CASCADE, null=True, blank=True)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_compra = models.DateTimeField(auto_now=True)

    estado_pago = models.CharField(
        max_length=20,
        choices=ESTADO_PAGO,
        default='pendiente'
    )

    total_compra = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"
        db_table = "compra"

    def save(self, *args, **kwargs):
        self.total_compra = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Compra #{self.id_compra} - {self.proveedor} - {self.producto}"
    @property
    def articulo(self):
        if self.producto:
            return self.producto.nombre
        elif self.insumo:
            return self.insumo.nombre
        return "Sin artículo"

class Mesa(models.Model):
    id_mesa = models.AutoField(primary_key=True)
    numero_mesa = models.IntegerField(unique=True, validators=[MinValueValidator(1), MaxValueValidator(10)])
    estado = models.CharField(max_length=20)

    ESTADO = [
        ("Disponible", "Disponible"),
        ("No disponible", "No disponible"),
    ]

    estado = models.CharField(max_length=15, choices=ESTADO, default="Disponible")

    class Meta:
        verbose_name = "Mesa"
        verbose_name_plural = "Mesas"
        db_table = 'mesa'

    def __str__(self):
        return f"Mesa {self.numero_mesa}"
    
class Plato(models.Model):
    id_plato = models.AutoField(primary_key=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, unique=True, null=True)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='platos/', null=True, blank=True)
    class Meta:
        verbose_name = "Plato"
        verbose_name_plural = "Platos"
        db_table = "plato"

    def __str__(self):
        return self.nombre

     
class Pedido(models.Model):

    ESTADO = [
        ("Preparación", "Preparación"),
        ("Entregado", "Entregado"),
    ]

    id_pedido = models.AutoField(primary_key=True)
    mesa = models.ForeignKey('Mesa', on_delete=models.CASCADE, verbose_name="Mesa")
    usuario = models.ForeignKey('usuarios.Usuario',on_delete=models.CASCADE,verbose_name="Empleado")
    fecha_hora = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora")
    estado = models.CharField(max_length=15, choices=ESTADO, default="Preparación", verbose_name="Estado")
    pago = models.BooleanField(default=False, verbose_name="Pagado")

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        db_table = 'pedido' 
        ordering = ['id_pedido']

    def __str__(self):
        return f"Pedido #{self.id_pedido} - Mesa {self.mesa.numero_mesa} - {self.estado}"

    @property
    def total_platos(self):
        """Suma el subtotal de todos los platos: cantidad × precio de la BD."""
        return sum(detalle.subtotal for detalle in self.detalle_platos.all())

    @property
    def total_productos(self):
        #Suma el subtotal de todos los productos: cantidad × precio de la BD.
        return sum(detalle.subtotal for detalle in self.detalle_productos.all())

    @property
    def total(self):
        #Total general del pedido = total platos + total productos.
        return self.total_platos + self.total_productos


class DetallePlato(models.Model):

    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="detalle_platos", verbose_name="Pedido")
    plato = models.ForeignKey('Plato', on_delete=models.CASCADE, verbose_name="Plato")
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name="Cantidad")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Precio Unitario")

    class Meta:
        verbose_name = "Detalle de Plato"
        verbose_name_plural = "Detalles de Platos"
        unique_together = ('pedido', 'plato')

    def __str__(self):
        return f"{self.plato.nombre} x {self.cantidad}"

    @property
    def subtotal(self):
        """Usa el precio guardado al crear el pedido, o calcula desde BD si no existe."""
        precio = self.precio_unitario or self.plato.precio
        return self.cantidad * precio

class DetallePedido(models.Model):

    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="detalle_productos", verbose_name="Pedido")
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE, verbose_name="Producto")
    cantidad = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name="Cantidad")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Precio Unitario")

    class Meta:
        verbose_name = "Detalle de Producto"
        verbose_name_plural = "Detalles de Productos"
        db_table = "detalle_pedido" 
        unique_together = ('pedido', 'producto')

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"

    @property
    def subtotal(self):
        """Usa el precio guardado al crear el pedido, o calcula desde BD si no existe."""
        precio = self.precio_unitario or self.producto.precio
        return self.cantidad * precio
            
class Comanda(models.Model):

    id_comanda = models.AutoField(primary_key=True)

    pedido = models.OneToOneField(
        Pedido,
        on_delete=models.CASCADE,
        related_name="comanda"
    )

    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE)

    fecha_hora = models.DateTimeField(auto_now_add=True)

    ESTADO = [
        ("Preparación", "Preparación"),
        ("Entregado", "Entregado"),
    ]

    estado = models.CharField(max_length=15, choices=ESTADO, default="Preparación")

    class Meta:
        db_table = "comanda"
        ordering = ['-fecha_hora']

    def __str__(self):
        return f"Comanda #{self.id_comanda}"

class Menu(models.Model):
    id_menu = models.AutoField(primary_key=True)

    plato = models.ForeignKey(Plato, on_delete=models.CASCADE, null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        if self.plato:
            return self.plato.nombre
        elif self.producto:
            return self.producto.nombre
        return "Menu vacío"

    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menus"
        db_table = "menu"

class insumo(models.Model):

    UNIDADES_MEDIDA = [
        ("kg", "Kilogramo (kg)"),
        ("g", "Gramo (g)"),
        ("l", "Litro (L)"),
        ("ml", "Mililitro (ml)"),
        ("m", "Metro (m)"),
        ("cm", "Centímetro (cm)"),
        ("unidad", "Unidad"),
    ]

    id_insumo = models.AutoField(primary_key=True)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=100)
    unidad = models.CharField(max_length=20, choices=UNIDADES_MEDIDA, default="unidad")
    valor = models.DecimalField(max_digits=20, decimal_places=2, error_messages={'max_digits': 'El valor es demasiado alto.'})
    stock = models.PositiveIntegerField(default=0)
    fecha_ingreso = models.DateField(auto_now_add=True)          # ← automática al crear
    fecha_vencimiento = models.DateField(null=True, blank=True)  # ← la ingresa el usuario

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'insumo'
        verbose_name_plural = 'insumos'
        db_table = 'insumo'

class Receta(models.Model):
    plato = models.OneToOneField(Plato, on_delete=models.CASCADE, related_name='recetas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Receta de {self.plato.nombre}"
    @property
    def costo_total(self):
        return sum(
            detalle.cantidad * detalle.insumo.valor
            for detalle in self.detalles.all()
        )

    class Meta:
        db_table = 'receta'
        verbose_name = 'Receta'
        verbose_name_plural = 'Recetas'

class DetalleReceta(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='detalles')
    insumo = models.ForeignKey(insumo, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.insumo.nombre} - {self.cantidad}"

    class Meta:
        db_table = 'detalle_receta'
        unique_together = ('receta', 'insumo')
        verbose_name = 'Detalle Receta'
        verbose_name_plural = 'Detalles Recetas'

class Notificacion(models.Model):

    id_notificacion = models.AutoField(primary_key=True)

    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE, null=True, blank=True)

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)
    insumo = models.ForeignKey(insumo, on_delete=models.CASCADE, null=True, blank=True)

    tipo_notificacion = models.CharField(max_length=100, db_index=True)
    mensaje = models.TextField()

    leido = models.BooleanField(default=False)

    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo_notificacion} - {self.mensaje}"

    class Meta:
        verbose_name = "notificacion"
        verbose_name_plural = "notificaciones"
        db_table = "notificacion"

class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=50, unique=True, blank=True, null=True)
    pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE)
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_venta = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)  # ← añadir
    def save(self, *arg, **kwargs):
        if not self.pk:
            super().save(*arg, **kwargs)  # Guardarmos para obtener el id
            self.codigo = f'VEN-set{self.pk:05d}'
            super().save(*arg, **kwargs)
    class Meta:
        db_table = "venta"

    def __str__(self):
        return f"Venta #{self.id_venta} - Pedido {self.pedido.id_pedido}"


class Pago(models.Model):
    METODOS = [
        ('Efectivo', 'Efectivo'),
        ('Tarjeta', 'Tarjeta'),
        ('Transferencia', 'Transferencia'),
    ]
    id_pago = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=50, unique=True, blank=True, null=True)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    metodo_pago = models.CharField(max_length=20, choices=METODOS)
    factura = models.CharField(max_length=50, blank=True, null=True)
    activo = models.BooleanField(default=True)  # ← añadir
    referencia = models.CharField(max_length=100, blank=True, null=True)  # Para transferencias
    comprobante = models.ImageField(upload_to='comprobantes/', blank=True, null=True)  # Para adjuntar comprobante de pago

    class Meta:
        db_table = "pago"
    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
            self.codigo = f'PAGO-{self.pk:05d}'
            Pago.objects.filter(pk=self.pk).update(codigo=self.codigo)  # igual que Factura
        else:
            super().save(*args, **kwargs)  # ← cuando actualiza, guarda normal