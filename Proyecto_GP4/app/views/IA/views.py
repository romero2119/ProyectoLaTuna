import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ollama import chat

from usuarios.models import Usuario
from app.models import (
    Cliente,
    Producto,
    Plato,
    Venta,
    Factura,
    Pago,
    Pedido,
    Categoria,
    Mesa,
    insumo as Insumo,  # alias para que se lea mejor en el código
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------------------

SALUDOS = {
    "hola", "buenas", "buenos dias", "buenas tardes",
    "buenas noches", "hi", "hello"
}

AYUDA = {
    "ayuda", "que puedes hacer", "qué puedes hacer", "opciones"
}

# Umbral de stock bajo (no existe campo stock_minimo en tus modelos,
# así que se define aquí. Ajusta el número según tu negocio).
UMBRAL_STOCK_BAJO = 10

# palabra clave -> (nombre del módulo, modelo Django o None si no aplica conteo)
MODULOS = {
    "usuario": ("Usuarios", Usuario),
    "usuarios": ("Usuarios", Usuario),
    "cliente": ("Clientes", Cliente),
    "clientes": ("Clientes", Cliente),
    "producto": ("Productos", Producto),
    "productos": ("Productos", Producto),
    "plato": ("Platos", Plato),
    "platos": ("Platos", Plato),
    "venta": ("Ventas", Venta),
    "ventas": ("Ventas", Venta),
    "pedido": ("Pedidos", Pedido),
    "pedidos": ("Pedidos", Pedido),
    "factura": ("Facturas", Factura),
    "facturas": ("Facturas", Factura),
    "pago": ("Pagos", Pago),
    "pagos": ("Pagos", Pago),
    "mesa": ("Mesas", Mesa),
    "mesas": ("Mesas", Mesa),
    "categoria": ("Categorías", Categoria),
    "categoría": ("Categorías", Categoria),
    "categorias": ("Categorías", Categoria),
    "insumo": ("Insumos", Insumo),
    "insumos": ("Insumos", Insumo),
    # módulos sin modelo directo en este archivo, solo para "dónde" / "cómo"
    "compra": ("Compras", None),
    "compras": ("Compras", None),
    "proveedor": ("Proveedores", None),
    "proveedores": ("Proveedores", None),
}

PALABRAS_VALIDAS = set(MODULOS.keys()) | {
    "restaurante", "taqueria", "taquería", "dashboard",
    "permisos", "roles", "backup", "restaurar", "stock", "inventario"
}

PALABRAS_COMO = {
    "como", "cómo", "manera", "forma", "pasos",
    "crear", "registrar", "agregar", "añadir", "generar",
    "anular", "cancelar", "editar", "modificar", "eliminar"
}

PALABRAS_STOCK_BAJO = {
    "stock bajo", "bajo stock", "poco stock", "agotado", "agotados",
    "agotandose", "agotándose", "por agotarse", "se esta acabando",
    "se está acabando", "inventario bajo", "falta stock", "escasez"
}

# Rutas reales de tu sistema (AJUSTA según tu urls.py)
RUTAS = {
    "Usuarios": "/usuarios/",
    "Clientes": "/clientes/",
    "Productos": "/productos/",
    "Platos": "/platos/",
    "Ventas": "/ventas/",
    "Facturas": "/facturas/",
    "Pagos": "/pagos/",
    "Pedidos": "/pedidos/",
    "Categorías": "/categorias/",
    "Mesas": "/mesas/",
    "Insumos": "/insumos/",
    "Compras": "/compras/",
    "Proveedores": "/proveedores/",
}

INSTRUCCIONES = {
    "Pedidos": (
        "Para crear un pedido: ve al módulo de Pedidos, haz clic en 'Nuevo pedido', "
        "selecciona la mesa o cliente, agrega los platos y confirma."
    ),
    "Clientes": (
        "Para registrar un cliente: ve al módulo de Clientes, haz clic en 'Nuevo cliente' "
        "y completa los datos solicitados."
    ),
    "Productos": (
        "Para agregar un producto: ve al módulo de Productos, haz clic en 'Nuevo producto', "
        "asigna una categoría y guarda."
    ),
    "Platos": (
        "Para crear un plato: ve al módulo de Platos, haz clic en 'Nuevo plato', "
        "asigna los productos/insumos que lo componen y su precio."
    ),
    "Ventas": (
        "Para registrar una venta: ve al módulo de Ventas y genera una nueva venta "
        "a partir de un pedido confirmado."
    ),
    "Facturas": (
        "Para generar una factura: ve al módulo de Facturas, selecciona la venta "
        "correspondiente y haz clic en 'Generar factura'."
    ),
    "Pagos": (
        "Para registrar un pago: ve al módulo de Pagos, selecciona la factura "
        "y elige el método de pago."
    ),
    "Mesas": (
        "Para agregar una mesa: ve al módulo de Mesas y haz clic en 'Nueva mesa'."
    ),
    "Categorías": (
        "Para crear una categoría: ve al módulo de Categorías y haz clic en 'Nueva categoría'."
    ),
    "Usuarios": (
        "Para registrar un usuario: ve al módulo de Usuarios, haz clic en 'Nuevo usuario' "
        "y asigna un rol."
    ),
    "Insumos": (
        "Para registrar un insumo: ve al módulo de Insumos, haz clic en 'Nuevo insumo' "
        "e indica su categoría, unidad de medida y stock."
    ),
    "Compras": (
        "Para registrar una compra: ve al módulo de Compras, selecciona el proveedor "
        "y agrega los insumos o productos comprados."
    ),
    "Proveedores": (
        "Para registrar un proveedor: ve al módulo de Proveedores, haz clic en "
        "'Nuevo proveedor' y completa sus datos de contacto."
    ),
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _buscar_modulo(mensaje):
    for palabra, (nombre, modelo) in MODULOS.items():
        if palabra in mensaje:
            return nombre, modelo
    return None, None


def _stock_bajo(modelo, limite=10):
    """Devuelve los registros cuyo stock está por debajo del umbral fijo."""
    return list(
        modelo.objects.filter(stock__lt=UMBRAL_STOCK_BAJO).order_by("stock")[:limite]
    )


def _formatear_stock_bajo(registros, etiqueta):
    if not registros:
        return f"No hay {etiqueta} con stock bajo en este momento. Todo está en niveles normales."

    detalle = ", ".join(f"{r.nombre} ({r.stock})" for r in registros)
    return f"Los siguientes {etiqueta} tienen stock bajo (menos de {UMBRAL_STOCK_BAJO} unidades): {detalle}."


def _construir_contexto():
    totales = {
        "Usuarios": Usuario.objects.count(),
        "Clientes": Cliente.objects.count(),
        "Productos": Producto.objects.count(),
        "Platos": Plato.objects.count(),
        "Categorías": Categoria.objects.count(),
        "Mesas": Mesa.objects.count(),
        "Pedidos": Pedido.objects.count(),
        "Ventas": Venta.objects.count(),
        "Facturas": Factura.objects.count(),
        "Pagos": Pago.objects.count(),
        "Insumos": Insumo.objects.count(),
    }
    datos = "\n".join(f"{k}: {v}" for k, v in totales.items())

    return f"""Eres el asistente virtual del sistema de gestión de La Taquería.

Solo puedes responder preguntas relacionadas con este sistema.

Módulos disponibles:
Dashboard, Usuarios, Clientes, Categorías, Productos, Platos, Mesas,
Pedidos, Ventas, Facturas, Pagos, Compras, Insumos, Proveedores

Datos actuales:
{datos}

Reglas:
- Responde únicamente en español.
- No inventes información.
- No hables de temas que no pertenezcan al sistema.
- No respondas preguntas de cultura general, programación, matemáticas, historia o política.
- Si la respuesta no existe en el sistema responde: "Solo puedo ayudarte con el sistema de gestión de La Taquería."
- Responde de forma amable y en máximo tres líneas.
"""


# ---------------------------------------------------------------------------
# Vista principal
# ---------------------------------------------------------------------------

@csrf_exempt
def chat_view(request):

    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"error": "Cuerpo de solicitud inválido"}, status=400)

    mensaje = data.get("message", "").strip().lower()

    if not mensaje:
        return JsonResponse({"response": "Escriba una consulta."})

    if mensaje in SALUDOS:
        return JsonResponse({
            "response": "Hola. Soy el asistente de La Taquería. ¿En qué puedo ayudarte?"
        })

    if mensaje in AYUDA:
        return JsonResponse({
            "response": (
                "Puedo ayudarte con clientes, productos, platos, pedidos, ventas, "
                "facturas, pagos, mesas, categorías, usuarios, insumos e información del sistema."
            )
        })

    # --- "¿Qué productos/insumos tienen stock bajo?" ---
    if any(p in mensaje for p in PALABRAS_STOCK_BAJO) or "stock" in mensaje or "inventario" in mensaje:
        if "insumo" in mensaje:
            registros = _stock_bajo(Insumo)
            texto = _formatear_stock_bajo(registros, "insumos")
            return JsonResponse({"response": texto, "link": RUTAS.get("Insumos")})

        if "producto" in mensaje:
            registros = _stock_bajo(Producto)
            texto = _formatear_stock_bajo(registros, "productos")
            return JsonResponse({"response": texto, "link": RUTAS.get("Productos")})

        registros_productos = _stock_bajo(Producto)
        registros_insumos = _stock_bajo(Insumo)

        partes = []
        if registros_productos:
            partes.append(_formatear_stock_bajo(registros_productos, "productos"))
        if registros_insumos:
            partes.append(_formatear_stock_bajo(registros_insumos, "insumos"))

        if not partes:
            return JsonResponse({
                "response": f"No hay productos ni insumos con stock bajo (menos de {UMBRAL_STOCK_BAJO} unidades) en este momento."
            })

        return JsonResponse({"response": " ".join(partes)})

    # --- "¿Dónde puedo hacer X?" ---
    if "donde" in mensaje or "dónde" in mensaje:
        nombre, _ = _buscar_modulo(mensaje)
        if nombre:
            ruta = RUTAS.get(nombre)
            texto = f"Puede realizar esa operación desde el módulo de {nombre}."
            if ruta:
                texto += f" Encuéntralo en {ruta}"
            return JsonResponse({"response": texto, "link": ruta})

    # --- "¿Cómo creo/registro/agrego X?" ---
    if any(p in mensaje for p in PALABRAS_COMO):
        nombre, _ = _buscar_modulo(mensaje)
        if nombre:
            ruta = RUTAS.get(nombre)
            instruccion = INSTRUCCIONES.get(
                nombre,
                f"Puede gestionar esa acción desde el módulo de {nombre}."
            )
            if ruta:
                instruccion += f" Puedes ir directo a {ruta}."
            return JsonResponse({"response": instruccion, "link": ruta})

    # --- "¿Cuántos X hay registrados?" ---
    nombre, modelo = _buscar_modulo(mensaje)
    if nombre and modelo:
        total = modelo.objects.count()
        return JsonResponse({
            "response": f"Actualmente existen {total} {nombre.lower()} registrados.",
            "link": RUTAS.get(nombre)
        })

    if not any(p in mensaje for p in PALABRAS_VALIDAS):
        return JsonResponse({
            "response": "Solo puedo responder preguntas relacionadas con el sistema de gestión de La Taquería."
        })

    contexto = _construir_contexto()

    try:
        respuesta = chat(
            model="llama3.1",
            messages=[
                {"role": "system", "content": contexto},
                {"role": "user", "content": mensaje},
            ],
            options={
                "temperature": 0.1,
                "num_predict": 80,
                "top_k": 20,
                "top_p": 0.8,
            },
        )
        return JsonResponse({"response": respuesta["message"]["content"].strip()})
    except Exception:
        logger.exception("Error al consultar el modelo LLM")
        return JsonResponse({
            "response": "No pude procesar tu consulta en este momento, intenta de nuevo."
        }, status=502)