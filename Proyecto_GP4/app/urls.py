from django.urls import path
from app.views.Categorias.views import *
from app.views.Platos.views import *
from app.views.Notificaciones.views import *
from app.views.Menu.views import *
from app.views.Receta.views import *
from app.views.Insumos.views import *
from app.views.Facturas.views import *
from app.views.Venta.views import *
from app.views.pago.views import *
#from app.views.usuario.views import *
from app.views.proveedor.views import *
from app.views.producto.views import *
from app.views.compra.views import *
from app.views.Comanda.views import *
from app.views.Mesa.views import *
from app.views.Pedido.views import *
from app.views.Cliente.views import *
from app.views.Dashborad.views import *
from app.reportes import *
from app.views.Backup.backup import *
from app.views.IA.views import chat_view
from app.views.Error403 import *


app_name = 'app'
urlpatterns = [
    
#urls de categorias
    path('listar_categorias/', CategoriaListView.as_view() , name='listar_categorias'),
    path('crear_categoria/', CategoriaCreateView.as_view() , name='crear_categoria'),
    path('editar_categoria/<int:pk>/', CategoriaUpdateView.as_view(), name='editar_categoria'),
    path('eliminar_categoria/<int:pk>/', CategoriaDeleteView.as_view(), name='eliminar_categoria'),
    path('exportar_categorias_pdf/',    ExportarCategoriasPDF.as_view(),    name='exportar_categorias_pdf'),
    path('exportar_categorias_excel/',  ExportarCategoriasExcel.as_view(),  name='exportar_categorias_excel'),

#urls de platos
    path('listar_platos/', PlatoListView.as_view() , name='listar_platos'),
    path('crear_plato/', PlatoCreateView.as_view() , name='crear_plato'),
    path('editar_plato/<int:pk>/', PlatoUpdateView.as_view(), name='editar_plato'),
    path('eliminar_plato/<int:pk>/', PlatoDeleteView.as_view(), name='eliminar_plato'),
    
#urls de notificaciones
    path('listar_notificaciones/', listar_notificaciones, name='listar_notificaciones'),
    path('crear_notificacion/', NotificacionCreateView.as_view() , name='crear_notificacion'),
    path('editar_notificacion/<int:pk>/', NotificacionUpdateView.as_view(), name='editar_notificacion'),
    path('eliminar_notificacion/<int:pk>/', NotificacionDeleteView.as_view(), name='eliminar_notificacion'),
    path('notificaciones/marcar-leida/<int:pk>/', marcar_leida, name='marcar_leida'),
    path('notificaciones/marcar-todas/', marcar_leidas, name='marcar_leidas'),
    
#MENU
    path('listar_menu/', MenuListView.as_view() , name='listar_menu'),
    path('crear_menu/', MenuCreateView.as_view() , name='crear_menu'),
    path('menu/editar/<int:pk>/', editar_menu, name='editar_menu'),
    path('eliminar_menu/<int:pk>/', MenuDeleteView.as_view(), name='eliminar_menu'),
    
#RECETA
    path('listar_receta/', RecetaListView.as_view() , name='listar_receta'),
    path('crear_receta/', RecetaCreateView.as_view() , name='crear_receta'),
    path('editar_receta/<int:pk>/', RecetaUpdateView.as_view(), name='editar_receta'),
    path('eliminar_receta/<int:pk>/', RecetaDeleteView.as_view(), name='eliminar_receta'),
    
#INSUMOS
    path('listar_insumos/', InsumosListView.as_view() , name='listar_insumos'),
    path('crear_insumos/', InsumosCreateView.as_view() , name='crear_insumos'),
    path('editar_insumos/<int:pk>/', InsumosUpdateView.as_view(), name='editar_insumos'),
    path('eliminar_insumos/<int:pk>/', InsumosDeleteView.as_view(), name='eliminar_insumos'),
    path('exportar_insumos_pdf/', ExportarinsumosPDF.as_view(), name='exportar_insumos_pdf'),
    path('exportar_insumos_excel/', ExportarinsumosExcel.as_view(), name='exportar_insumos_excel'),

# FACTURAS
    path('listar_facturas/', FacturaListView.as_view() , name='listar_facturas'),
    path('crear_factura/<int:pago_id>/', crear_factura , name='crear_factura'),
    path('editar_factura/<int:pk>/', FacturaUpdateView.as_view(), name='editar_factura'),
    path('reporte_facturas/pdf/', ExportarfacturasPDF.as_view(), name='reporte_facturas_pdf'),
    path('reporte_facturas/excel/', ExportarfacturasExcel.as_view(), name='reporte_facturas_excel'),
    path('facturas/desactivar/<int:pk>/', FacturaDesactivarView.as_view(), name='desactivar_factura'),
    path('facturas/detalle/<int:pk>/', FacturaDetailView.as_view(), name='detalle_factura'), #este es nuevo muchcahos
    
# VENTAS
    path('listar_ventas/', VentaListView.as_view(), name='listar_ventas'),
    path('crear_venta/', VentaCreateView.as_view(), name='crear_venta'),
    path('editar_venta/<int:pk>/', VentaUpdateView.as_view(), name='editar_venta'),
    path('eliminar_venta/<int:pk>/', VentaDeleteView.as_view(), name='eliminar_venta'),
    path('pagar_venta/<int:venta_id>/',pagar_venta,name='pagar_venta'),
    path('reporte_ventas_pdf/', ExportarventasPDF.as_view(), name='reporte_ventas_pdf'),
    path('reporte_ventas_excel/', ExportarventasExcel.as_view(), name='reporte_ventas_excel'),
    
# PAGOS
    path('listar_pagos/', PagoListView.as_view(), name='listar_pagos'),
    path('pago/crear/<int:id_venta>/', PagoCreateView.as_view(), name='crear_pago'),
    path('eliminar_pago/<int:pk>/', EliminarPagoView.as_view(), name='eliminar_pago'),
    path('reporte_pagos/pdf/', ExportarpagosPDF.as_view(), name='reporte_pagos_pdf'),
    path('reporte_pagos/excel/', ExportarpagosExcel.as_view(), name='reporte_pagos_excel'),
    
#PROVEEDORES

    path('listar_proveedores/', ProveedorListView.as_view(), name='listar_proveedores'),
    path('crear_proveedor/', ProveedorCreateView.as_view(), name='crear_proveedor'),
    path('eliminar_proveedor/<int:pk>/', ProveedorDeleteView.as_view(), name='eliminar_proveedor'),
    path('editar_proveedor/<int:pk>/', ProveedorUpdateView.as_view(), name='editar_proveedor'),
    path('exportar_proveedores_pdf/', ExportarProveedoresPDF.as_view(), name='exportar_proveedores_pdf'),
    path('exportar_proveedores_excel/', ExportarProveedoresExcel.as_view(), name='exportar_proveedores_excel'),
    path('backup/proveedores/', backup_proveedores, name='backup_proveedores'),

# PRODUCTO
    path('listar_productos/', ProductoListView.as_view(), name='listar_productos'),
    path('crear_producto/', ProductoCreateView.as_view(), name='crear_producto'),
    path('eliminar_producto/<int:pk>/', ProductoDeleteView.as_view(), name='eliminar_producto'),
    path('editar_producto/<int:pk>/', ProductoUpdateView.as_view(), name='editar_producto'),
    path('exportar_productos_pdf/', ExportarProductosPDF.as_view(), name='exportar_productos_pdf'),
    path('exportar_productos_excel/', ExportarProductosExcel.as_view(), name='exportar_productos_excel'),
    path('backup/productos/', backup_productos, name='backup_productos'),

# COMPRA 
    path('listar_compras/', CompraListView.as_view(), name='listar_compras'),
    path('crear_compra/', CompraCreateView.as_view(), name='crear_compra'),
    path('eliminar_compra/<int:pk>/', CompraDeleteView.as_view(), name='eliminar_compra'),
    path('editar_compra/<int:pk>/', CompraUpdateView.as_view(), name='editar_compra'),
    path('exportar_compras_pdf/', ExportarcomprasPDF.as_view(), name='exportar_compras_pdf'),
    path('exportar_compras_excel/', ExportarcomprasExcel.as_view(), name='exportar_compras_excel'),
    path('backup/compras/', backup_compras, name='backup_compras'),
    
# COMANDA
    path('listar_comanda/', ComandaListView.as_view() , name='listar_comandas'),
    path('imprimir_comanda/<int:pk>/', imprimir_comanda, name='imprimir_comanda'),
    
# MESA
    path('listar_mesa/', MesaListView.as_view() , name='listar_mesas'),
    path('crear_mesa/', MesaCreateView.as_view() , name='crear_mesa'),
    path('editar_mesa/<int:pk>/', MesaUpdateView.as_view(), name='editar_mesa'),
    path('eliminar_mesa/<int:pk>/', MesaDeleteView.as_view(), name='eliminar_mesa'),
    
# PEDIDO
    path('listar_pedido/', PedidoListView.as_view() , name='listar_pedidos'),
    path('crear_pedido/', PedidoCreateView.as_view() , name='crear_pedido'),
    path('editar_pedido/<int:pk>/', PedidoUpdateView.as_view(), name='editar_pedido'),
    path('eliminar_pedido/<int:pk>/', PedidoDeleteView.as_view(), name='eliminar_pedido'),
    path('pedido/detalle/<int:pk>/', DetallePedidoView.as_view(), name='detalle_pedido'),
    path('exportar_pedido_pdf/', ExportarpedidoPDF.as_view(), name='exportar_pedido_pdf'),
    path('exportar_pedido_excel/', ReportePedidosExcel.as_view(), name='exportar_pedido_excel'),
    path('verificar_mesa_disponible/', verificar_mesa_disponible, name='verificar_mesa_disponible'),

# CLIENTE
    path('listar_cliente/', ClienteListView.as_view() , name='listar_clientes'),
    path('crear_cliente/', ClienteCreateView.as_view() , name='crear_cliente'),
    path('editar_cliente/<int:pk>/', ClienteUpdateView.as_view(), name='editar_cliente'),
    path('eliminar_cliente/<int:pk>/', ClienteDeleteView.as_view(), name='eliminar_cliente'),  
    path('exportar_clientes_pdf/', ExportarclientesPDF.as_view(), name='exportar_clientes_pdf'),
    path('exportar_clientes_excel/', ExportarclientesExcel.as_view(), name='exportar_clientes_excel'),
    
# PLATO
    path('exportar_plato_pdf/', ExportarPlatoPDF.as_view(), name='exportar_plato_pdf'),
    path('exportar_plato_excel/', ExportarPlatoExcel.as_view(), name='exportar_plato_excel'),

# DASHBOARD
    path('dashboard/', dashboardView.as_view(), name='dashboard'),
    
# IA
    path('chat_bot/', chat_view, name='chat_bot'),
    
# BACKUP
    path('backup/', backup, name='backup'),
    path('backup/restaurar/', restaurar_datos, name='restaurar_datos'),
    path('backup/ventas/', backup_ventas, name='backup_ventas'),
    path('backup/pagos/', backup_pagos, name='backup_pagos'),
    path('backup/facturas/', backup_facturas, name='backup_facturas'),
    path('backup/insumos/', backup_insumos, name='backup_insumos'),
    path('backup/pedidos/', backup_pedidos, name='backup_pedidos'), 
    path('backup/clientes/', backup_clientes, name='backup_clientes'), 

  
    path('pedidos/historial/', PedidoHistorialView.as_view(), name='historial_pedidos'),
    path('ventas/historial/', VentaHistorialView.as_view(), name='historial_ventas'),
    path('pagos/historial/', PagoHistorialView.as_view(), name='historial_pagos'),
    path('facturas/historial/', FacturaHistorialView.as_view(), name='historial_facturas'),
    
# Error 403
    path('acceso_denegado/', acceso_denegado, name='acceso_denegado')
]

