require([
  'jquery',
  'mockup-patterns-datatables' 
], function($) {
  'use strict';
$(document).ready(function(){
 var ajax_url = $("#ajaxsearch").attr('data-ajax-target');
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
