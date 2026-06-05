import subprocess

def main():
    res = subprocess.run(['git', 'diff', 'sapo_BWT_new/Templates/product.bwt'], capture_output=True, text=True, encoding='utf-8')
    with open('scratch/diff_utf8.txt', 'w', encoding='utf-8') as f:
        f.write(res.stdout)
    print("Diff saved to scratch/diff_utf8.txt successfully!")

if __name__ == '__main__':
    main()
