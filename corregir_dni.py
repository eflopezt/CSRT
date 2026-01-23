#!/usr/bin/env python
"""
Script para corregir DNIs que perdieron ceros a la izquierda.

Este script ayuda a identificar y corregir DNIs que tienen menos de 8 dígitos,
ya que probablemente perdieron ceros al inicio durante una importación de Excel.

Uso:
    python corregir_dni.py --listar          # Listar DNIs sospechosos
    python corregir_dni.py --corregir        # Aplicar corrección automática a DNIs de 7 dígitos
    python corregir_dni.py --manual          # Modo interactivo para corrección manual
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from personal.models import Personal
from django.db.models import Q
import argparse


def listar_dni_sospechosos():
    """Lista todos los DNIs que tienen menos de 8 dígitos."""
    print("\n" + "="*80)
    print("DNIs SOSPECHOSOS (menos de 8 dígitos)")
    print("="*80 + "\n")
    
    # Buscar DNIs cortos que son solo números
    personal_sospechoso = Personal.objects.all()
    
    sospechosos = []
    for p in personal_sospechoso:
        dni = p.nro_doc
        # Si es numérico y tiene menos de 8 dígitos, es sospechoso
        if dni.isdigit() and len(dni) < 8:
            sospechosos.append(p)
    
    if not sospechosos:
        print("✓ No se encontraron DNIs sospechosos.")
        return []
    
    print(f"Se encontraron {len(sospechosos)} DNIs sospechosos:\n")
    print(f"{'DNI Actual':<12} {'Largo':<8} {'Nombre':<40} {'Estado':<12}")
    print("-" * 80)
    
    for p in sospechosos:
        print(f"{p.nro_doc:<12} {len(p.nro_doc):<8} {p.apellidos_nombres[:40]:<40} {p.estado:<12}")
    
    return sospechosos


def corregir_dni_automatico(dry_run=True):
    """
    Corrige automáticamente DNIs de 7 dígitos añadiendo un cero al inicio.
    
    Args:
        dry_run: Si es True, solo muestra qué se haría sin aplicar cambios.
    """
    print("\n" + "="*80)
    print("CORRECCIÓN AUTOMÁTICA DE DNIs DE 7 DÍGITOS")
    print("="*80 + "\n")
    
    if dry_run:
        print("MODO SIMULACIÓN (no se aplicarán cambios)\n")
    else:
        print("⚠️  APLICANDO CAMBIOS REALES\n")
    
    personal = Personal.objects.all()
    corregidos = []
    
    for p in personal:
        dni = p.nro_doc
        # Solo corregir DNIs numéricos de exactamente 7 dígitos
        if dni.isdigit() and len(dni) == 7:
            nuevo_dni = '0' + dni
            
            # Verificar que no exista otro registro con el nuevo DNI
            if Personal.objects.filter(nro_doc=nuevo_dni).exclude(pk=p.pk).exists():
                print(f"⚠️  No se puede corregir {dni} → {nuevo_dni}: Ya existe otro registro")
                continue
            
            corregidos.append({
                'persona': p,
                'dni_anterior': dni,
                'dni_nuevo': nuevo_dni
            })
            
            if not dry_run:
                p.nro_doc = nuevo_dni
                p.save()
                print(f"✓ Corregido: {dni} → {nuevo_dni} ({p.apellidos_nombres})")
            else:
                print(f"  Corregiría: {dni} → {nuevo_dni} ({p.apellidos_nombres})")
    
    print(f"\nTotal: {len(corregidos)} DNI{'s' if len(corregidos) != 1 else ''} {'corregidos' if not dry_run else 'a corregir'}")
    
    return corregidos


def corregir_dni_manual():
    """Modo interactivo para corregir DNIs manualmente."""
    print("\n" + "="*80)
    print("CORRECCIÓN MANUAL DE DNIs")
    print("="*80 + "\n")
    
    sospechosos = listar_dni_sospechosos()
    
    if not sospechosos:
        return
    
    print("\n" + "="*80)
    print("\nOpciones:")
    print("  - Ingrese el nuevo DNI para corregir")
    print("  - Presione ENTER para omitir")
    print("  - Escriba 'q' para salir")
    print("="*80 + "\n")
    
    corregidos = 0
    
    for p in sospechosos:
        print(f"\nPersonal: {p.apellidos_nombres}")
        print(f"DNI actual: {p.nro_doc} ({len(p.nro_doc)} dígitos)")
        print(f"Estado: {p.estado}")
        if p.subarea:
            print(f"SubÁrea: {p.subarea}")
        
        while True:
            respuesta = input("\nNuevo DNI (o ENTER/q): ").strip()
            
            if respuesta.lower() == 'q':
                print(f"\nTotal corregidos: {corregidos}")
                return
            
            if not respuesta:
                break
            
            # Validar el nuevo DNI
            if not respuesta.isdigit():
                print("❌ Error: El DNI debe contener solo números")
                continue
            
            if len(respuesta) not in [8, 9]:
                print("⚠️  Advertencia: DNI no tiene 8 o 9 dígitos")
                confirmar = input("¿Continuar de todos modos? (s/N): ").strip().lower()
                if confirmar != 's':
                    continue
            
            # Verificar duplicados
            if Personal.objects.filter(nro_doc=respuesta).exclude(pk=p.pk).exists():
                print(f"❌ Error: Ya existe otro registro con DNI {respuesta}")
                continue
            
            # Aplicar corrección
            dni_anterior = p.nro_doc
            p.nro_doc = respuesta
            p.save()
            print(f"✓ DNI actualizado: {dni_anterior} → {respuesta}")
            corregidos += 1
            break
    
    print(f"\n{'='*80}")
    print(f"Total corregidos: {corregidos}")
    print("="*80 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='Herramienta para corregir DNIs que perdieron ceros a la izquierda',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python corregir_dni.py --listar
  python corregir_dni.py --corregir --dry-run
  python corregir_dni.py --corregir
  python corregir_dni.py --manual
        """
    )
    
    parser.add_argument(
        '--listar',
        action='store_true',
        help='Listar DNIs sospechosos (menos de 8 dígitos)'
    )
    
    parser.add_argument(
        '--corregir',
        action='store_true',
        help='Corregir automáticamente DNIs de 7 dígitos añadiendo un cero'
    )
    
    parser.add_argument(
        '--manual',
        action='store_true',
        help='Modo interactivo para corrección manual'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simular corrección sin aplicar cambios (solo con --corregir)'
    )
    
    args = parser.parse_args()
    
    # Si no se especifica ninguna opción, mostrar ayuda
    if not (args.listar or args.corregir or args.manual):
        parser.print_help()
        return
    
    try:
        if args.listar:
            listar_dni_sospechosos()
        
        if args.corregir:
            corregir_dni_automatico(dry_run=args.dry_run)
            
            if args.dry_run:
                print("\n⚠️  Para aplicar los cambios, ejecute sin --dry-run:")
                print("   python corregir_dni.py --corregir")
        
        if args.manual:
            corregir_dni_manual()
    
    except KeyboardInterrupt:
        print("\n\nOperación cancelada por el usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
