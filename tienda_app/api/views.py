from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from tienda_app.infra.factories import PaymentFactory
from tienda_app.services import CompraService

from .serializers import OrdenInputSerializer


class CompraAPIView(APIView):
    """
    Endpoint para procesar compras via JSON.
    POST /api/v1/comprar/
    Payload: {"libro_id": 1, "direccion_envio": "Calle 123", "cantidad": 1}
    """

    def post(self, request):
        serializer = OrdenInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        datos = serializer.validated_data

        try:
            gateway = PaymentFactory.get_processor()
            servicio = CompraService(procesador_pago=gateway)
            usuario = request.user if request.user.is_authenticated else None
            resultado = servicio.ejecutar_compra(
                libro_id=datos['libro_id'],
                cantidad=datos.get('cantidad', 1),
                direccion=datos['direccion_envio'],
                usuario=usuario,
            )

            return Response(
                {
                    'estado': 'exito',
                    'mensaje': f'Orden creada. Total: {resultado}',
                },
                status=status.HTTP_201_CREATED,
            )

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_409_CONFLICT)
        except Exception:
            return Response({'error': 'Error interno'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class InventarioAPIView(APIView):
    """
    Endpoint para consultar el inventario.
    GET /api/v1/inventario/
    """

    def get(self, request):
        from tienda_app.models import Libro
        
        libros = Libro.objects.prefetch_related('inventario').all()
        inventario_data = []
        
        for libro in libros:
            inventario_data.append({
                'id': libro.id,
                'titulo': libro.titulo,
                'precio': str(libro.precio),
                'stock': libro.inventario.cantidad if hasattr(libro, 'inventario') and libro.inventario else 0
            })
        
        return Response({
            'inventario': inventario_data,
            'total_libros': len(inventario_data),
            'libros_con_stock': sum(1 for item in inventario_data if item['stock'] > 0),
            'libros_sin_stock': sum(1 for item in inventario_data if item['stock'] == 0)
        })
