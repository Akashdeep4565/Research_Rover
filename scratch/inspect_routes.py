import os
import re

routes_dir = "backend/app/api/routes"
for fname in sorted(os.listdir(routes_dir)):
    if fname.endswith(".py") and not fname.startswith("__"):
        path = os.path.join(routes_dir, fname)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        endpoints = re.findall(r'@router\.(get|post|put|delete)\(\s*["\']([^"\']+)["\']', content)
        print(f"=== {fname} ===")
        for method, ep in endpoints:
            print(f"  {method.upper():6} {ep}")
