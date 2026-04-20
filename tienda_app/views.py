from django.shortcuts import render,get_object_or_404
from django.views import View
from .infra.factories import PaymentFactory
from .services import CompraService
from django . http import HttpResponse
from . models import Libro , Inventario , Orden




class CompraView(View):
    """
    CBV: Vista Basada en Clases.
    Actúa como un "Portero": recibe la petición y delega al servicio.
    """

    template_name = 'tienda_app/compra.html'

    def setup_service(self):
        gateway = PaymentFactory.get_processor()
        return CompraService(procesador_pago=gateway)

    def get(self, request, libro_id):
        servicio = self.setup_service()
        contexto = servicio.obtener_detalle_producto(libro_id)
        return render(request, self.template_name, contexto)

    def post(self, request, libro_id):
        servicio = self.setup_service()
        try:
            total = servicio.ejecutar_compra(libro_id, cantidad=1)
            return render(
                request,
                self.template_name,
                {
                    'mensaje_exito': f"¡Gracias por su compra! Total: ${total}",
                    'total': total,
                },
            )
        except (ValueError, Exception) as e:
            return render(request, self.template_name, {'error': str(e)}, status=400)
        

        import datetime




def compra_rapida_fbv(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)

    if request.method == 'POST':

        # VIOLACION SRP
        inventario = Inventario.objects.get(libro=libro)

        if inventario.cantidad > 0:

            # VIOLACION OCP
            total = float(libro.precio) * 1.19

            # VIOLACION DIP
            with open("pagos_manuales.log", "a") as f:
                f.write(f"[{datetime.datetime.now()}] Pago FBV: ${total}\n")

            inventario.cantidad -= 1
            inventario.save()

            Orden.objects.create(libro=libro, total=total)

            return HttpResponse(f"Compra exitosa: {libro.titulo}")

        else:
            return HttpResponse("Sin stock", status=400)

    total_estimado = float(libro.precio) * 1.19

    return render(request,'tienda_app/compra_rapida.html',
        {
            'libro': libro,
            'total': total_estimado
        }
    )


from django.views import View

class CompraRapidaView(View):

    template_name = 'tienda_app/compra_rapida.html'

    def get(self, request, libro_id):

        libro = get_object_or_404(Libro, id=libro_id)

        total = float(libro.precio) * 1.19

        return render(
            request,
            self.template_name,
            {
                'libro': libro,
                'total': total
            }
        )

    def post(self, request, libro_id):

        libro = get_object_or_404(Libro, id=libro_id)

        gateway = PaymentFactory.get_processor()

        service = CompraService(gateway)

        try:

            total = service.ejecutar_compra(libro_id)

            return HttpResponse(f"Compra exitosa. Total: {total}")

        except Exception as e:

            return HttpResponse(str(e), status=400)


def inventario_view(request):
    """
    Vista para mostrar el inventario actual de todos los libros.
    GET /inventario/
    """
    libros_con_inventario = Libro.objects.prefetch_related('inventario').all()
    
    contexto = {
        'libros': libros_con_inventario,
        'titulo': 'Inventario de Libros'
    }
    
    return render(request, 'tienda_app/inventario.html', contexto)