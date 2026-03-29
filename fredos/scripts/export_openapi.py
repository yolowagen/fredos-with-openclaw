import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

def export_openapi():
    # FastAPI generates the OpenAPI schema on demand
    schema = app.openapi()
    
    output_path = "fredos_openapi.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2)
        
    print(f"Successfully exported OpenAPI schema to {output_path}")

if __name__ == "__main__":
    export_openapi()
