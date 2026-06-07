import os

base_dir = r"f:\BAO_SAPO\sapo_new"

matches = []
for root, dirs, files in os.walk(base_dir):
    for f_name in files:
        if f_name.endswith(".js") or f_name.endswith(".bwt"):
            path = os.path.join(root, f_name)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                for kw in ["OptionSelectors", "OptionSelector", "selectCallback", "Bizweb.Option"]:
                    if kw in content:
                        matches.append((path, kw))
            except Exception:
                pass

print("Found references:")
for m in matches:
    print(m)
