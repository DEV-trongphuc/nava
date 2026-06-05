import os

path = r"f:\BAO_SAPO\sapo_new\build_demos.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update window.openBottomSheet
old_open_bs = """                window.openBottomSheet = function() {
                    const overlay = document.getElementById('nava-bs-overlay');
                    const bs = document.getElementById('nava-bottom-sheet');
                    const stickyBar = document.getElementById('sticky-cart-bar');
                    
                    if (overlay && bs) {
                        isBsOpen = true;
                        if (stickyBar) {
                            stickyBar.style.setProperty('transform', 'translateY(120%)', 'important');
                        }
                        overlay.style.display = 'block';
                        bs.style.display = 'flex';
                        void overlay.offsetWidth;
                        void bs.offsetWidth;
                        overlay.style.opacity = '1';
                        bs.classList.add('open');
                        document.body.style.overflow = 'hidden';
                        
                        // Hide compare bar when bottom sheet is open
                        if (typeof updateCompareBar === 'function') {
                            updateCompareBar();
                        }
                    }
                };"""

new_open_bs = """                window.openBottomSheet = function() {
                    if (window.innerWidth >= 992) {
                        return; // Don't show bottom-sheet modal on PC/desktop
                    }
                    const overlay = document.getElementById('nava-bs-overlay');
                    const bs = document.getElementById('nava-bottom-sheet');
                    const stickyBar = document.getElementById('sticky-cart-bar');
                    
                    if (overlay && bs) {
                        isBsOpen = true;
                        if (stickyBar) {
                            stickyBar.style.setProperty('transform', 'translateY(120%)', 'important');
                        }
                        overlay.style.display = 'block';
                        bs.style.display = 'flex';
                        void overlay.offsetWidth;
                        void bs.offsetWidth;
                        overlay.style.opacity = '1';
                        bs.classList.add('open');
                        document.body.style.overflow = 'hidden';
                        
                        // Automatically open/expand the dropdown lists on mobile bottom sheet
                        setTimeout(() => {
                            const bsDropdowns = bs.querySelectorAll('.nava-dropdown-wrapper, .nava-custom-select-wrapper, .custom-select-wrapper');
                            bsDropdowns.forEach(w => {
                                w.classList.add('active');
                            });
                        }, 100);

                        // Hide compare bar when bottom sheet is open
                        if (typeof updateCompareBar === 'function') {
                            updateCompareBar();
                        }
                    }
                };"""

if old_open_bs in content:
    content = content.replace(old_open_bs, new_open_bs)
    print("Successfully replaced openBottomSheet in build_demos.py")
else:
    # Let's try with different indentation or whitespace
    # We will do a generic regex replace
    import re
    pattern = r'window\.openBottomSheet\s*=\s*function\(\)\s*\{[\s\S]*?if\s*\(overlay\s*&&\s*bs\)\s*\{[\s\S]*?\}\s*\};'
    match = re.search(pattern, content)
    if match:
        print("Found regex match for openBottomSheet!")
        # Replace the matched string with our new version
        # Let's see the new code to match the indentation of the match
        matched_str = match.group(0)
        # We will determine indentation
        lines = matched_str.split('\n')
        indent = len(lines[0]) - len(lines[0].lstrip())
        new_bs_indented = "\n".join(" " * indent + line.strip() for line in new_open_bs.split('\n'))
        content = content.replace(matched_str, new_bs_indented.strip())
        print("Successfully replaced openBottomSheet using regex")
    else:
        print("Could not find openBottomSheet in build_demos.py!")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
