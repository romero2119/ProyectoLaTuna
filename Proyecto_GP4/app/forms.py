from dataclasses import field
from django.forms import ModelForm, inlineformset_factory
from app.models import *
from django import forms 
from django.forms import inlineformset_factory
import re
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError



class ClienteForm(ModelForm):

    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'numero_documento': forms.TextInput(attrs={
                'placeholder': 'Ingrese la cédula del cliente'}),
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Ingrese el nombre del cliente'
            }),
            'apellido': forms.TextInput(attrs={
                'placeholder': 'Ingrese el apellido del cliente'
            }),
            'telefono': forms.TextInput(attrs={
                'placeholder': 'Ingrese el teléfono del cliente'
            }),
            'correo_electronico': forms.EmailInput(attrs={
                'placeholder': 'Ingrese el correo electrónico del cliente'
            }),
            'direccion': forms.TextInput(attrs={
                'placeholder': 'Ingrese la dirección del cliente'}),
            'tipo_cliente': forms.Select(attrs={
                'placeholder': 'Seleccione el tipo de cliente'}),
        }
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()

        if not nombre:
            raise forms.ValidationError("El nombre no puede estar vacío.")

        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre):
            raise forms.ValidationError("El nombre solo debe contener letras.")

        return nombre
    
    def clean_apellido(self):
        apellido = self.cleaned_data.get('apellido', '').strip()

        if not apellido:
            raise forms.ValidationError("El apellido no puede estar vacío.")


        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', apellido):
            raise forms.ValidationError("El apellido solo debe contener letras.")

        return apellido


    def clean_correo_electronico(self):
        correo = self.cleaned_data.get('correo_electronico')

        if not re.match(r'^[a-zA-Z][a-zA-Z0-9]*@(gmail|hotmail)\.com$', correo):
            raise forms.ValidationError(
                "El correo debe iniciar con una letra y solo puede contener "
                "letras y números antes del '@', y debe ser @gmail.com o @hotmail.com."
            )

        return correo


    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')

        if not telefono.isdigit():
            raise forms.ValidationError("El teléfono solo debe contener números.")

        if len(telefono) != 10:
            raise forms.ValidationError("El teléfono debe tener 10 dígitos.")

        return telefono


    def clean_numero_documento(self):
        numero = self.cleaned_data.get('numero_documento')

        if not numero.isdigit():
            raise forms.ValidationError("El número de documento solo debe contener dígitos.")

        if len(numero) < 6:
            raise forms.ValidationError("El número de documento es demasiado corto.")

        if len(numero) > 12:
            raise forms.ValidationError("El número de documento es demasiado largo.")

        return numero
    
class PedidoForm(ModelForm):
    class Meta:
        model = Pedido
        fields = ['mesa', 'usuario', 'estado']
        widgets = {
            'mesa': forms.Select(attrs={
            'class': 'form-control select2', 
            'data-placeholder': 'Seleccione una mesa',
            }),
            'usuario': forms.Select(attrs={
            'class': 'form-control select2',
            'data-placeholder': 'Seleccione un empleado',
            }),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['estado'].choices = [
                ('Preparación', 'Preparación')
            ]
            self.fields['estado'].initial = 'Preparación'


        elif self.instance.estado == 'Entregado':
            self.fields['estado'].disabled = True

    def clean_estado(self):
        
        if self.instance.pk and self.instance.estado == 'Entregado':
            return 'Entregado'

        return self.cleaned_data.get('estado')
    
    def clean_mesa(self):
        mesa = self.cleaned_data.get('mesa')
        
        if not mesa:
            raise forms.ValidationError('Por favor seleccione una mesa.')


        if not self.instance.pk:
            if mesa and mesa.estado == 'No disponible':
                raise forms.ValidationError(
                    f'La mesa {mesa.numero_mesa} no está disponible. '
                    f'Por favor seleccione otra mesa.'
                )
        return mesa
    
    def clean_usuario(self):
        Usuario = self.cleaned_data.get('usuario')
        if not Usuario:
            raise forms.ValidationError('Por favor seleccione un usuario.')
        return Usuario


class DetallePlatoForm(ModelForm):
    class Meta:
        model = DetallePlato
        fields = ['plato', 'cantidad']
        widgets = {
            'plato': forms.Select(attrs={'class': 'form-control select2'}),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Cantidad'
            }),
        }

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        plato = self.cleaned_data.get('plato')

        # La cantidad debe ser mayor a 0
        if not plato:
            return cantidad 
        
        if cantidad is not None and cantidad <= 0:
            raise forms.ValidationError('La cantidad debe ser mayor a 0.')

        return cantidad

    def clean(self):
        cleaned_data = super().clean()
        plato    = cleaned_data.get('plato')
        cantidad = cleaned_data.get('cantidad')

        if plato:
            # El plato debe tener un precio válido registrado en la BD
            if plato.precio <= 0:
                raise forms.ValidationError(
                    f'El plato "{plato.nombre}" no tiene un precio válido. '
                    f'Contacte al administrador.'
                )

        return cleaned_data

class DetallePedidoForm(ModelForm):
    class Meta:
        model = DetallePedido
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control select2'}),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Cantidad'
            }),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostramos la descripción del producto en el selector
        # en vez del nombre que trae por defecto el __str__
        self.fields['producto'].queryset = Producto.objects.all()
        self.fields['producto'].label_from_instance = lambda obj: obj.nombre

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        producto = self.cleaned_data.get('producto')

        # La cantidad debe ser mayor a 0
        if not producto:
            return cantidad

        if cantidad is not None and cantidad <= 0:
            raise forms.ValidationError('La cantidad debe ser mayor a 0.')

        return cantidad

    def clean(self):
        cleaned_data = super().clean()
        producto = cleaned_data.get('producto')
        cantidad = cleaned_data.get('cantidad')

        # Si no hay producto seleccionado no validamos
        # (puede ser una fila vacía del formset)
        if not producto:
            return cleaned_data

        if cantidad is not None:
            if producto.stock <= 0:
                raise forms.ValidationError(
                    f'El producto "{producto.descripcion}" no tiene stock disponible. '
                    f'No es posible agregarlo al pedido.'
                )

            if cantidad > producto.stock:
                raise forms.ValidationError(
                    f'Solo hay {producto.stock} unidades disponibles de '
                    f'"{producto.descripcion}". Ingrese una cantidad menor o igual.'
                )

        return cleaned_data


DetallePlatoFormSet = inlineformset_factory(
    Pedido,
    DetallePlato,
    form=DetallePlatoForm,
    extra=1,
    can_delete=True,
    min_num=0,
    validate_min=True
)


DetallePedidoFormSet = inlineformset_factory(
    Pedido,
    DetallePedido,
    form=DetallePedidoForm,
    extra=1,
    can_delete=True,
    min_num=0,
    validate_min=True
)

class MesaForm(ModelForm):
    class Meta:
        model = Mesa
        fields = '__all__'
        widgets = {
            'numero_mesa': forms.NumberInput(attrs={
                'placeholder': 'Ingrese el número de la mesa'}),
            'estado': forms.Select(attrs={
                'placeholder': 'Seleccione el estado de la mesa'}),
            
        }
class ComandaForm(ModelForm):
    class Meta:
        model = Comanda
        fields = '__all__'
        widgets = {
            'fecha_hora': forms.DateTimeInput(attrs={
                'placeholder': 'Ingrese la fecha y hora de la comanda'}),
            'estado': forms.Select(attrs={
                'placeholder': 'Seleccione el estado de la comanda'}),
            'usuario_id': forms.NumberInput(attrs={
                'placeholder': 'Ingrese el ID del usuario que realiza la comanda'}),
        }
class CategoriaForm(ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Ingrese el nombre de la categoria'}),
            'descripcion': 
                forms.Textarea(attrs={
                    'placeholder': 'Ingrese la descripcion de la categoria',
                    'rows': 3,
                    'cols': 3}),
        }
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if len(nombre) < 3:
            raise forms.ValidationError('El nombre debe tener al menos 3 caracteres')
        if len(nombre) > 30:
            raise forms.ValidationError('El nombre no puede tener más de 30 caracteres')
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre):
            raise forms.ValidationError('El nombre solo puede contener letras y espacios')
        if nombre.isspace():
            raise forms.ValidationError('El nombre no puede ser solo espacios')
        if nombre != nombre.strip():
            raise forms.ValidationError('El nombre no puede tener espacios al inicio o al final')
        return nombre
    
    def clean_descripcion(self):
        descripcion = self.cleaned_data['descripcion']
        if len(descripcion) < 10:
            raise forms.ValidationError('La descripción debe tener al menos 10 caracteres')
        return descripcion

class PlatoForm(ModelForm):
    class Meta:
        model = Plato
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Ingrese el nombre del plato'}),
            'descripcion': 
                forms.Textarea(attrs={
                    'placeholder': 'Ingrese la descripcion del plato',
                    'rows': 3,
                    'cols': 3}),
        }
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if len(nombre) < 3:
            raise forms.ValidationError('El nombre debe tener al menos 3 caracteres')
        if not re.match(r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s]+$', nombre):
            raise forms.ValidationError('El nombre solo puede contener letras, números y espacios')
        if nombre.isdigit():
            raise forms.ValidationError('El nombre no puede ser solo números')
        if nombre.isspace():
            raise forms.ValidationError('El nombre no puede ser solo espacios')
        if nombre != nombre.strip():
            raise forms.ValidationError('El nombre no puede tener espacios al inicio o al final')
        return nombre
    
    def clean_descripcion(self):
        descripcion = self.cleaned_data['descripcion']
        if len(descripcion) < 10:
            raise forms.ValidationError('La descripción debe tener al menos 10 caracteres')
        if len(descripcion) > 200:
            raise forms.ValidationError('La descripción no puede tener más de 200 caracteres')
        if not re.match(r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s,\.]+$', descripcion):
            raise forms.ValidationError("Solo se permiten letras, números, espacios, coma (,) y punto (.)")
        return descripcion
    
    def clean_precio(self):
        precio = self.cleaned_data['precio']
        if precio < 0:
            raise forms.ValidationError('El precio no puede ser negativo')
        if precio == 0:
            raise forms.ValidationError('El precio no puede ser cero')
        if precio is None:
            raise forms.ValidationError('El precio es obligatorio')
        if re.match(r'\^[0-9\.]+$', str(precio)):
            raise forms.ValidationError('El precio solo puede contener números y puntos decimales')
        return precio
    
    def clean_categoria(self):
        categoria = self.cleaned_data['categoria']
        if categoria and categoria.estado != 'activo':
            raise forms.ValidationError('La categoría seleccionada no está activa')
        return categoria

class NotificacionForm(ModelForm):
    class Meta:
        model = Notificacion
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Ingrese el nombre de la notificación'}),
            'descripcion': 
                forms.Textarea(attrs={
                    'placeholder': 'Ingrese la descripcion de la notificación',
                    'rows': 3,
                    'cols': 3}),
        }
class MenuForm(ModelForm):
    class Meta:
        model = Menu
        fields = '__all__'
        widgets = {
            'descripcion': 
                forms.Textarea(attrs={
                    'placeholder': 'Ingrese la descripcion del menu',
                    'rows': 3,
                    'cols': 3}),
            'precio': forms.NumberInput(attrs={
                'placeholder': 'Ingrese el precio del menu'}),
        }
        

class RecetaForm(ModelForm):
    class Meta:
        model = Receta
        fields = ['plato']   # solo el plato si así lo tienes
        widgets = {
            'plato': forms.Select(attrs={
                'class': 'form-control'
            })
        }

class DetalleRecetaForm(ModelForm):
    class Meta:
        model = DetalleReceta
        fields = ['insumo', 'cantidad']
        widgets = {
            'insumo': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'})
        }

DetalleFormSet = inlineformset_factory(
    Receta,
    DetalleReceta,
    form=DetalleRecetaForm,
    extra=1,  
    can_delete=True
)

class InsumosForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

  
        self.fields['categoria'].queryset = Categoria.objects.filter(
            estado='activo'
        )
        from datetime import date
        self.fields['fecha_vencimiento'].widget.attrs['min'] = date.today().isoformat()

    class Meta:
        model = insumo
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Ingrese el nombre del insumo'}),
            'descripcion': forms.Textarea(attrs={
                'placeholder': 'Ingrese la descripcion del insumo',
                'rows': 3,
                'cols': 3}),
            'valor': forms.NumberInput(attrs={
                'placeholder': 'Ingrese el valor del insumo'}),
            'fecha_vencimiento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }, format='%Y-%m-%d'),
        }


    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        
        # ── CORRECCIÓN: excluye el insumo actual al editar ──
        qs = insumo.objects.filter(nombre__iexact=nombre)
        if self.instance.pk:  # si estamos editando
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Este insumo ya está registrado.')

        if len(nombre) < 3:
            raise forms.ValidationError('El nombre debe tener al menos 3 caracteres')

        if not re.match(r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ ]+$', nombre):
            raise forms.ValidationError('El nombre solo puede contener letras, números y espacios')

        if nombre.isdigit():
            raise forms.ValidationError('El nombre no puede ser solo números')

        if "  " in nombre:
            raise forms.ValidationError('No se permiten espacios dobles')

        if nombre.startswith(' ') or nombre.endswith(' '):
            raise forms.ValidationError('El nombre no puede iniciar ni terminar con espacio')

        return nombre

    def clean_categoria(self):
        categoria = self.cleaned_data.get('categoria')

        if categoria.estado != 'activo':
            raise forms.ValidationError(
                'No puede seleccionar una categoría inactiva.'
            )

        return categoria
    

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')

        if len(descripcion) < 10:
            raise forms.ValidationError(
                'La descripcion debe tener al menos 10 caracteres'
            )

        if descripcion.isdigit():
            raise forms.ValidationError(
                'La descripcion no puede ser solo números'
            )
        
        if not re.match(r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ ]+$', descripcion):
            raise forms.ValidationError(
                'La descripcion solo puede contener letras, números y espacios'
            )

        return descripcion

    def clean_valor(self):
        valor = self.cleaned_data.get('valor')

        if valor is not None and valor > 10000000:
            raise forms.ValidationError(
                'El valor es demasiado alto'
            )

        return valor


    # 🔹 Validación individual de STOCK
    def clean_stock(self):
        stock = self.cleaned_data.get('stock')

        if stock is not None and stock > 1000000:
            raise forms.ValidationError(
                'El stock es demasiado alto'
            )

        return stock

    def clean(self):
        cleaned_data = super().clean()

        valor = cleaned_data.get('valor')
        stock = cleaned_data.get('stock')

        if valor is not None and valor < 0:
            self.add_error('valor', 'El valor debe ser mayor a 0')

        if stock is not None and stock < 0:
            self.add_error('stock', 'El stock no puede ser negativo')

        return cleaned_data    
    
        
class FacturaForm(ModelForm):
    class Meta:
        model = Factura
        fields = '__all__'
        widgets = {
            'valor_total': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el valor total'
            }),
            'metodo_pago': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('Efectivo', 'Efectivo'),
                ('Tarjeta', 'Tarjeta'),
                ('Transferencia', 'Transferencia'),
            ])
        }

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['pedido']
        
class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['metodo_pago']
        widgets = {
            'metodo_pago': forms.Select(attrs={'class': 'form-control'})
        }

class UsuarioForm(ModelForm):
    
    class Meta:
        model = Usuario
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Ingrese el nombre del usuario'}),
            'apellido': forms.TextInput(attrs={
                'placeholder': 'Ingrese el apellido del usuario'}),
            'correo_electronico': forms.EmailInput(attrs={
                'placeholder': 'Ingrese el correo electrónico del usuario'}),
            'rol': forms.Select(attrs={
                'placeholder': 'Seleccione el rol del usuario'}),
            'contrasena': forms.PasswordInput(render_value=True, attrs={
                'placeholder': 'Ingrese la contraseña del usuario'}),
            'numero_documento': forms.TextInput(attrs={
                'placeholder': 'Ingrese el número de documento del usuario'}),
    
        }
    def clean_nombre(self): 
        nombre = self.cleaned_data.get('nombre')
        if nombre.isdigit():
            raise forms.ValidationError('El nombre no puede ser solo números')
        if nombre.startswith(' '):
            raise forms.ValidationError('El nombre no puede iniciar con espacio')
        if len(nombre) < 3:
            raise forms.ValidationError('El nombre debe tener al menos 3 caracteres')
        if not re.match(r'^[a-zA-Z\s]+$', nombre):
            raise forms.ValidationError('El nombre solo puede contener letras y espacios')
        return nombre
    
    def clean_apellido(self):
        apellido = self.cleaned_data.get('apellido')
        if len(apellido) < 3:
            raise forms.ValidationError('El apellido debe tener al menos 3 caracteres')
        if not re.match(r'^[a-zA-Z\s]+$', apellido):
            raise forms.ValidationError('El apellido solo puede contener letras y espacios')   
        return apellido

    def clean_correo_electronico(self):
        correo = self.cleaned_data.get('correo_electronico')

        if not correo:
            raise forms.ValidationError("El correo electrónico es obligatorio.")
        correo = correo.lower().strip()
        usuarios = Usuario.objects.filter(correo_electronico__iexact=correo)
        if self.instance.pk:
            usuarios = usuarios.exclude(pk=self.instance.pk)
        if usuarios.exists():
            raise forms.ValidationError("El correo electrónico ya está registrado.")
        return correo
    
    def clean_contrasena(self):
        
        contrasena = self.cleaned_data.get('contrasena')
        if len(contrasena) < 8:
            raise forms.ValidationError('La contraseña debe tener al menos 8 caracteres')
        if not re.search(r'[A-Z]', contrasena):
            raise forms.ValidationError('La contraseña debe contener al menos una letra mayúscula')

        if not re.search(r'[a-z]', contrasena):
            raise forms.ValidationError('La contraseña debe contener al menos una letra minúscula')

        if not re.search(r'[0-9]', contrasena):
            raise forms.ValidationError('La contraseña debe contener al menos un número')
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', contrasena):
            raise forms.ValidationError('La contraseña debe contener al menos un carácter especial')

        if re.search(r'(.)\1{3,}', contrasena):
            raise forms.ValidationError('La contraseña no puede contener caracteres repetidos más de 3 veces')

        if contrasena in ['123456', 'password', 'qwerty', 'admin123']:
            raise forms.ValidationError('La contraseña es demasiado común')
        
        return contrasena
    
    def clean_numero_documento(self):
        numero_documento = self.cleaned_data.get('numero_documento')

        if not numero_documento:
            raise forms.ValidationError('Debe ingresar un número de documento')

        numero_documento = numero_documento.strip()

        if not re.match(r'^[0-9]+$', numero_documento):
            raise forms.ValidationError('El número de documento solo puede contener números')

        if len(numero_documento) < 10:
            raise forms.ValidationError('El número de documento debe tener al menos 10 caracteres')

        if len(numero_documento) > 15:
            raise forms.ValidationError('El número de documento no puede tener más de 15 caracteres')

        if numero_documento == numero_documento[0] * len(numero_documento):
            raise forms.ValidationError('Número de documento inválido')

        numeros_invalidos = ['123456789', '1234567890', '0000000000']
        if numero_documento in numeros_invalidos:
            raise forms.ValidationError('Número de documento inválido')

        return numero_documento

    
    
class ProveedorForm(ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'
        widgets = {
            'nombre_proveedor': forms.TextInput(attrs={
                'placeholder': 'Ingrese el nombre del proveedor'}),
            'telefono': forms.TextInput(attrs={
                'placeholder': 'Ingrese el teléfono del proveedor'}),
            'correo_electronico': forms.EmailInput(attrs={
                'placeholder': 'Ingrese el correo electrónico del proveedor'}),
            'direccion': forms.Textarea(attrs={
                'placeholder': 'Ingrese la dirección del proveedor',
                'rows': 3,
                'cols': 3}),
            'numero_documento': forms.TextInput(attrs={
                'placeholder': 'Ingrese el número de documento del proveedor'}),
        }

    def clean_nombre_proveedor(self):
        nombre = (self.cleaned_data.get('nombre_proveedor') or "").strip()

        if not nombre:
            raise forms.ValidationError('El nombre es obligatorio.')

        if len(nombre) < 3:
            raise forms.ValidationError('El nombre del proveedor debe tener al menos 3 caracteres')
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s\.\-&]+$', nombre):
            raise forms.ValidationError('El nombre contiene caracteres no permitidos')
        return nombre

    def clean_telefono(self):
        telefono = (self.cleaned_data.get('telefono') or "").strip()

        if not telefono:
            raise forms.ValidationError('El teléfono es obligatorio.')

        if not telefono.isdigit():
            raise forms.ValidationError('El teléfono solo puede contener números')

        if len(telefono) < 10:
            raise forms.ValidationError('El teléfono debe tener al menos 10 caracteres')

        return telefono

    def clean_correo_electronico(self):
        correo = (self.cleaned_data.get('correo_electronico') or "").strip().lower()

        if not correo:
            raise forms.ValidationError('El correo electrónico es obligatorio.')

        proveedores = Proveedor.objects.filter(correo_electronico__iexact=correo)
        if self.instance.pk:
            proveedores = proveedores.exclude(pk=self.instance.pk)

        if proveedores.exists():
            raise forms.ValidationError('El correo electrónico ya está registrado.')

        return correo

    def clean_direccion(self):
        direccion = (self.cleaned_data.get('direccion') or "").strip()

        if len(direccion) < 10:
            raise forms.ValidationError('La dirección debe tener al menos 10 caracteres')

        return direccion

    def clean_numero_documento(self):
        numero = (self.cleaned_data.get('numero_documento') or "").strip()

        if not numero.isdigit():
            raise forms.ValidationError('El número de documento debe contener solo números.')

        return numero

class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Ingrese el nombre del producto'}),
            'descripcion': forms.Textarea(attrs={
                'placeholder': 'Ingrese la descripción del producto',
                'rows': 3,
                'cols': 3}),
            'precio': forms.NumberInput(attrs={
                'placeholder': 'Ingrese el precio del producto'}),
            'cantidad': forms.NumberInput(attrs={
                'placeholder': 'Ingrese el stock del producto'}),
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date',}),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date',
                'placeholder': 'Ingrese la fecha de vencimiento del producto'}),
        }

    def clean_nombre(self):
        nombre = (self.cleaned_data.get('nombre') or "").strip()
        if not nombre:
            raise forms.ValidationError('El nombre es obligatorio.')

        if len(nombre) < 3:
            raise forms.ValidationError('El nombre del producto debe tener al menos 3 caracteres')

        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s\.\-&]+$', nombre):
            raise forms.ValidationError('El nombre contiene caracteres no permitidos')
        return nombre

    def clean_descripcion(self):
        descripcion = (self.cleaned_data.get('descripcion') or "").strip()

        if not descripcion:
            raise forms.ValidationError('La descripción es obligatoria.')

        if len(descripcion) < 5:
            raise forms.ValidationError('La descripción debe tener al menos 5 caracteres')
        return descripcion



    def clean_precio(self):
        precio = self.cleaned_data.get('precio')

        if precio is None:
            raise forms.ValidationError('El precio es obligatorio.')

        if precio <= 0:
            raise forms.ValidationError('El precio debe ser mayor a 0')
        return precio

    def clean(self):
        cleaned_data = super().clean()

        fecha_ingreso = cleaned_data.get('fecha_ingreso')
        fecha_vencimiento = cleaned_data.get('fecha_vencimiento')

        if fecha_vencimiento and fecha_ingreso:
            if fecha_vencimiento <= fecha_ingreso:
                self.add_error('fecha_vencimiento', 'La fecha de vencimiento debe ser posterior a la fecha de ingreso.')
        return cleaned_data

class CompraForm(ModelForm):

    articulo = forms.ChoiceField(
        label="Artículo",
        choices=[],
        required=True
    )

    class Meta:
        model = Compra
        fields = "__all__"

        widgets = {
            "producto": forms.HiddenInput(),
            "insumo": forms.HiddenInput(),

            "proveedor": forms.Select(attrs={
                "placeholder": "Seleccione el proveedor"
            }),

            "cantidad": forms.NumberInput(attrs={
                "placeholder": "Ingrese la cantidad de la compra",
                "id": "id_cantidad"
            }),

            "precio_unitario": forms.NumberInput(attrs={
                "placeholder": "Ingrese el precio unitario",
                "id": "id_precio_unitario"
            }),

            "fecha_compra": forms.DateInput(attrs={
                "type": "date"
            }),

            "estado_pago": forms.Select(),

            "total_compra": forms.NumberInput(attrs={
                "readonly": True,
                "id": "id_total_compra"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        opciones = [
            ("", "Seleccione un artículo")
        ]

        # Productos
        for producto in Producto.objects.all():
            opciones.append(
                (
                    f"producto_{producto.pk}",
                    f"Producto - {producto.nombre}"
                )
            )

        # Insumos
        for item in insumo.objects.all():
            opciones.append(
                (
                    f"insumo_{item.pk}",
                    f"Insumo - {item.nombre}"
                )
            )

        self.fields["articulo"].choices = opciones

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get("cantidad")

        if cantidad <= 0:
            raise forms.ValidationError(
                "La cantidad debe ser mayor a 0"
            )

        return cantidad

    def clean_precio_unitario(self):
        precio = self.cleaned_data.get("precio_unitario")

        if precio <= 0:
            raise forms.ValidationError(
                "El precio unitario debe ser mayor a 0"
            )

        return precio

    def clean(self):
        cleaned_data = super().clean()

        articulo = cleaned_data.get("articulo")

        if not articulo:
            raise forms.ValidationError(
                "Debe seleccionar un artículo."
            )

        if articulo.startswith("producto_"):
            pk = articulo.split("_")[1]
            cleaned_data["producto"] = Producto.objects.get(pk=pk)
            cleaned_data["insumo"] = None

        elif articulo.startswith("insumo_"):
            pk = articulo.split("_")[1]
            cleaned_data["insumo"] = insumo.objects.get(pk=pk)
            cleaned_data["producto"] = None

        return cleaned_data

    def save(self, commit=True):
        compra = super().save(commit=False)

        compra.producto = self.cleaned_data.get("producto")
        compra.insumo = self.cleaned_data.get("insumo")

        if commit:
            compra.save()

        return compra