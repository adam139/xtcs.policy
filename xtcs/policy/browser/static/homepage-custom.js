
require([
  'jquery','roll','ajax-fetchimg','bootstrap-carousel','bootstrap-tabs'
], function($,roll,ajaximg,carousel,tabs) {
  'use strict';
$(document).ready(function(){
	var root = $("#roll_chanpin").attr("data-root"); 
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
	$("#juanzengfangshi").on("click","div",function (e) {
		  e.preventDefault();
		  var url = root + "/aixinjuanzeng/aixinjuankuan/@@donated_workflow";
		  window.location.href = url;
		  return false;
		});		
		
	$(".big-ad").on("click",function (e) {
		  e.preventDefault();
		  var url = $(this).attr("data-target");
		  window.location.href = url;
		  return false;
		});
    $('.carousel').carousel();						
	StartRollV();
	//StartRollVs();
	//rolltext(".roll-wrapper");    
	var ajaxurl = root + "/cishanxiangmu/tuijianxiangmu/@@barsview_mini";
	ajaxfetchimg("roll_chanpin", ajaxurl, ".roll_image", 1);
	});
});