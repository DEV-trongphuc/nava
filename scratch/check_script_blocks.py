import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/live_scripts.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

def find_script_block(line_num):
    # Duyệt ngược từ line_num lên để tìm tiêu đề SCRIPT block
    for i in range(line_num - 1, -1, -1):
        if "=========================================" in lines[i] and "SCRIPT" in lines[i+1]:
            return lines[i+1].strip()
    return "Unknown Script"

print(f"Line 2505 (syncSwatches call) is in: {find_script_block(2505)}")
print(f"Line 4052 (window.mainProductAvailable definition) is in: {find_script_block(4052)}")
