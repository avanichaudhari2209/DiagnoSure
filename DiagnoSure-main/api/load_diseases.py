import json
from api.models import Disease

with open("api/diseases.json") as f:
    data = json.load(f)

for d in data:

    Disease.objects.create(
        name=d.get("name"),
        description=d.get("name"),

        category=d.get("category", "General"),
        severity=d.get("severity", "Medium"),

        symptoms=d.get("symptoms", []),
        precautions=d.get("precautions", []),

        risk_factors=d.get("risk_factors", []),   # 🔥 MUST BE HERE

        contagious=d.get("contagious", False)
    )

print("Diseases loaded successfully ")