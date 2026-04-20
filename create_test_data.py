#!/usr/bin/env python
"""
Script para crear datos de prueba para el tutorial DRF.
Ejecutar: python manage.py shell < create_test_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tienda.settings')
django.setup()

from tienda_app.models import Libro, Inventario
from django.contrib.auth.models import User

# Crear usuario de prueba
user, created = User.objects.get_or_create(
    username='testuser',
    defaults={'email': 'test@example.com'}
)
if created:
    user.set_password('test123')
    user.save()
    print(f"✓ Usuario creado: {user.username}")
else:
    print(f"✓ Usuario existente: {user.username}")

# Crear libros de prueba
libros_data = [
    {'titulo': 'Clean Code', 'precio': 45.99},
    {'titulo': 'Design Patterns', 'precio': 55.50},
    {'titulo': 'Refactoring', 'precio': 40.00},
]

for data in libros_data:
    libro, created = Libro.objects.get_or_create(
        titulo=data['titulo'],
        defaults={'precio': data['precio']}
    )
    
    # Crear inventario
    inventario, inv_created = Inventario.objects.get_or_create(
        libro=libro,
        defaults={'cantidad': 100}
    )
    
    if created:
        print(f"✓ Libro creado: {libro.titulo} - ${libro.precio}")
    if inv_created:
        print(f"  Inventario: {inventario.cantidad} unidades")

print("\n✓ Datos de prueba creados exitosamente")
