const cartWarp = $('.js-cart');
const cartEmpty = $('.cart__empty');
const cartCount = $('.btn-cart-indicator');
const cartTotal = $('.cart__summary_total');
const regexValue = /\[value]/g;
const cartItemTemplate = document.getElementById('cart-item-template');

function updateCartForm(data, cartClass) {
	let cartContainer = $(cartClass);
	if (cartContainer.length && data.length) {
		cartContainer.empty();
		data.forEach(item => {
			let variantTitle = (item.variant_title === 'Default Title') ?  '' : item.variant_title,
				link_img = item.image || '//bizweb.dktcdn.net/100/434/011/themes/845632/assets/no_image.jpg?1645108680061';
			link_img = link_img.imgUrl('small');
			const instance = document.importNode(cartItemTemplate.content, true);
			instance.querySelectorAll('.js-titlte').forEach(elem => elem.setAttributes({'title': item.title, 'href': item.url, 'html': item.title }));
			instance.querySelectorAll('.js-variant-titlte').forEach(elem => elem.innerHTML = variantTitle);
			instance.querySelectorAll('.js-price').forEach(elem => elem.innerHTML = (item.price > 0) ? formatStoreCurrency.format(item.price * item.quantity) : variantStrings.giftPrice);
			instance.querySelectorAll('.js-quantity').forEach(elem => elem.setAttributes({'value': item.quantity, 'data-variantid': item.variant_id}));
			instance.querySelectorAll('.js-img').forEach(elem => elem.setAttributes({'src': link_img, 'alt': data.title}));
			if(item.price <= 0){
				instance.querySelectorAll('.js-number-input').forEach(elem => elem.classList.add('disabled'));
				instance.querySelectorAll('.js-remove-item-cart').forEach(elem => elem.classList.add('d-none'));
			}
			instance.querySelectorAll('.js-remove-item-cart').forEach(elem => elem.setAttributes({'title': cartStrings.delete, 'data-variantid': item.variant_id, 'html': cartStrings.delete }));
			cartContainer.append(instance);
		}); 
		cartWarp.removeClass('d-none');
		cartEmpty.addClass('d-none');
	} else{
		cartWarp.addClass('d-none');
		cartEmpty.removeClass('d-none');
	}
}
function updateCartInfo(data){
	if(data.item_count > 0){
		cartCount.text((data.item_count > 99) ? '99+' : data.item_count).removeClass('d-none')
	} else {
		cartCount.text('').addClass('d-none');
	}
	cartTotal.html(formatStoreCurrency.format(data.total_price));
}

async function buyNow(e){
	if (typeof e !== 'undefined') e.preventDefault();
	await mewService.clearCart().then(() =>{
		$(document).trigger('changeCart');
	})
	let form = $(this).parents('form');
	let dataForm = new FormData(form[0]);
	let queryString = new URLSearchParams(dataForm).toString();
	mewService.addFromForm(queryString).then(() =>{
		window.location.href = '/checkout';
	}, () => {
		console.log(cartStrings.error)
	}).catch(error => {
		createToast('error', toastString.toastAddErrorTitle, toastString.toastAddErrorMessage);
		console.error('Đã có lỗi xảy ra: ' + error.message);
	}).finally(()=>{
		setTimeout(function(){ 
			$this.prop('disabled', false);
			$this.find('.button__text').toggleClass('fadeOut');
			$this.find('.button__loader').toggleClass('fadeOut');
			createToast('success', toastString.toastAddSuccessTitle, toastString.toastAddSuccessMessage);
		}, 700);
	});
}

async function addToCart(e){
	e.preventDefault();
	let $this = $(this);
	$this.prop('disabled', true);
	let dataForm = new FormData($this.parents('form')[0]);
	let serialFormData = mewService.serializeFormData(dataForm);

	let checkQuantityAvailable = await mewService.checkMaxQuantityAvailable(serialFormData.quantity, serialFormData.variantId, serialFormData.productAlias);
	switch(checkQuantityAvailable.status) {
		case 'inRangeQuantity':
		case 'available':
			dataForm.set('quantity', checkQuantityAvailable.quantity);
			break;
		case 'exceedQuantity':
			createToast('warning', toastString.toastInventoryExccedTitle, toastString.toastInventoryExccedMessage);
			dataForm.set('quantity', checkQuantityAvailable.quantity);
			break;
		case 'maxQuantity':
			createToast('warning', toastString.toastInventoryMaxTitle, toastString.toastInventoryMaxMessage);
			dataForm.set('quantity', checkQuantityAvailable.quantity);
			break;
		case 'unavailable':
			createToast('error', toastString.toastInventoryUnavaiTitle, toastString.toastInventoryUnavaiMessage);
			setTimeout(function(){ 
				$this.prop('disabled', false);
			}, 700);
			return false;
			break;
		case 'error':
		case 'notFound':
			alert(cartStrings.error);
			setTimeout(function(){ 
				$this.prop('disabled', false);
			}, 400);
			return false;
			break;
		default:
	} 

	let queryString = new URLSearchParams(dataForm).toString();
	console.log(queryString);
	mewService.addFromForm(queryString).then(() =>{
		$(document).trigger('changeCart');
	}).catch(error => {
		createToast('error', toastString.toastAddErrorTitle, toastString.toastAddErrorMessage);
		console.error('Đã có lỗi xảy ra: ' + error.message);
	}).finally(()=>{
		setTimeout(function(){ 
			$this.prop('disabled', false);
			createToast('success', toastString.toastAddSuccessTitle, toastString.toastAddSuccessMessage);
		}, 400);
	});
}

$(document).on('click', '.js-step-qty', async function(e){
	e.preventDefault();
	let input = $(this).parents('.number-input').find('input'),
		currentVal = parseInt(input.val()),
		variantId = input.data('variantid');
	if($(this).hasClass('plus')){
		var checkQuantityAvailable = await mewService.checkMaxQuantityAvailable(currentVal + 1, variantId);

		switch(checkQuantityAvailable.status) {
			case 'exceedQuantity':
				createToast('warning', toastString.toastInventoryExccedTitle, toastString.toastInventoryExccedMessage);
				break;
			case 'maxQuantity':
				createToast('warning', toastString.toastInventoryMaxTitle, toastString.toastInventoryMaxMessage);
				break;
			case 'unavailable':
				createToast('error', toastString.toastInventoryUnavaiTitle, toastString.toastInventoryUnavaiMessage);
				return false;
				break;
			case 'error':
				createToast('error', toastString.toastInventoryUnavaiTitle, cartStrings.error);
				return false;
				break;
			default:
		} 
		input.val(checkQuantityAvailable.quantity);
	} else {
		input.val((currentVal - 1 <= 0) ? 0 : currentVal - 1)
	}
	mewService.updateItem(variantId, input.val()).then(() =>{
		$(document).trigger('changeCart');
	})
});

$(document).on('click', '.js-clearcart', function(){
	mewService.clearCart().then(() =>{
		$(document).trigger('changeCart');
	})
})
$(document).on('changeCart', debounce(function(){
	mewService.getCart().then(res => {
		updateCartForm(res.items, '.cart__basket');
		updateCartInfo(res);
	});
}, 300));

$(document).on('click', '.js-remove-item-cart', function(e){
	e.preventDefault();
	let variantId = $(this).data('variantid');
	mewService.updateItem(variantId, 0).then(() =>{
		let variantItem = $(`.variantId-${variantId}`);
		variantItem.addClass('deleted');
		setTimeout(function(){
			variantItem.remove();
		}, 200);
		$(document).trigger('changeCart');
	})
})
$(document).ready(function(){
	$(document).trigger('changeCart');
	$('.js-addToCart').on('click', throttle(addToCart, 200));
	/*$('.js-buynow').on('click', buyNow );*/
	$(".v_more_coupon").on('click', function() {
		$(this).parents('.free-gifts').find('.none_mb').toggleClass('open_gift');
		$(this).find('.t1').toggleClass('d-none');
	});
});