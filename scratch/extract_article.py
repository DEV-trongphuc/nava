import os
from bs4 import BeautifulSoup

def extract():
    src_path = r"C:\Users\AD\.gemini\antigravity-ide\brain\03370dae-95d0-4353-967c-5822634bf864\.system_generated\steps\259\content.md"
    if not os.path.exists(src_path):
        print("Source file not found")
        return
        
    with open(src_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    soup = BeautifulSoup(content, 'html.parser')
    
    # Extract the main section (optional, just to save the full section)
    section = soup.find('section', class_='col2-right-layout')
    if section:
        os.makedirs("scratch", exist_ok=True)
        with open("scratch/extracted_article_content.html", "w", encoding="utf-8") as f:
            f.write(str(section))
        print("Extracted section successfully!")
    else:
        print("Section col2-right-layout not found")
        
    # Extract the entry-content contents
    entry = soup.find('div', class_='entry-content')
    if entry:
        # Get the inner HTML
        inner_html = entry.decode_contents()
        with open("scratch/m_content_art.html", "w", encoding="utf-8") as f:
            f.write(inner_html.strip())
        print("Extracted entry-content successfully using BeautifulSoup!")
    else:
        print("entry-content div not found")

if __name__ == "__main__":
    extract()
