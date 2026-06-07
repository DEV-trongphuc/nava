import re

fpath = 'f:/BAO_SAPO/sapo_new/sapo_BWT_new/Templates/customers/addresses.bwt'
content = open(fpath, encoding='utf-8').read()

# Match the huge JSON line and replace it
pattern = re.compile(r'var locationData = \{.*?\};', re.DOTALL)
clean_code = '''var locationData = null;
            fetch("{{ 'city.json' | asset_url }}")
                .then(function(res) { return res.json(); })
                .then(function(data) { locationData = data; })
                .catch(function(err) { console.error("Lỗi tải city.json", err); });'''

content = pattern.sub(clean_code, content)
open(fpath, 'w', encoding='utf-8').write(content)
print("Cleaned up successfully!")
