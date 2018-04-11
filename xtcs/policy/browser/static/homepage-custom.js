
require([
  'jquery','roll','ajax-fetchimg','bootstrap-carousel','bootstrap-tabs'
], function($,roll,ajaximg,carousel,tabs) {
  'use strict';
$(document).ready(function(){ 
	$(".nav-tabs a").mouseover(function (e) {
		  e.preventDefault();
		  $(this).tab('show');
		});
	$(".nav-tabs").on("click","a",function (e) {
		  e.preventDefault();
		  var url = $(this).attr("data-js-target");
		  window.location.href = url;
		  return false;
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
								
	StartRollV();
	//StartRollVs();
	rolltext(".roll-wrapper");
    var root = $("#roll_chanpin").attr("data-root");
	var ajaxurl = root + "/cishanxiangmu/tuijianxiangmu/@@barsview_mini";
	ajaxfetchimg("roll_chanpin", ajaxurl, ".roll_image", 1);
	});
});