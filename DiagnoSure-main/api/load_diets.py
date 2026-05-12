import os
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "diagnosure.settings")
django.setup()

from api.models import Disease

def load_diets():
    with open('api/diet.json', 'r', encoding='utf-8') as f:
        diets = json.load(f)

    updated_count = 0
    for diet_entry in diets:
        # Match by exact exact first
        d = Disease.objects.filter(name=diet_entry['name']).first()
        
        if not d:
            # Fallback to fuzzy match
            d = Disease.objects.filter(name__icontains=diet_entry['name'].split('(')[0].strip()).first()
            
        if d:
            d.diet = diet_entry['diet']
            d.save()
            updated_count += 1
        else:
            print(f"WARNING: Could not finding matching database disease for: {diet_entry['name']}")

    print(f"Successfully mapped {updated_count} diets to diseases!")

if __name__ == "__main__":
    load_diets()
