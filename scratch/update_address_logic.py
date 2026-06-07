fpath = 'f:/BAO_SAPO/sapo_new/sapo_BWT_new/Templates/customers/addresses.bwt'
content = open(fpath, encoding='utf-8').read()

# Define the new script block content
js_code = '''    <script>
        document.addEventListener('DOMContentLoaded', function() {
            var locationData = null;
            fetch("{{ 'city.json' | asset_url }}")
                .then(function(res) { return res.json(); })
                .then(function(data) { locationData = data; })
                .catch(function(err) { console.error("Lỗi tải city.json", err); });

            var activeZone = null;
            var currentStep = 1; // 1: City, 2: District/Ward
            var selectedCity = null;
            
            // Open modal when clicking custom trigger field
            $(document).on('click', '.nava-address-trigger', function() {
                activeZone = $(this).attr('data-zone');
                currentStep = 1;
                selectedCity = null;
                $('#address-search').val('');
                renderOptions();
                $('#nava-address-modal').addClass('active');
            });
            
            window.closeAddressModal = function() {
                $('#nava-address-modal').removeClass('active');
            };
            
            window.goBackAddressStep = function() {
                if (currentStep > 1) {
                    currentStep--;
                    $('#address-search').val('');
                    renderOptions();
                }
            };
            
            $('#address-search').on('input', function() {
                renderOptions();
            });
            
            function getCleanCityName(name) {
                var match = name.match(/\[(.*?)\]/);
                return match ? match[1] : name.replace(/\\s*\\(.*?\\)\\s*/g, '').trim();
            }
            
            function waitForOptions(selectEl, callback) {
                var checkCount = 0;
                var interval = setInterval(function() {
                    checkCount++;
                    if (selectEl.find('option').length > 1 || checkCount > 40) {
                        clearInterval(interval);
                        callback();
                    }
                }, 50);
            }
            
            function renderOptions() {
                var listEl = $('#address-list');
                listEl.empty();
                
                if (!locationData) {
                    listEl.html('<div style="padding: 20px; text-align: center; color: var(--text-gray);">Đang tải dữ liệu khu vực...</div>');
                    return;
                }
                
                var query = $('#address-search').val().toLowerCase().trim();
                
                if (currentStep === 1) {
                    $('#nava-modal-title').text('Chọn Tỉnh / Thành phố');
                    $('#nava-modal-footer').hide();
                    
                    var filteredCities = locationData.cities.filter(function(c) {
                        var clean = getCleanCityName(c.name).toLowerCase();
                        var raw = c.name.toLowerCase();
                        return clean.includes(query) || raw.includes(query);
                    });
                    
                    if (filteredCities.length === 0) {
                        listEl.html('<div style="padding: 20px; text-align: center; color: var(--text-gray);">Không tìm thấy</div>');
                        return;
                    }
                    
                    filteredCities.forEach(function(c) {
                        var div = $('<div class="list-item"></div>');
                        div.html('<span>' + getCleanCityName(c.name) + '</span> <i class="ph-bold ph-caret-right" style="color:var(--text-gray)"></i>');
                        div.on('click', function() {
                            selectedCity = c;
                            currentStep = 2;
                            $('#address-search').val('');
                            renderOptions();
                        });
                        listEl.append(div);
                    });
                } else if (currentStep === 2) {
                    $('#nava-modal-title').text('Chọn Quận / Huyện');
                    $('#nava-modal-footer').show();
                    
                    var cleanCityName = getCleanCityName(selectedCity.name);
                    var filteredWards = locationData.wards.filter(function(w) {
                        return w.city === cleanCityName;
                    });
                    
                    if (query) {
                        filteredWards = filteredWards.filter(function(w) {
                            return w.wnew.toLowerCase().includes(query) || (w.wold && w.wold.toLowerCase().includes(query));
                        });
                    }
                    
                    if (filteredWards.length === 0) {
                        listEl.html('<div style="padding: 20px; text-align: center; color: var(--text-gray);">Không tìm thấy</div>');
                        return;
                    }
                    
                    filteredWards.forEach(function(w) {
                        var div = $('<div class="list-item"></div>');
                        div.html('<div><span>' + w.wnew + '</span>' + (w.wold && w.wold !== w.wnew ? '<div class="list-item-sub">(Cũ: ' + w.wold + ')</div>' : '') + '</div> <i class="ph-bold ph-check" style="color:transparent"></i>');
                        div.on('click', function() {
                            closeAddressModal();
                            
                            // 1. Select Province
                            var provinceSelectId = activeZone === 'billing' ? 'mySelect2' : 'mySelect3_' + activeZone;
                            var provinceSelect = $('#' + provinceSelectId);
                            
                            var foundProvinceVal = "";
                            provinceSelect.find('option').each(function() {
                                var optText = $(this).text().toLowerCase();
                                if (optText.includes(cleanCityName.toLowerCase()) || cleanCityName.toLowerCase().includes(optText)) {
                                    foundProvinceVal = $(this).val();
                                }
                            });
                            
                            if (foundProvinceVal) {
                                provinceSelect.val(foundProvinceVal).trigger('change');
                            }
                            
                            // 2. Select District
                            var districtSelectId = activeZone === 'billing' ? 'mySelect3' : 'mySelect4_' + activeZone;
                            var districtSelect = $('#' + districtSelectId);
                            
                            waitForOptions(districtSelect, function() {
                                var foundDistrictVal = "";
                                districtSelect.find('option').each(function() {
                                    var optText = $(this).text().toLowerCase();
                                    if (optText.includes(w.wnew.toLowerCase()) || w.wnew.toLowerCase().includes(optText)) {
                                        foundDistrictVal = $(this).val();
                                    }
                                });
                                
                                if (foundDistrictVal) {
                                    districtSelect.val(foundDistrictVal).trigger('change');
                                } else {
                                    var firstOpt = districtSelect.find('option').eq(1).val();
                                    if (firstOpt) districtSelect.val(firstOpt).trigger('change');
                                }
                                
                                // 3. Select Ward
                                var wardSelectId = activeZone === 'billing' ? 'mySelect4' : 'mySelect5_' + activeZone;
                                var wardSelect = $('#' + wardSelectId);
                                
                                waitForOptions(wardSelect, function() {
                                    var firstWardOpt = wardSelect.find('option').eq(1).val();
                                    if (firstWardOpt) {
                                        wardSelect.val(firstWardOpt).trigger('change');
                                    }
                                });
                            });
                            
                            var displayVal = cleanCityName + ', ' + w.wnew;
                            $('.nava-address-trigger[data-zone="' + activeZone + '"] .nava-address-display')
                                .text(displayVal)
                                .css('color', 'var(--text-dark)');
                        });
                        listEl.append(div);
                    });
                }
            }
        });
    </script>'''

# Replace the old script block with the new one
start_idx = content.find('<script>')
end_idx = content.find('</script>') + len('</script>')

if start_idx != -1 and end_idx != -1:
    new_content = content[:start_idx] + js_code + content[end_idx:]
    open(fpath, 'w', encoding='utf-8').write(new_content)
    print("Addresses logic script updated successfully!")
else:
    print("Script tags not found!")
