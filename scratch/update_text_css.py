import re

with open('assets/style.css', 'r', encoding='utf-8') as f:
    content = f.read()

block_h4 = """.benefit-card-mini h4 {
    font-size: 1.05rem;
    font-weight: 800;
    margin-bottom: 6px;
    line-height: 1.3;
}"""

new_block_h4 = """.benefit-card-mini h4 {
    font-size: 0.95rem;
    font-weight: 800;
    margin-bottom: 4px;
    line-height: 1.3;
    white-space: nowrap;
}"""

block_p = """.benefit-card-mini p {
    font-size: 0.85rem;
    color: var(--text-gray);
    margin: 0;
    line-height: 1.3;
}"""

new_block_p = """.benefit-card-mini p {
    font-size: 0.75rem;
    color: var(--text-gray);
    margin: 0;
    line-height: 1.3;
    white-space: nowrap;
}"""

block_h4_regex = re.compile(re.escape(block_h4).replace(r'\n', r'\r?\n'))
content = block_h4_regex.sub(new_block_h4, content)

block_p_regex = re.compile(re.escape(block_p).replace(r'\n', r'\r?\n'))
content = block_p_regex.sub(new_block_p, content)

with open('assets/style.css', 'w', encoding='utf-8') as f:
    f.write(content)

print("CSS updated successfully!")
