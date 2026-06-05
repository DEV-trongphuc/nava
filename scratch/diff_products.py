import difflib

file_orig = 'f:/BAO_SAPO/sapo_new/sapo_BWT_using_no_change_it/Templates/product.bwt'
file_new = 'f:/BAO_SAPO/sapo_new/sapo_BWT_new/Templates/product.bwt'

with open(file_orig, 'r', encoding='utf-8') as f:
    orig_lines = f.readlines()

with open(file_new, 'r', encoding='utf-8') as f:
    new_lines = f.readlines()

diff = difflib.unified_diff(orig_lines, new_lines, fromfile='original', tofile='new', n=0)

added_count = 0
deleted_count = 0
for line in diff:
    if line.startswith('+') and not line.startswith('+++'):
        added_count += 1
    elif line.startswith('-') and not line.startswith('---'):
        deleted_count += 1

print(f"Added lines: {added_count}")
print(f"Deleted lines: {deleted_count}")

# Print first few added blocks
diff = difflib.unified_diff(orig_lines, new_lines, fromfile='original', tofile='new', n=2)
count = 0
for line in diff:
    if line.startswith('+') or line.startswith('-') or line.startswith('@@'):
        print(line.strip())
        count += 1
        if count > 100:
            print("... (truncated)")
            break
