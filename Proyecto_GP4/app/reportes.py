from django.shortcuts import render
from django.views.generic import View
from django.views import View as DjangoView
from django.http import HttpResponse, JsonResponse
from app.models import *
from app.utils import exportar_pdf, exportar_excel
from datetime import datetime
from django.utils import timezone
from django.shortcuts import render


# ====== EXPORTAR INSUMOS======

class ExportarinsumosPDF(DjangoView):
    """
    VISTA PARA EXPORTAR INSUMOS A PDF
    Obtiene todos los insumos y los exporta en formato PDF
    """    
    def get(self, request):
        # Obtener todos los insumos
        insumos = insumo.objects.all()
        
        # Definir las columnas que se muestran en el reporte
        columnas = ['id_insumo', 'nombre', 'descripcion', 'categoria', 'stock', 'valor']       
        # Preparar los datos en formato de tuplas
        datos = [
            (i.id_insumo, i.nombre, i.descripcion, i.categoria, i.stock, i.valor)
            for i in insumos
        ]      
        # Generar nombre del archivo con timestamp
        nombre_archivo = f'Reporte_Insumos_{datetime.now().strftime("%d_%m_%Y")}'
        # Llamar funcion de exportacion a PDF
        return exportar_pdf(
            titulo='REPORTE DE INSUMOS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )

class ExportarinsumosExcel(DjangoView):
    """
    VISTA PARA EXPORTAR INSUMOS A EXCEL
    Obtiene todos los insumos y los exporta en formato Excel
    """   
    def get(self, request):
        # Obtener todos los insumos
        insumos = insumo.objects.all()       
        # Definir las columnas que se mostraran en el reporte
        columnas = ['id_insumo', 'nombre', 'descripcion', 'categoria', 'stock', 'valor']
        # Preparar los datos en  tuplas
        datos = [
            (insumo.id_insumo, str(insumo.nombre), str(insumo.descripcion), str(insumo.categoria), insumo.stock, insumo.valor)
            for insumo in insumos
        ]      
        # Generar nombre del archivo con timestamp
        nombre_archivo = f'Reporte_Insumos_{datetime.now().strftime("%d_%m_%Y")}'
        
        # Llamar funcion de exportacion a Excel
        return exportar_excel(
            titulo='REPORTE DE INSUMOS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )
    
# ====== EXPORTAR CATEGORIAS ======
class ExportarCategoriasPDF(DjangoView):
    def get(self, request):
        categorias = Categoria.objects.all()
        columnas = ['ID', 'Nombre', 'Descripción','Estado', 'Fecha_creacion']
        datos = [( cat.id , cat.nombre , cat.descripcion, cat.estado, cat.fecha_creacion) for cat in categorias]
        
        nombre_archivo = f'Reporte_Categorias_{datetime.now().strftime("%d_%m_%Y")}'
        
        return exportar_pdf(
            titulo='REPORTE DE CATEGORIAS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )

class ExportarCategoriasExcel(DjangoView):
    
    def get(self, request):
        # Obtener todas las categorias 
        categorias = Categoria.objects.all()
        
        # Definir las columnas que se mostraran en el reporte
        columnas = ['ID', 'Nombre', 'Descripcion', 'Estado']
        
        # Preparar los datos en  tuplas
        datos = [
            (cat.id, cat.nombre, cat.descripcion, cat.estado)
            for cat in categorias
        ]
        
        # Generar nombre del archivo con timestamp
        nombre_archivo = f'Reporte_Categorias_{datetime.now().strftime("%d_%m_%Y")}'
        
        # Llamar funcion de exportacion a Excel
        return exportar_excel(
            titulo='REPORTE DE CATEGORIAS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )

# ====== EXPORTAR PROVEEDORES ======
class ExportarProveedoresPDF(DjangoView):
    """
    VISTA PARA EXPORTAR PROVEEDORES A PDF
    Obtiene todos los proveedores y los exporta en formato PDF
    """

    
    def get(self, request):
        # Obtener todas las categorias 
        proveedor = Proveedor.objects.all()
        
        # Definir las columnas que se muestran en el reporte
        columnas = ['ID', 'Nombre', 'Telefono', 'Correo', 'Direccion']
        
        # Preparar los datos en formato de tuplas
        datos = [
            (cat.id_proveedor, cat.nombre_proveedor, cat.telefono, cat.correo_electronico, cat.direccion)
            for cat in proveedor
        ]
        
        # Generar nombre del archivo con timestamp
        nombre_archivo = f'Reporte_Proveedores_{datetime.now().strftime("%d_%m_%Y")}'
        
        # Llamar funcion de exportacion a PDF
        return exportar_pdf(
            titulo='REPORTE DE PROVEEDORES',
            columnas=columnas,
            datos=datos,   
            nombre_archivo=nombre_archivo
        )

class ExportarProveedoresExcel(DjangoView):
    
    def get(self, request):
        # Obtener todos los proveedores 
        proveedor = Proveedor.objects.all()
        
        
        # Definir las columnas que se mostraran en el reporte
        columnas = ['ID', 'Nombre', 'Telefono', 'Correo', 'Direccion']
        
        # Preparar los datos en  tuplas
        datos = [
            (cat.id_proveedor, cat.nombre_proveedor, cat.telefono, cat.correo_electronico, cat.direccion)
            for cat in proveedor
        ]
        
        # Generar nombre del archivo con timestamp
        nombre_archivo = f'Reporte_Proveedores_{datetime.now().strftime("%d_%m_%Y")}'
        
        # Llamar funcion de exportacion a Excel
        return exportar_excel(
            titulo='REPORTE DE PROVEEDORES',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )
    


# ====== EXPORTAR VENTAS ======

class ExportarventasPDF(DjangoView):
    """
    VISTA PARA EXPORTAR VENTAS A PDF
    Obtiene todas las ventas y las exporta en formato PDF
    """
    
    def get(self, request):
        # Obtener todas las ventas
        ventas = Venta.objects.all()
        
        # primero validemos  que existan datos antes de generar el reporte
        if not ventas.exists():
            
            return render(request, 'reportes/alerta.html', status=404)
        
        # Definir las columnas que se muestran en el reporte
        columnas = ['ID', 'Usuario', 'Pedido', 'Total', 'Fecha']
        
        # Preparar los datos en formato de tuplas
        datos = [
            (venta.id_venta, venta.usuario, venta.pedido, venta.total, venta.fecha_venta)
            for venta in ventas
        ]
        
        # Generar nombre del archivo con timestamp
        nombre_archivo = f'Reporte_Ventas_{datetime.now().strftime("%d_%m_%Y")}'
        
        # Llamar funcion de exportacion a PDF
        return exportar_pdf(
            titulo='REPORTE DE VENTAS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )

class ExportarventasExcel(DjangoView):
    """
    VISTA PARA EXPORTAR VENTAS A EXCEL
    Obtiene todas las ventas y las exporta en formato Excel
    """
    
    def get(self, request):
        # Obtener todas las ventas
        ventas = Venta.objects.all()
        
        # Validar que existan datos antes de generar el reporte
        if not ventas.exists():
            
            return render(request, 'reportes/alerta.html', status=404)
        
        # Definir las columnas que se mostraran en el reporte
        columnas = ['ID', 'Usuario', 'Pedido', 'Total', 'Fecha']
        
        # Preparar los datos en  tuplas
        datos = [
            (venta.id_venta, str(venta.usuario), str(venta.pedido), venta.total, venta.fecha_venta.replace(tzinfo=None))
            for venta in ventas
        ]
        
        # Generar nombre del archivo con timestamp
        nombre_archivo = f'Reporte_Ventas_{datetime.now().strftime("%d_%m_%Y")}'
        
        # Llamar funcion de exportacion a Excel
        return exportar_excel(
            titulo='REPORTE DE VENTAS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )


# ====== EXPORTAR PEDIDOS ======

class ExportarpedidoPDF(DjangoView):

    def get(self, request):
        
        estado = request.GET.get('buscar', '')
        fecha = request.GET.get('fecha', '')

        pedidos = Pedido.objects.all().prefetch_related(
            'detalle_platos__plato',
            'detalle_productos__producto',
        )
        
        if estado:
            pedidos = pedidos.filter(estado__incontains=estado)
            
        if fecha:
            pedidos = pedidos.filter(fecha_hora__date=fecha)

        columnas = ['ID', 'MESA', 'PLATOS', 'PRODUCTOS', 'USUARIO', 'FECHA', 'ESTADO', 'TOTAL']

        datos = []

        for pedido in pedidos:

            platos = ", ".join([
                detalle.plato.nombre for detalle in pedido.detalle_platos.all()
            ])

            productos = ", ".join([
                detalle.producto.nombre for detalle in pedido.detalle_productos.all()
            ])

            datos.append(
                (
                    pedido.id_pedido,
                    pedido.mesa.numero_mesa,
                    platos,
                    productos,
                    pedido.usuario,
                    pedido.fecha_hora,
                    pedido.estado,
                    pedido.total
                )
            )

        nombre_archivo = f'Reporte_Pedidos_{datetime.now().strftime("%d_%m_%Y")}'

        return exportar_pdf(
            titulo='REPORTE DE PEDIDOS',
            columnas=columnas,
            datos=datos,    
            nombre_archivo=nombre_archivo
        )
    

class ReportePedidosExcel(DjangoView):
    

    def get(self, request):
        
        estado = request.GET.get('buscar', '')
        fecha = request.GET.get('fecha', '')

        pedidos = Pedido.objects.all().prefetch_related(
            'detalle_platos__plato',
            'detalle_productos__producto',
        )
        
        if estado:
            pedidos = pedidos.filter(estado__icontains=estado)
            
        if fecha:
            pedidos = pedidos.filter(fecha_hora__date=fecha)

        columnas = ['ID', 'MESA', 'PLATOS', 'PRODUCTOS', 'USUARIO', 'FECHA', 'ESTADO', 'TOTAL']

        datos = []

        for pedido in pedidos:

            platos = ", ".join([
                detalle.plato.nombre for detalle in pedido.detalle_platos.all()
            ])

            productos = ", ".join([
                detalle.producto.nombre for detalle in pedido.detalle_productos.all()
            ])

            datos.append(
                (
                    pedido.id_pedido,
                    pedido.mesa.numero_mesa,
                    platos,
                    productos,
                    str(pedido.usuario),
                    timezone.localtime(pedido.fecha_hora).strftime("%d/%m/%Y %H:%M"),
                    pedido.estado,
                    pedido.total
                )
            )

        nombre_archivo = f'Reporte_Pedidos_{datetime.now().strftime("%d_%m_%Y")}'

        return exportar_excel(
            titulo='REPORTE DE PEDIDOS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )

# ====== EXPORTAR productos ======
class ExportarProductosPDF(DjangoView):
    
    
    """
    VISTA PARA EXPORTAR PRODUCTOS A PDF
    Obtiene todos los productos y los exporta en formato PDF
    """

    
    def get(self, request):
        # Obtener todas las categorias 
        producto = Producto.objects.all()
        
        # Definir las columnas que se muestran en el reporte
        columnas = ['ID', 'Nombre', 'Unidad', 'Precio', 'Stock', 'Fecha de Ingreso', 'Fecha de Vencimiento']
        
        # Preparar los datos en formato de tuplas
        datos = [
            (cat.id_producto, cat.nombre, cat.unidad, cat.precio, cat.stock, cat.fecha_ingreso, cat.fecha_vencimiento)
            for cat in producto
        ]
        
        # Generar nombre del archivo con timestamp
        nombre_archivo = f'Reporte_Productos_{datetime.now().strftime("%d_%m_%Y")}'
        
        # Llamar funcion de exportacion a PDF
        return exportar_pdf(
            titulo='REPORTE DE PRODUCTOS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )

class ExportarProductosExcel(DjangoView):
    """
    VISTA PARA EXPORTAR PRODUCTOS A EXCEL
    Obtiene todos los productos y los exporta en formato Excel
    """
    
    def get(self, request):
        # Obtener todas las categorias 
        producto = Producto.objects.all()
        
        # Definir las columnas que se mostraran en el reporte
        columnas = ['ID', 'NOMBRE', 'UNIDAD', 'PRECIO', 'STOCK', 'FECHA DE NGRESO', 'FECHA DE VENCIMIENTO']
        
        # Preparar los datos en  tuplas
        datos = [
            (cat.id_producto, cat.nombre, cat.unidad, cat.precio, cat.stock, cat.fecha_ingreso, cat.fecha_vencimiento)
            for cat in producto
        ]
        
        # Generar nombre del archivo con timestamp
        nombre_archivo = f'Reporte_Productos_{datetime.now().strftime("%d_%m_%Y")}'
        
        # Llamar funcion de exportacion a Excel
        return exportar_excel(
            titulo='REPORTE DE PRODUCTOS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )


#-------------------------------------------------------------------------------
#=======ESTAS SON LAS VISTAS O CLASES PARA CREAR EL REPORTE DE PAGOS============
#-------------------------------------------------------------------------------

class ExportarpagosPDF(DjangoView):
    """
    VISTA PARA EXPORTAR PAGOS A PDF
    Obtiene todos los pagos y los exporta en formato PDF
    """
    
    def get(self, request):
        # Obtener todos los pagos
        pagos = Pago.objects.all()
        
        #vamos a validar ahpora para alerta de pagos
        if not pagos.exists():
            
            return render(request, 'reportes/alerta.html', status=404)
        # Definir las columnas que se muestran en el reporte
        columnas = ['ID', 'Venta', 'Factura', 'Total venta ', 'Monto pagado ', 'Fecha', 'Metodo de pago']
        
        # Preparar los datos en formato de tuplas
        datos = [
            (pago.id_pago, pago.venta, pago.factura, pago.venta.total, pago.monto, pago.fecha, pago.metodo_pago)
            for pago in pagos
        ]
        
        # Generar nombre del archivo con timestamp
        nombre_archivo = f'Reporte_Pagos_{datetime.now().strftime("%d_%m_%Y")}'
        
        # Llamar funcion de exportacion a PDF
        return exportar_pdf(
            titulo='REPORTE DE PAGOS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )

class ExportarpagosExcel(DjangoView):
    """
    VISTA PARA EXPORTAR PAGOS A EXCEL
    Obtiene todos los pagos y los exporta en formato Excel
    """
    
    def get(self, request):
        # Obtener todos los pagos
        pagos = Pago.objects.all()
        
        # Definir las columnas que se muestran en el reporte
        columnas = ['ID', 'Venta', 'Factura', 'Total venta ', 'Monto pagado ', 'Fecha', 'Metodo de pago']
        
        # Preparar los datos en formato de tuplas
        datos = [
            (pago.id_pago, str(pago.venta), pago.factura, pago.venta.total, pago.monto, pago.fecha.replace(tzinfo=None), pago.metodo_pago)
            for pago in pagos
        ]
        
        # Generar nombre del archivo con timestamp
        nombre_archivo = f'Reporte_Pagos_{datetime.now().strftime("%d_%m_%Y")}'
        
        # Llamar funcion de exportacion a Excel
        return exportar_excel(
            titulo='REPORTE DE PAGOS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )
        
#======================================================================================



# ====== EXPORTAR compras ======

class ExportarcomprasPDF(DjangoView):
    """
    VISTA PARA EXPORTAR COMPRAS A PDF
    Obtiene todas las compras y las exporta en formato PDF
    """

    
    def get(self, request):
        # Obtener todas las categorias 
        compra = Compra.objects.all()
        
        # Definir las columnas que se muestran en el reporte
        columnas = ['ID', 'PROVEEDOR','PRODUCTO', 'INSUMO', 'FECHA COMPRA', 'ESTADO PAGO', 'TOTAL']
        
        # Preparar los datos en formato de tuplas
        datos = [
            (cat.id_compra, cat.proveedor, cat.producto, cat.insumo, cat.fecha_compra, cat.estado_pago, cat.total_compra)
            for cat in compra
        ]
        
        # Generar nombre del archivo con timestamp
        nombre_archivo = f'Reporte_Compras_{datetime.now().strftime("%d_%m_%Y")}'
        
        # Llamar funcion de exportacion a PDF
        return exportar_pdf(
            titulo='REPORTE DE COMPRAS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )


class ExportarcomprasExcel(DjangoView):
    
    def get(self, request):
        # Obtener todas las categorias 
        compra = Compra.objects.all()
        
        # Definir las columnas que se mostraran en el reporte
        columnas = ['ID', 'PROVEEDOR', 'PRODUCTO', 'INSUMO', 'FECHA COMPRA', 'ESTADO PAGO', 'TOTAL']
        
        # Preparar los datos en  tuplas
        datos = [
            (cat.id_compra,str(cat.proveedor), str(cat.producto), str(cat.insumo), cat.fecha_compra.replace(tzinfo=None), cat.estado_pago, cat.total_compra)
            for cat in compra
        ]
        
        # Generar nombre del archivo con timestamp
        nombre_archivo = f'Reporte_Compras_{datetime.now().strftime("%d_%m_%Y")}'
        
        # Llamar funcion de exportacion a Excel
        return exportar_excel(
            titulo='REPORTE DE COMPRAS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )
#======================================================================================




#=======ESTAS SON LAS VISTAS O CLASES PARA CREAR EL REPORTE DE FACTURAS============

class ExportarfacturasPDF(DjangoView):
    """
    VISTA PARA EXPORTAR FACTURAS A PDF
    Obtiene todas las facturas y las exporta en formato PDF
    """
    
    def get(self, request):
        # Obtener todas las facturas
        facturas = Factura.objects.all()
        
        # Definir las columnas que se muestran en el reporte
        columnas = ['ID', 'Venta', 'Total', 'Método de pago', 'Fecha']
        
        # Preparar los datos en formato de tuplas
        datos = [
            (factura.id, factura.venta, factura.valor_total, factura.metodo_pago, factura.fecha_hora)
            for factura in facturas
        ]
        
        # Generar nombre del archivo con timestamp
        nombre_archivo = f'Reporte_Facturas_{datetime.now().strftime("%d_%m_%Y")}'
        
        # Llamar funcion de exportacion a PDF
        return exportar_pdf(
            titulo='REPORTE DE FACTURAS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )

class ExportarfacturasExcel(DjangoView):
    """
    VISTA PARA EXPORTAR FACTURAS A EXCEL
    Obtiene todas las facturas y las exporta en formato Excel
    """
    
    def get(self, request):
        # Obtener todas las facturas
        facturas = Factura.objects.all()
        
        # Definir las columnas que se mostraran en el reporte
        columnas = ['ID', 'Venta', 'Total', 'Método de pago', 'Fecha']
        
        # Preparar los datos en  tuplas
        datos = [
            (factura.id, str(factura.venta), factura.valor_total, factura.metodo_pago, factura.fecha_hora.replace(tzinfo=None))
            for factura in facturas
        ]
        
        # Generar nombre del archivo con timestamp
        nombre_archivo = f'Reporte_Facturas_{datetime.now().strftime("%d_%m_%Y")}'
        
        # Llamar funcion de exportacion a Excel
        return exportar_excel(
            titulo='REPORTE DE FACTURAS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )
    
class ExportarclientesPDF(DjangoView):
    def get(self, request):
        clientes = Cliente.objects.all()
        columnas = ['ID', 'Nombre', 'Correo', 'Telefono', 'Direccion']
        datos = [( cliente.id_cliente, cliente.nombre, cliente.correo_electronico, cliente.telefono, cliente.direccion) for cliente in clientes]
        
        nombre_archivo = f'Reporte_Clientes_{datetime.now().strftime("%d_%m_%Y")}'
        
        return exportar_pdf(
            titulo='REPORTE DE CLIENTES',
            columnas=columnas,
            datos=datos,    
            nombre_archivo=nombre_archivo
        )
        
class ExportarclientesExcel(DjangoView):
    def get(self, request):
        clientes = Cliente.objects.all()
        columnas = ['ID', 'Nombre', 'Correo', 'Telefono', 'Direccion']
        datos = [( cliente.id_cliente, cliente.nombre, cliente.correo_electronico, cliente.telefono, cliente.direccion) for cliente in clientes]
        
        nombre_archivo = f'Reporte_Clientes_{datetime.now().strftime("%d_%m_%Y")}'
        
        return exportar_excel(
            titulo='REPORTE DE CLIENTES',
            columnas=columnas,
            datos=datos,    
            nombre_archivo=nombre_archivo
        )
