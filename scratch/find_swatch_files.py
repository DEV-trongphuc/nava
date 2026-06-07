import os

base_dir = r"f:\BAO_SAPO\sapo_new"

matches = []
for root, dirs, files in os.walk(base_dir):
    for f_name in files:
        if "swatch" in f_name.lower():
            matches.append(os.path.join(root, f_name))

print("Found files:")
for m in matches:
    print(m)
