import re

def main():
    bwt_path = r"sapo_BWT_new/Templates/product.bwt"
    with open(bwt_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    script_blocks = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
    for i, block in enumerate(script_blocks):
        print(f"--- Script block {i+1} ---")
        liquid_tags = re.findall(r'({%.*?%}|{{.*?}})', block)
        for tag in liquid_tags:
            print(tag)

if __name__ == '__main__':
    main()
