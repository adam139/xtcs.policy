
require([
  'jquery','roll','bootstrap-carousel','bootstrap-tabs'
], function($,roll,carousel,tabs) {
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
	StartRollV();
	StartRollVs();
	rolltext(".roll-wrapper");
	$("#quicksearch").on("click",".searchButton",function(){var a=$("#search_input").val();var b2=encodeURIComponent(a);var base=$("#ajax").attr('data-js-target');window.location.href=base+"/@@allorgnization_listings?orgname="+b2;return false;});$("#search_input").keypress(function(event){if(event.which==13){var a=$("#search_input").val();var b2=encodeURIComponent(a);var base=$("#ajax").attr('data-js-target');window.location.href=base+"/@@allorgnization_listings?orgname="+b2;return false;}});
	});
});