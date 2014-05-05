(function($){

	var mobile = ($(window).width()<768) ? true : false;

	// Click on faces
	$(".persons a").click(
		function(e){
			e.preventDefault();
			var 	_this = $(this),
						currentActive;
			//currentActive = $(".persons").find('.active');

			if (mobile) {
				currentActive = _this.closest(".persons").find('.active');
			}else{
				currentActive = $(".persons").find('.active');
			}

 			// delete the current class
 			currentActive.removeClass('active');

 			// add active to the current elem
 			_this.addClass("active");

		}
	);

	// Popup for the first time only
	if (localStorage.getItem("firstTime") == undefined) {
		$('#green-popup').fadeIn();
		localStorage.setItem("firstTime", "Visited");
	};
	// Click on close button
	$("#green-popup .close").click(
		function(e){
			e.preventDefault();
			$("#green-popup").fadeOut();
		}
	);

})(jQuery);