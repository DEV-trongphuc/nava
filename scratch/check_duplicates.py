import os

file_path = 'f:/BAO_SAPO/sapo_new/sapo_BWT_new/Templates/product.bwt'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

# Let's see if we have massive blocks that repeat
seen_blocks = {}
block_size = 20 # lines
for i in range(len(lines) - block_size):
    block = "".join(lines[i:i+block_size])
    if block in seen_blocks:
        seen_blocks[block].append(i)
    else:
        seen_blocks[block] = [i]

duplicates = {k: v for k, v in seen_blocks.items() if len(v) > 1}
print(f"Number of duplicate blocks of size {block_size}: {len(duplicates)}")
for k, v in list(duplicates.items())[:5]:
    print(f"Block duplicate at indices: {v}")
    print("--- Block ---")
    print(k[:200] + "...")
    print("-------------")
