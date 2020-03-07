require([
  'jquery',
  'mockup-patterns-datatables' 
], function($) {
  'use strict';
// read url query string
$.extend({
  getUrlVars: function(){
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
      hash = hashes[i].split('=');
      vars.push(hash[0]);
      vars[hash[0]] = hash[1];
    }
    return vars;
  },
  getUrlVar: function(name){
    return $.getUrlVars()[name];
  }
});  
  
$(document).ready(function(){
 var ajax_url = $("#ajaxsearch").attr('data-ajax-target');
 var byName = $.getUrlVar('name');
 if (byName === undefined || byName == null || byName === "") { 	 	
  } else {
  	var byName2 = decodeURIComponent(byName);
  	$(".documentFirstHeading").html(byName2);
  }
 var byId = $.getUrlVar('id');  
  if (byId === undefined || byId == null || byId === "") {  	
  } else {
  	$("#xiangmuId").val(byId);
  }
 $('#datatable').DataTable({
 	"processing": true,
 	"serverSide": true,
 	"ajax":{
 		'url':ajax_url,
 		'type':'POST',
        "data": function ( d ) {                
                 d.xiangmu_id = $('#xiangmuId').val();                
            } 		
 	},
 	'language':{
 		'url':'http://cdn.datatables.net/plug-ins/1.10.20/i18n/Chinese.json'
 	},
 });
	});
});
