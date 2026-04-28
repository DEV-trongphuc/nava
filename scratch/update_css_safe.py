import re

with open('assets/style.css', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Modify .benefit-card-mini and .b-icon-mini
# Specifically matching the block to avoid replacing everywhere
block1 = """.benefit-card-mini {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    background: var(--bg-white);
    padding: 25px 20px;
    border-radius: var(--radius-md);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
    border: 1px solid var(--border-color);
}

.b-icon-mini {
    font-size: 2rem;
    color: var(--primary);
    background: rgba(0, 51, 102, 0.05);
    width: 55px;
    height: 55px;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 50%;
    flex-shrink: 0;
    margin-bottom: 15px;
}"""

new_block1 = """.benefit-card-mini {
    display: flex;
    flex-direction: row;
    align-items: center;
    text-align: left;
    gap: 15px;
    background: var(--bg-white);
    padding: 25px 20px;
    border-radius: var(--radius-md);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
    border: 1px solid var(--border-color);
}

.b-icon-mini {
    font-size: 2rem;
    color: var(--primary);
    background: rgba(0, 51, 102, 0.05);
    width: 55px;
    height: 55px;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 50%;
    flex-shrink: 0;
    margin-bottom: 0;
}"""

# handle \r\n vs \n
block1_regex = re.compile(re.escape(block1).replace(r'\n', r'\r?\n'))
content = block1_regex.sub(new_block1, content)


# 2. Modify .b-icon-mini in media query
block_media = """    .b-icon-mini {
        width: 45px !important;
        height: 45px !important;
        font-size: 1.5rem !important;
        margin-bottom: 10px !important;
    }"""
new_block_media = """    .b-icon-mini {
        width: 45px !important;
        height: 45px !important;
        font-size: 1.5rem !important;
        margin-bottom: 0 !important;
    }"""
block_media_regex = re.compile(re.escape(block_media).replace(r'\n', r'\r?\n'))
content = block_media_regex.sub(new_block_media, content)

# 3. Modify .product-card .card-actions
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

old_actions_regex = re.compile(re.escape(old_actions).replace(r'\n', r'\r?\n'))
content = old_actions_regex.sub(new_actions, content)

with open('assets/style.css', 'w', encoding='utf-8') as f:
    f.write(content)

print("CSS updated successfully!")
