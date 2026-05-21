import re

def check_html_tags(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Remove scripts and styles content
    html_clean = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', html, flags=re.IGNORECASE)
    html_clean = re.sub(r'<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>', '', html_clean, flags=re.IGNORECASE)
    html_clean = re.sub(r'<!--.*?-->', '', html_clean, flags=re.DOTALL)
    
    tags = re.findall(r'<\/?([a-zA-Z0-9:-]+)(?:\s+[^>]*)?>', html_clean)
    
    stack = []
    self_closing = {'img', 'br', 'hr', 'input', 'meta', 'link', 'embed', 'param', 'source', 'track', 'wbr', 'col', 'base', 'area'}
    
    errors = []
    for i, tag in enumerate(tags):
        tag_lower = tag.lower()
        if tag.startswith('/'):
            tag_name = tag_lower[1:]
            if tag_name in self_closing:
                continue
            
            if not stack:
                errors.append(f"Error: Close tag </{tag_name}> found but stack is empty")
                continue
                
            last_open = stack.pop()
            if last_open != tag_name:
                errors.append(f"Mismatch: Expecting </{last_open}>, but found </{tag_name}>.")
                # Put it back to keep checking or do whatever
                stack.append(last_open)
        else:
            if tag_lower.endswith('/') or tag_lower in self_closing:
                continue
            stack.append(tag_lower)
            
    if stack:
        errors.append(f"Unclosed tags at end: {stack}")
        
    if errors:
        print("ERRORS FOUND:")
        for err in errors:
            print(err)
    else:
        print("NO ERRORS FOUND")

check_html_tags('f:/BAO_SAPO/sapo_new/demo_product.html')
