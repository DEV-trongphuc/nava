import re

def inspect_file(filepath):
    encodings = ['utf-8', 'utf-16', 'utf-16-le', 'utf-16-be', 'latin-1']
    content = ""
    for enc in encodings:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                content = f.read()
                break
        except Exception as e:
            continue
            
    if not content:
        print("Failed to read file.")
        return
        
    # Search for terms and write to a safe file
    targets = ["DANH MỤC SẢN PHẨM", "LỌC GIÁ", "THƯƠNG HIỆU", "danh-muc-san-pham", "filter-sidebar", "sidebar", "col-lg-3"]
    
    with open("scratch/inspect_output.txt", "w", encoding="utf-8") as out:
        out.write(f"File length: {len(content)} characters\n")
        for t in targets:
            matches = [m.start() for m in re.finditer(re.escape(t), content, re.IGNORECASE)]
            out.write(f"Search for '{t}': found {len(matches)} matches\n")
            if matches:
                first_match = matches[0]
                start = max(0, first_match - 200)
                end = min(len(content), first_match + 800)
                out.write(f"Snippet near first match of '{t}':\n")
                out.write(content[start:end])
                out.write("\n" + "="*50 + "\n")
                
    print("Done! Check scratch/inspect_output.txt")

inspect_file("f:\\BAO_SAPO\\sapo_new\\demo_collection.html")
