'use strict';
let selectedSortby;
let filter = new Bizweb.SearchFilter();
let selectedFilterWarp = $('.filter-container__selected-filter'),
	filterInput = $('.filter-container input[type=checkbox]'),
	productContainer = $('.category-products');
let inputPriceRangeMin = $('#filter-khoanggia-tu');
let inputPriceRangeMax = $('#filter-khoanggia-den');
let inputPriceRangeStep = 5000000 || 1;
let btnFilterPriceRange = $('.js-filter-pricerange');
let filterRangeText = '';
let wm = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
//var mewCompare = new MewCompare();

const sortByObj = {
	'price-asc': 'price_min:asc', 'price-desc': 'price_min:desc', 'alpha-asc': 'name:asc', 'alpha-desc': 'name:desc', 'created-desc': 'created_on:desc', 'created-asc': 'created_on:asc', 'default': ''
	//'default': sort
}
const sortByClass = {
	'price_min:asc': '.sortby-price-asc', 'price_min:desc': '.sortby-price-desc', 'name:asc': '.sortby-alpha-asc', 'name:desc': '.sortby-alpha-desc', 'created_on:desc': '.sortby-created-desc', 'created_on:asc': '.sortby-created-asc', 'default': '.sortby-default'
}
const regexFilterItem = /\(.*?\)/g;
const regexMinValuev2 = /\s*>=\s*(\d+)/;
const regexMaxValuev2 = /\<=\s*(\d+)/;
const priceRangeInputConfig={allowDecimalPadding:!1,alwaysAllowDecimalCharacter:!0,currencySymbolPlacement:"s",decimalCharacter:",",decimalPlaces:1,decimalPlacesRawValue:0,decimalPlacesShownOnBlur:0,digitGroupSeparator:".",minimumValue:"0",modifyValueOnWheel:!1,outputFormat:"string",integerPos:!0,watchExternalChanges:!0, caretPositionOnFocus: 'end'};
if(colId > 0){
	filter.addValue('collection', 'collections', colId, 'AND');
}
function toggleFilter(e) {
	_toggleFilter(e);
	renderFilteredItems(filterRangeText);
	doSearch(1);
}

function _toggleFilter(e) {
	let $element = $(e);
	let group = $element.attr('data-group');
	let field = $element.attr('data-field');
	let value = $element.attr('value');
	let operator = $element.attr('data-operator');

	if (!$element.is(':checked')) {
		filter.deleteValue(group, field, value, operator);
	} else {
		filter.addValue(group, field, value, operator);
	}
}
function _toggleFilterPriceRange(e) {
	let $element = $(e);
	let group = 'Khoảng giá';
	let field = 'price_min';
	let operator = 'OR';	 
	let value = $element.attr('data-value');
	filter.deleteValuePriceRange(group, field, value, operator);
	filter.addValue(group, field, value, operator);
}
function renderFilteredItems(filterRangeItem) {
	let filteredItemTemplate = '';
	selectedFilterWarp.find('.filter-container__selected-filter-list').empty();

	filterInput.each(function(index) {
		if ($(this).is(':checked')) {
			let id = $(this).attr('id'),
				name = $(this).closest('label').text();
			filteredItemTemplate += `<li class='filter-container__selected-filter-item d-inline-flex align-items-center mr-2 mb-1'><a href='javascript:void(0)' class='p-1 pl-2 rounded' onclick="removeFilteredItem('${id}')">${name} <svg width=18 height=18><use href="#svg-close"></use></svg></a></li>`;
		}
	});

	if(filterRangeItem){
		console.log(filterRangeItem);
		let fitlerTxt = filterRangeItem.replace('AND', '&#8702;').replace('(>=','').replace('<=','').replace(')','');
		filteredItemTemplate += `<li class='filter-container__selected-filter-item d-inline-flex align-items-center mr-2 mb-1'><a href='javascript:void(0)' class='p-1 pl-2 rounded' onclick="removeFilteredRange()">${fitlerTxt} <svg width=18 height=18><use href="#svg-close"></use></svg></a></li>`;
	}
	if(filteredItemTemplate !== ''){
		selectedFilterWarp.find('.filter-container__selected-filter-list').append(filteredItemTemplate);
		selectedFilterWarp.find('.filter-container__selected-filter-list').append(`<li class='filter-container__selected-filter-item d-inline-flex align-items-center'><a href='javascript:void(0)' class='p-1 pl-2 pr-2 rounded' onclick="clearAllFiltered()">Xoá</a></li>`)
		selectedFilterWarp.removeClass('d-none');
	} else{
		selectedFilterWarp.addClass('d-none');
	}
}

function removeFilteredItem(id) {
	$('.filter-container #' + id).trigger('click');
}
function removeFilteredRange() {
	let group = 'Khoảng giá';
	let field = 'price_min';
	let operator = 'OR';	 
	let value = btnFilterPriceRange.attr('data-value');
	filterRangeText = '';
	filter.deleteValuePriceRange(group, field, value, operator);
	inputPriceRangeMin.val('');
	inputPriceRangeMax.val('');
	renderFilteredItems(filterRangeText);
	doSearch(1);
	if(wm < 991){
		$('.open-filters').trigger('click');
	}
	window.addEventListener('resize', throttle( function(){
	}, 200));
}
function clearAllFiltered() {
	filter = new Bizweb.SearchFilter();
	if(colId > 0) filter.addValue('collection', 'collections', colId, 'AND');

	selectedFilterWarp.find('.filter-container__selected-filter-list').empty();
	filterInput.prop('checked', false)
	selectedFilterWarp.addClass('d-none');
	if(filterRangeText != ''){
		removeFilteredRange();
	}
	doSearch(1);
	if(wm < 991){
		$('.open-filters').trigger('click');
	}
	window.addEventListener('resize', throttle( function(){
	}, 200));
}
var doSearch = function(page, options) {
	if(!options) options = {};
	filter.search({view: selectedViewData, page: page, sortby: selectedSortby}).then(res => {
		productContainer.html(res);
		let arrImg = document.querySelector('.category-products').querySelectorAll('.lazy');
		arrImg.forEach((v) => { io.observe(v);})
		pushCurrentFilterState({sortby: selectedSortby, page: page});
		productContainer.find('.js-addToCart').on('click', addToCart);
		scrollToTop(800);
		resortby(selectedSortby);
		mewCompare.init();
		if(window.BPR && window.BPR.loadBadges){
			window.BPR.initDomEls(), window.BPR.loadBadges()
		}
		//if (window.BPR !== undefined){
		//	return window.BPR.initDomEls(), window.BPR.loadBadges();
		//}
	});
}
function sortby(sort) {	
	selectedSortby = sortByObj[sort] || sortByObj.default;
	doSearch(1);
}
function resortby(sort) {
	//console.log($(sortByClass[sort]));
	//$(sortByClass[sort]).prop('selected', true);
	$(sortByClass[sort]).attr('checked', 'checked')
}
function pushCurrentFilterState(options) {

	if(!options) options = {};
	let url = filter.buildSearchUrl(options);
	let queryString = url.slice(url.indexOf('?'));
	if(selectedViewData === 'data_list') { queryString = queryString + '&view=list'	}
	else{ queryString = queryString + '&view=grid'	}

	pushState(queryString);
}

function pushState(url) {
	window.history.pushState({
		turbolinks: true,
		url: url
	}, null, url)
}

function selectFilterByCurrentQuery() {
	let isFilter = false;
	const queryString = decodeURI(window.location.search);
	const filters = queryString.match(regexFilterItem);
	const page = new URL(window.location.href).searchParams.get('page');
	const sortOrder = new URL(window.location.href).searchParams.get('sortby');
	//console.log(sortOrder);
	if(queryString) {
		isFilter = true;
	}
	if(filters && filters.length > 0) {
		filters.forEach(function(item) {
			if(isFilterRange && item.includes('>')){
				//let minValue = regexMinValue.exec(item);
				let minValue = regexMinValuev2.exec(item);
				let maxValue = regexMaxValuev2.exec(item);
				console.log(minValue[1], maxValue[1]);
				if (minValue !== null && maxValue !== null){
					inputPriceRangeMin.val(minValue[1]);
					inputPriceRangeMax.val(maxValue[1]);
				}
				btnFilterPriceRange.attr('data-value', item).trigger('click');
				filterRangeText = item;
				//renderFilteredItems(item);
				doSearch(1);
			} else {
				let element = $(`.aside-content input[value='${item}']`);
				element.attr('checked', 'checked');
				_toggleFilter(element);
			}
		});
		isFilter = true;
	}
	if(sortOrder) {
		//console.log(sortOrder)
		//resortby(sortOrder);
		selectedSortby = sortOrder || sortByObj.default;
	} else {
		resortby('default') 
	}
	if(isFilter && page) {
		doSearch(page);
		renderFilteredItems(filterRangeText);
	}
}
$(function() {
	selectFilterByCurrentQuery();
	
	if(isFilterRange){
		AutoNumeric.multiple(['#filter-khoanggia-tu', '#filter-khoanggia-den'], priceRangeInputConfig); 
	}
	
	let page = new URL(window.location.href).searchParams.get('page');
	console.log(page);
	$(window).on('popstate', function(){
		const pages = page--;
		console.log(pages);
		//doSearch(pages);

	});
});
$(document).on('click', '.open_mnu', function(e) {
  e.preventDefault(); // chặn click ảnh hưởng đến <a>
  $(this).closest('.nav-item').toggleClass('active');
});
$(".filter-item").on('click', 'label', function(){
	$('.sidebar_mobi').removeClass('openf');
	$('.open-filters').removeClass('openf');
	$('#body_overlay').addClass('d-none');
	$('body').removeClass('modal-open');
});
$('.open-filters').on('click', function(e){
	e.stopPropagation();
	$('.sidebar_mobi').toggleClass('openf');
	if ($('.sidebar_mobi').hasClass('openf')){
		$('#body_overlay').removeClass('d-none');
		colLeft.classList.remove("active");
		menuButton.forEach(menu => menu.classList.remove("active"));
		$('body').addClass('modal-open');
	}else {
		$('#body_overlay').addClass('d-none');
		$('body').removeClass('modal-open');
	}
});
$('.view_mores').on('click', 'a', function() {
	if( $(this).hasClass('one') ){
		$(this).addClass('d-none');
		$('.view_mores .two').removeClass('d-none');
	} else {
		$(this).addClass('d-none');
		$('.view_mores .one').removeClass('d-none');
	}
	$('.content_coll').toggleClass('active');
	$('.bg_cl').toggleClass('d-none');
});
if(isFilterRange){
	(btnFilterPriceRange) && inputPriceRangeMin.on('keyup paste', function(e){
		e.preventDefault();
		let priceRangeMin = $(this).val().replace(/\./gi, '');
		if(priceRangeMin && parseInt(priceRangeMin) > 0){
			inputPriceRangeMax.val(parseInt(priceRangeMin) + inputPriceRangeStep);
		} 
	})
	btnFilterPriceRange.on('click', function(e){
		e.preventDefault();
		let priceRangeMin = inputPriceRangeMin.val().replace(/\./gi, '') || '0';
		let priceRangeMax = inputPriceRangeMax.val().replace(/\./gi, '') || '0';
		$(this).attr('data-value','(>='+priceRangeMin+' AND <='+priceRangeMax+')');
		$(this).parents('.aside-item').find('input[type=checkbox]').prop('checked', false);
		_toggleFilterPriceRange($(this));
		filterRangeText = '(>='+priceRangeMin+' AND <='+priceRangeMax+')';
		renderFilteredItems(filterRangeText);
		doSearch(1);
		if(wm < 991){
			$('.sidebar_mobi').removeClass('openf');
			$('.open-filters').removeClass('openf');
			$('#body_overlay').addClass('d-none');
			$('body').removeClass('modal-open');
		}
		//window.addEventListener('resize', throttle( function(){
		//}, 200));
	});
}
var swiperBannerC = new Swiper('.banner_collection', {
	spaceBetween: 10,
	loop: true,
	speed:1000,
	autoplay: {
		delay: 5000,
		disableOnInteraction: true,
	},
	navigation: {
		nextEl: '.mbc_next',
		prevEl: '.mbc_prev',
	},
	breakpoints: {
		0: {
			slidesPerView: 1.2
		},
		576: {
			slidesPerView: 1.5
		},
		768: {
			slidesPerView: 2
		},
		992: {
			slidesPerView: 2
		},
		1200: {
			slidesPerView: 2
		}
	}
});