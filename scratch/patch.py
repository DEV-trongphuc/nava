import re

def patch():
    file_path = 'f:/BAO_SAPO/sapo_new/build_demos.py'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. margin-top for collection-hero
    content = re.sub(
        r'margin-top: 25px;',
        r'margin-top: 60px;',
        content
    )
    
    # 2. compare-page padding
    content = re.sub(
        r'\.compare-page \{ padding: 40px 15px; max-width: 1200px; margin: 40px auto; \}',
        r'.compare-page { padding: 20px 15px; max-width: 1200px; margin: 10px auto; }',
        content
    )
    
    # 3. Remove "Khám phá sự khác biệt" (not found previously, but just in case)
    content = re.sub(
        r'<p[^>]*>Khám phá sự khác biệt.*?<\/p>',
        r'',
        content
    )
    
    # 4. Product Page Mockup (replace Datasheet section)
    with open('f:/BAO_SAPO/sapo_new/scratch/product_desc.html', 'r', encoding='utf-8') as f:
        desc_html = f.read()
    
    # In build_demos.py, the product page tabs start at <div class="nava-tabs">
    # We will replace from <div class="nava-tabs"> ... to the end of the product detail section.
    # The end of the section is just before <!-- Recommended Products Section -->
    # Actually, let's just replace the whole <div class="col-left"> of product details? No, it's safer to regex match the specific part.
    
    content = re.sub(
        r'<!-- Product Info Tabs -->.*?<!-- Recommended Products Section -->',
        '<!-- Product Details from NavaStore -->\n              <div style="background: #fff; padding: 20px; border-radius: 12px; margin-bottom: 40px; box-shadow: 0 4px 20px rgba(0,0,0,0.03); overflow: hidden;">\n' + desc_html.replace('\\', '\\\\') + '\n              </div>\n              <!-- Recommended Products Section -->',
        content,
        flags=re.DOTALL
    )
    
    # 5. Address Modal logic in checkout
    # Move modal to body
    content = re.sub(
        r'function openAddressModal\(\) \{',
        r'function openAddressModal() {\n            const modal = document.getElementById("address-modal");\n            if (modal && modal.parentNode !== document.body) { document.body.appendChild(modal); }',
        content
    )
    
    # Add step 3 to goBackAddressStep
    content = re.sub(
        r'if \(addressStep === 2\) \{',
        r'if (addressStep === 3) { addressStep = 2; document.querySelector(".modal-search").style.display = "block"; renderAddressList(); } else if (addressStep === 2) {',
        content
    )
    
    # Update step 3 trigger in ward select
    content = re.sub(
        r'selectedWard = w;\n.*?addressStep = 2;\n.*?if\(searchInput\) searchInput.value = \'\';\n.*?renderAddressList\(\);',
        r'selectedWard = w;\n                        addressStep = 3;\n                        if(searchInput) searchInput.value = \'\';\n                        renderAddressList();',
        content
    )
    
    # Add addressStep === 3 logic in renderAddressList
    step3_logic = r'''            } else if (addressStep === 3) {
                document.getElementById('modal-title').textContent = 'Số nhà & Đường';
                const sContainer = document.querySelector('.modal-search');
                if(sContainer) sContainer.style.display = 'none';
                listEl.innerHTML = `
                    <div style="padding: 20px;">
                        <input type="text" id="street-input" class="nava-input" placeholder="VD: Số 123 đường ABC" style="margin-bottom: 15px; width: 100%; box-sizing: border-box; background: var(--bg-gray);">
                        <button class="action-btn" style="width: 100%; border:none; background: var(--primary); color: #fff; font-weight: 700; height: 48px; border-radius: 12px; cursor: pointer;" onclick="confirmAddress()">Xác nhận địa chỉ</button>
                    </div>
                `;
'''
    
    content = re.sub(
        r'(\} else if \(addressStep === 2\) \{.*?)(?=\n            \}\n\n        \})',
        r'\1' + '\n' + step3_logic,
        content,
        flags=re.DOTALL
    )

    # confirmAddress function
    confirm_func = r'''
        function confirmAddress() {
            const street = document.getElementById('street-input').value;
            if(!street) { alert('Vui lòng nhập số nhà & đường'); return; }
            const fullAddress = street + ', ' + selectedWard.wnew + ', ' + getCleanCityName(selectedCity.name);
            document.getElementById('address-display').textContent = fullAddress;
            document.getElementById('address-display').style.color = 'var(--text-dark)';
            closeAddressModal();
        }
    '''
    content = re.sub(
        r'function renderAddressList\(\) \{',
        confirm_func + '\n        function renderAddressList() {',
        content
    )
    
    # Hide the extra street input
    content = re.sub(
        r'<div class="input-group">\s*<input type="text" class="nava-input" placeholder="S.*?nh.*?, T.*?n.*?" value=".*?">\s*</div>',
        '',
        content
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched successfully")

if __name__ == '__main__':
    patch()
