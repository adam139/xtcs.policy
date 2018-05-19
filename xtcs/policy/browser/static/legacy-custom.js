require([
  'jquery'
], function($) {
  'use strict';
$(document).ready(function(){
	$('a[href$="juanzenggongshi"]').on("click",function (e) {
    	  e.preventDefault();
		  var url = $(this).attr("href");
		  window.location.href = url + "/@@donate_listings";
		  return false;
    });	
	var leftHeight = $('.portletNavigationTree dd').height();
	var rightHeight = $('#content').parent().height();
	if((leftHeight) && leftHeight > rightHeight) {
		leftHeight = rightHeight;
		$('.portletNavigationTree dd').height(leftHeight).css("overflow","auto");
		}
	
});
});