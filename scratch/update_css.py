import re

with open('assets/style.css', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Modify .benefit-card-mini
content = content.replace(
    '    flex-direction: column;\n    align-items: center;\n    text-align: center;',
    '    flex-direction: row;\n    align-items: center;\n    text-align: left;\n    gap: 15px;'
)

# 2. Modify .b-icon-mini margin-bottom
content = content.replace(
    '    margin-bottom: 15px;',
    '    margin-bottom: 0;'
)

# 3. Modify .b-icon-mini in media query
content = content.replace(
    '    margin-bottom: 10px !important;',
    '    margin-bottom: 0 !important;'
)

# 4. Modify .product-card .card-actions
old_actions = """.product-card .card-actions {
    position: absolute;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%) translateY(20px);
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
    width: 100%;
    display: flex;
    justify-content: center;
    z-index: 20;
}

.product-card:hover .card-actions {
    opacity: 1;
    visibility: visible;
    transform: translateX(-50%) translateY(0);
}"""

new_actions = """.product-card .card-actions {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 20;
}

.product-card .card-actions a {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
    cursor: pointer;
}

.product-card:hover .card-actions {
    /* No hover transform needed */
}"""

# handle \r\n vs \n
old_actions_regex = re.compile(re.escape(old_actions).replace(r'\n', r'\r?\n'))
content = old_actions_regex.sub(new_actions, content)

with open('assets/style.css', 'w', encoding='utf-8') as f:
    f.write(content)

print("CSS updated successfully!")
