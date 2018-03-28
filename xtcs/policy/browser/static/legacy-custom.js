require([
  'jquery'
], function($) {
  'use strict';
$(document).ready(function(){
	var leftHeight = $('.portletNavigationTree dd').height();
	var rightHeight = $('#content').parent().height();
	if((leftHeight) && leftHeight > rightHeight) {
		leftHeight = rightHeight;
		$('.portletNavigationTree dd').height(leftHeight).css("overflow","auto");
		}
	
});
});