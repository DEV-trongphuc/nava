def main():
    with open('scratch/live_cart.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    import re
    match = re.search(r'(<template id="cart-item-template">.*?</template>)', content, re.DOTALL)
    if match:
        print(match.group(1))
    else:
        print("Template not found!")

if __name__ == '__main__':
    main()
