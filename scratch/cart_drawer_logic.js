CART DRAWER LOGIC
    // ============================================
    const cartBtn = document.getElementById('header-cart-btn');
    const cartDrawer = document.getElementById('cart-drawer');
    const cartOverlay = document.getElementById('cart-drawer-overlay');
    const cartCloseBtn = document.getElementById('cart-close-btn');
    const cartCountBadge = document.getElementById('cart-count-badge');
    const cartEmptyState = document.getElementById('cart-empty-state');
    const cartLoadingState = document.getElementById('cart-loading-state');
    const cartItemsList = document.getElementById('cart-items-list');
    const cartFooter = document.getElementById('cart-drawer-footer');
    const cartTotalPrice = document.getElementById('cart-total-price');

    const toggleCartDrawer = (show) => {
        if (show) {
            cartDrawer.classList.add('active');
            cartOverlay.classList.add('active');
            document.body.style.overflow = 'hidden';
            loadCartData();
        } else {
            cartDrawer.classList.remove('active');
            cartOverlay.classList.remove('active');
            document.body.style.overflow = '';
        }
    };

    if (cartBtn) {
        cartBtn.addEventListener('click', (e) => {
            e.preventDefault();
            toggleCartDrawer(true);
        });
    }

    if (cartCloseBtn) cartCloseBtn.addEventListener('click', () => toggleCartDrawer(false));
    if (cartOverlay) cartOverlay.addEventListener('click', () => toggleCartDrawer(false));

    // Format currency
    const formatMoney = (amount) => {
        return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(amount);
    };

    const updateCartUI = (cart) => {
        cartLoadingState.style.display = 'none';

        if (!cart || !cart.items || cart.items.length === 0) {
            cartEmptyState.style.display = 'flex';
            cartItemsList.innerHTML = '';
            cartFooter.style.display = 'none';
            if (cartCountBadge) {
                cartCountBadge.style.display = 'none';
                cartCountBadge.textContent = '0';
            }
            return;
        }

        // Has items
        cartEmptyState.style.display = 'none';
        cartFooter.style.display = 'block';

        // Update badge
        if (cartCountBadge) {
            cartCountBadge.style.display = 'flex';
            cartCountBadge.textContent = cart.item_count || cart.items.length;
        }

        // Update total
        if (cartTotalPrice) {
            cartTotalPrice.textContent = formatMoney(cart.total_price);
        }

        // Render items
        cartItemsList.innerHTML = '';
        cart.items.forEach(item => {
            const itemEl = document.createElement('div');
            itemEl.className = 'cart-item';

            // Get proper image or placeholder
            let imgUrl = item.image || 'https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/logo.png';
            if (imgUrl.startsWith('//')) imgUrl = 'https:' + imgUrl;

            itemEl.innerHTML = `
                <img src="${imgUrl}" alt="${item.title}" class="cart-item-img" onerror="this.src='https://bizweb.dktcdn.net/100/543/817/themes/1000289/assets/logo.png'">
                <div class="cart-item-info">
                    <div class="cart-item-title">${item.title}</div>
                    <div class="cart-item-price">${formatMoney(item.price)}</div>
                    <div class="cart-item-actions">
                        <span class="cart-qty">SL: ${item.quantity}</span>
                    </div>
                </div>
            `;
            cartItemsList.appendChild(itemEl);
        });
    };

    const loadCartData = () => {
        cartLoadingState.style.display = 'flex';
        cartEmptyState.style.display = 'none';
        cartItemsList.innerHTML = '';
        cartFooter.style.display = 'none';

        fetch('/cart.js')
            .then(res => res.json())
            .then(cart => {
                updateCartUI(cart);
            })
            .catch(err => {
                console.error('Error fetching cart:', err);
                // Fallback to empty if failed
                updateCartUI(null);
            });
    };

    // Initial check on page load if token exists in localStorage
    if (localStorage.getItem('cart')) {
        fetch('/cart.js')
            .then(res => res.json())
            .then(cart => {
                if (cart && cart.item_count > 0 && cartCountBadge) {
                    cartCountBadge.style.display = 'flex';
                    cartCountBadge.textContent = cart.item_count;
                }
            })
            .catch(err => console.error('Error fetching initial cart data:', err));
    }

});


// ============================================
// 11. SHOPEE REVIEWS REALTIME API
// ============================================
const shopeeList = document.getElementById('shopeeCommentsList');
if (shopeeList) {
  