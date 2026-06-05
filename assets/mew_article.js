var swiperRelateBlog = new Swiper('.latest-blog', {
	spaceBetween: 20,
	loop: false,
	speed: 900,
	navigation: {
		nextEl: '.mew_latest_blog_next',
		prevEl: '.mew_latest_blog_prev',
	},
	autoplay: {
		delay: 4000,
		disableOnInteraction: false,
	},
	slidesPerColumnFill: 'row',
	slidesPerColumn: 2,
	breakpoints: {
		375: {
			slidesPerView: 1
		},
		568: {
			slidesPerView: 1
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

$(".open_mnu").on('click', function(){
	$(this).toggleClass('cls_mn').next().toggle();
});
