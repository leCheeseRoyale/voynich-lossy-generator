"""
Build complete folio-to-IIIF-image-ID mapping from the manifest data.
Then download a stratified sample of herbal page images for annotation.
"""
import json
import re
import urllib.request
import os
import sys

# Fetch the IIIF manifest
MANIFEST_URL = "https://collections.library.yale.edu/manifests/2002046"

print("Fetching IIIF manifest...")
req = urllib.request.Request(MANIFEST_URL, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    manifest = json.loads(resp.read().decode('utf-8'))

# Extract folio labels and image IDs from canvases
folio_map = {}
canvases = manifest.get('sequences', [{}])[0].get('canvases', [])
if not canvases:
    # Try IIIF v3 structure
    canvases = manifest.get('items', [])

print(f"Found {len(canvases)} canvases")

for canvas in canvases:
    # Get label
    label = canvas.get('label', '')
    if isinstance(label, dict):
        label = label.get('en', [''])[0] if 'en' in label else str(label)
    elif isinstance(label, list):
        label = label[0] if label else ''

    # Get image ID from the image resource URL
    images = canvas.get('images', [])
    if not images:
        items = canvas.get('items', [])
        if items:
            items2 = items[0].get('items', [])
            if items2:
                body = items2[0].get('body', {})
                img_id = body.get('id', '') or body.get('@id', '')
        continue
    else:
        resource = images[0].get('resource', {})
        img_id = resource.get('@id', '') or resource.get('id', '')

    # Extract numeric image ID
    id_match = re.search(r'/(\d+)/', img_id)
    if id_match:
        numeric_id = id_match.group(1)
    else:
        numeric_id = None

    # Normalize folio label: "1r" -> "f1r"
    label_clean = label.strip()
    folio_match = re.match(r'^(\d+[rv]\d?)$', label_clean)
    if folio_match:
        folio_key = f"f{folio_match.group(1)}"
    else:
        folio_key = label_clean

    if numeric_id:
        folio_map[folio_key] = numeric_id

print(f"Mapped {len(folio_map)} folios")

# Save mapping
os.makedirs('data', exist_ok=True)
with open('data/folio_image_map.json', 'w') as f:
    json.dump(folio_map, f, indent=2)

# Show herbal pages with their image IDs
herbal_folios = [
    'f1v','f2r','f2v','f3r','f3v','f4r','f4v','f5r','f5v','f6r','f6v',
    'f7r','f7v','f8r','f8v','f9r','f9v','f10r','f10v','f11r','f11v',
    'f13r','f13v','f14r','f14v','f15r','f15v','f16r','f16v','f17r','f17v',
    'f18r','f18v','f19r','f19v','f20r','f20v','f21r','f21v','f22r','f22v',
    'f23r','f23v','f24r','f24v','f25r','f25v','f26r','f26v','f27r','f27v',
    'f28r','f28v','f29r','f29v','f30r','f30v','f31r','f31v','f32r','f32v',
    'f33r','f33v','f34r','f34v','f35r','f35v','f36r','f36v','f37r','f37v',
    'f38r','f38v','f39r','f39v','f40r','f40v','f41r','f41v','f42r','f42v',
    'f43r','f43v','f44r','f44v','f45r','f45v','f46r','f46v','f47r','f47v',
    'f48r','f48v','f49r','f49v','f50r','f50v','f51r','f51v','f52r','f52v',
    'f53r','f53v','f54r','f54v','f55r','f55v','f56r','f56v','f57r',
    'f65r','f65v','f66v','f87r','f87v','f90r1','f90r2','f90v1','f90v2',
    'f93r','f93v','f94r','f94v','f95r1','f95r2','f95v1','f95v2','f96r','f96v'
]

mapped = 0
missing = []
for f in herbal_folios:
    if f in folio_map:
        mapped += 1
    else:
        missing.append(f)

print(f"\nHerbal pages mapped: {mapped}/{len(herbal_folios)}")
if missing:
    print(f"Missing: {missing}")

# Select stratified sample of 40 for pilot annotation
# Take every 3rd page to spread across the section
import random
random.seed(42)
available = [f for f in herbal_folios if f in folio_map]
# Systematic sample: every ~3rd page
step = max(1, len(available) // 40)
pilot_pages = available[::step][:40]

print(f"\nPilot annotation set ({len(pilot_pages)} pages):")
for f in pilot_pages:
    img_id = folio_map[f]
    url = f"https://collections.library.yale.edu/iiif/2/{img_id}/full/!800,800/0/default.jpg"
    print(f"  {f}: {url}")

# Save pilot list
with open('data/pilot_pages.json', 'w') as f:
    json.dump({p: folio_map[p] for p in pilot_pages}, f, indent=2)

print(f"\nPilot page list saved to data/pilot_pages.json")
