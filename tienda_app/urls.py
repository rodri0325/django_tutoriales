from django.urls import path
from .api.views import CompraAPIView
from .api.views import InventarioAPIView
from .views import CompraView
from .views import compra_rapida_fbv
from .views import CompraRapidaView
from .views import inventario_view

urlpatterns = [
    # Usamos .as_view() para habilitar la CBV
    path('compra/<int:libro_id>/', CompraView.as_view(), name='finalizar_compra'),
    path('api/v1/comprar/', CompraAPIView.as_view(), name='api_comprar'),
    path('api/v1/inventario/', InventarioAPIView.as_view(), name='api_inventario'),
    path('compra-rapida/<int:libro_id>/', compra_rapida_fbv, name='compra_rapida_fbv'),
    path('cbv/compra-rapida/<int:libro_id>/', CompraRapidaView.as_view(), name='compra_rapida_cbv'),
    path('inventario/', inventario_view, name='inventario'),
]
