
require([
  'jquery','bootstrap-tabs'
], function($,tabs) {
  'use strict';
$(document).ready(function(){ 
	$(".nav-tabs a").mouseover(function (e) {
		  e.preventDefault();
		  $(this).tab('show');
		});

	$(".big-ad").on("click",function (e) {
		  e.preventDefault();
		  var url = $(this).attr("data-target");
		  window.location.href = url;
		  return false;
		});
    $('a[href$="juanzenggongshi"]').on("click",function (e) {
    	  e.preventDefault();
		  var url = $(this).attr("href");
		  window.location.href = url + "/@@donate_listings";
		  return false;
    });	

	});
});