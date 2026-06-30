jQuery(document).ready(function($){

    // Smooth scroll — getElementById (jQuery #id fails with diacritics e.g. călătorie)
    $(function () {
      function smoothScrollToHash(hash) {
        if (!hash || hash === '#') {
          return false;
        }
        var id = decodeURIComponent(hash.replace(/^#/, ''));
        var el = document.getElementById(id);
        if (!el) {
          return false;
        }
        $('html, body').animate({
          scrollTop: $(el).offset().top
        }, 1000);
        return true;
      }

      setTimeout(function () {
        if (location.hash) {
          window.scrollTo(0, 0);
          smoothScrollToHash(location.hash);
        }
      }, 1);

      $('a[href*="#"]:not([href="#"])').click(function () {
        if (location.pathname.replace(/^\//, '') === this.pathname.replace(/^\//, '') && location.hostname === this.hostname) {
          if (smoothScrollToHash(this.hash)) {
            if (history.pushState) {
              history.pushState(null, null, this.hash);
            }
            return false;
          }
        }
      });
    });
	
	
	// toggle comments
    // $('.show-comments').on('click', function() {  
	// 	$('#comments').toggleClass('comments--show');		
	// });

	//toggle search
	$('.show-search').on('click', function() {  
		$('.bd-search').toggleClass('search--show');		
	});
    
    // spoilers
     $(document).on('click', '.spoiler', function() {
        $(this).removeClass('spoiler');
     });
    
 });   

// deferred style loading
var loadDeferredStyles = function () {
	var addStylesNode = document.getElementById("deferred-styles");
	var replacement = document.createElement("div");
	replacement.innerHTML = addStylesNode.textContent;
	document.body.appendChild(replacement);
	addStylesNode.parentElement.removeChild(addStylesNode);
};
var raf = window.requestAnimationFrame || window.mozRequestAnimationFrame ||
	window.webkitRequestAnimationFrame || window.msRequestAnimationFrame;
if (raf) raf(function () {
	window.setTimeout(loadDeferredStyles, 0);
});
else window.addEventListener('load', loadDeferredStyles);


// Reset animations on page: body.preload
setTimeout(function(){
	document.body.className="";
},500);

// Open/close navigation when clicked .nav-icon
$(document).ready(function(){
	$('.nav-icon').click(function(){
		$('.nav-icon').toggleClass('active');
	});
	$(".nav-icon").click(function(){
		$("#menu").toggleClass('active');
	});
	$(".nav-icon").click(function(){
		$("#blackover-nav").toggleClass('active');
	});
	$(".nav-icon").click(function(){
		$("body").toggleClass('active-side');
	});
});

// Close navigation when clicked .blackover (Black background)
$(document).ready(function(){
	$("#blackover-nav").click(function(){
		$(".nav-icon").removeClass('active');
	});
	$("#blackover-nav").click(function(){
		$("#menu").removeClass('active');
	});
	$("#blackover-nav").click(function(){
		$("#blackover-nav").removeClass('active');
	});
	$("#blackover-nav").click(function(){
		$("body").removeClass('active-side');
	});
});

// Grid selector Inspiration
$(document).ready(function(){
	$(".grid-selector").click(function(){
		$(".grid-selector").toggleClass('active');
	});
	$(".grid-selector").click(function(){
		$(".post").toggleClass('active');
	});
});

$(document).keyup(function(e) {
	if (e.keyCode == 27) { 
		$(".nav-icon").removeClass('active');
		$("#menu").removeClass('active');
		$("#blackover-nav").removeClass('active');
		$("body").removeClass('active-side');
	}
});


// remove all :hover stylesheets on mobile
function hasTouch() {
return 'ontouchstart' in document.documentElement
		|| navigator.maxTouchPoints > 0
		|| navigator.msMaxTouchPoints > 0;
}

if (hasTouch()) { 
	try {
		for (var si in document.styleSheets) {
			var styleSheet = document.styleSheets[si];
			if (!styleSheet.rules) continue;

			for (var ri = styleSheet.rules.length - 1; ri >= 0; ri--) {
				if (!styleSheet.rules[ri].selectorText) continue;

				if (styleSheet.rules[ri].selectorText.match(':hover')) {
					styleSheet.deleteRule(ri);
				}
			}
		}
	} catch (ex) {}
}


$(document).ready(function(){

    //Check to see if the window is top if not then display button
    $(window).scroll(function(){
        if ($(this).scrollTop() > 300) {
            $('.scroll-top').addClass('active');
        } else {
            $('.scroll-top').removeClass('active');
        }
    });

    //Click event to scroll to top
    $('.scroll-top').click(function(){
        $('html, body').animate({scrollTop : 0},300);
        return false;
    });

});


// DOCS

$(document).ready(function(){
    

     //Check to see if the back-menu is in the div
    $(window).scroll(function(){
        if ($(this).scrollTop() > 130) {
            $('.back-page-button-dark').removeClass('back-page-button-w');
        } else {
            $('.back-page-button-dark').addClass('back-page-button-w');
        }
    });


});

// Custom cursor — cerc cu stroke #42d0ff, fill la hover
$(document).ready(function () {
	if (!window.matchMedia('(pointer: fine)').matches) {
		return;
	}

	var cursor = document.getElementById('custom-cursor');
	if (!cursor) {
		return;
	}

	var hoverSelector = 'a, button, input, textarea, select, label, .nav-icon, .badge, .post-card, .show-search, [href], [role="button"]';

	document.documentElement.classList.add('custom-cursor-enabled');

	document.addEventListener('mousemove', function (e) {
		cursor.style.left = e.clientX + 'px';
		cursor.style.top = e.clientY + 'px';
		cursor.classList.remove('is-hidden');

		var target = document.elementFromPoint(e.clientX, e.clientY);
		if (target && target.closest(hoverSelector)) {
			cursor.classList.add('is-hover');
		} else {
			cursor.classList.remove('is-hover');
		}
	}, { passive: true });

	document.documentElement.addEventListener('mouseleave', function () {
		cursor.classList.add('is-hidden');
	});
});
