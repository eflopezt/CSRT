#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.append('/workspaces/gestion-personal-nuevo')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from personal.models import Roster, Personal
from collections import Counter

print(f'Personal: {Personal.objects.count()}')
print(f'Roster: {Roster.objects.count()}')
print('\nMuestra de códigos en roster:')
codigos = [r.codigo for r in Roster.objects.all()]
print(Counter(codigos))
print('\nDías libres de personal:')
for p in Personal.objects.all()[:5]:
    count_t = Roster.objects.filter(personal=p, codigo='T').count()
    count_tr = Roster.objects.filter(personal=p, codigo='TR').count()
    print(f'{p.apellidos_nombres}: {p.dias_libres_ganados} días libres (T:{count_t}, TR:{count_tr})')
