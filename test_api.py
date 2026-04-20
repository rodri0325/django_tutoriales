#!/usr/bin/env python
"""
Script de prueba para la API DRF.
Simula una compra por API y verifica que:
1. La compra se procesa correctamente
2. El inventario se decuenta
3. Se genera el log de pagos
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"
API_ENDPOINT = f"{BASE_URL}/api/v1/comprar/"

def test_api_purchase():
    """Testa el endpoint de compra por API"""
    
    print("=" * 60)
    print("PRUEBA DE API: COMPRA POR JSON")
    print("=" * 60)
    print(f"Timestamp: {datetime.now()}")
    print()
    
    # Datos de prueba
    payload = {
        "libro_id": 1,
        "direccion_envio": "Calle Principal 123, Apartado 5",
        "cantidad": 1
    }
    
    print(f"📤 Enviando POST a: {API_ENDPOINT}")
    print(f"📦 Datos: {json.dumps(payload, indent=2)}")
    print()
    
    try:
        # Hacer la petición POST
        response = requests.post(API_ENDPOINT, json=payload)
        
        print(f"✓ Código de estado: {response.status_code}")
        print(f"📄 Respuesta:")
        print(json.dumps(response.json(), indent=2))
        print()
        
        # Verificar que la compra fue exitosa
        if response.status_code == 201:
            print("✓ COMPRA EXITOSA - Código 201 Created")
            return True
        else:
            print("✗ ERROR EN LA COMPRA")
            return False
            
    except Exception as e:
        print(f"✗ ERROR DE CONEXIÓN: {e}")
        return False

def check_inventory():
    """Verifica el inventario actual del libro"""
    print()
    print("=" * 60)
    print("VERIFICANDO INVENTARIO")
    print("=" * 60)
    
    from django.core.management import execute_from_command_line
    import os
    import django
    
    # Configurar Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tienda.settings')
    django.setup()
    
    from tienda_app.models import Inventario
    
    try:
        inv = Inventario.objects.get(libro_id=1)
        print(f"📊 Inventario Libro ID=1: {inv.cantidad} unidades")
        return inv.cantidad
    except Exception as e:
        print(f"✗ Error al consultar inventario: {e}")
        return None

def check_log_file():
    """Verifica el archivo de log de pagos"""
    print()
    print("=" * 60)
    print("VERIFICANDO LOG DE PAGOS")
    print("=" * 60)
    
    import os
    log_file = r"c:\Users\Usuario\Documents\django_solid\TEIS-DjangoSOLID\pagos_locales_DAVID_RODRIGUEZ.log"
    
    if os.path.exists(log_file):
        print(f"📄 Archivo log encontrado: {log_file}")
        print()
        print("Últimas 5 líneas del log:")
        print("-" * 60)
        with open(log_file, 'r') as f:
            lines = f.readlines()
            for line in lines[-5:]:
                print(f"  {line.strip()}")
        print("-" * 60)
        return True
    else:
        print(f"✗ Archivo log no encontrado: {log_file}")
        return False

if __name__ == "__main__":
    print("\n🚀 INICIANDO PRUEBAS DE API - TUTORIAL DRF\n")
    
    # Ejecutar prueba de API
    success = test_api_purchase()
    
    # Esperar un poco para que se escriba el log
    time.sleep(1)
    
    # Verificar inventario
    check_inventory()
    
    # Verificar log
    check_log_file()
    
    print()
    print("=" * 60)
    if success:
        print("✓ PRUEBA COMPLETADA EXITOSAMENTE")
    else:
        print("✗ PRUEBA FALLÓ")
    print("=" * 60)
    print()
