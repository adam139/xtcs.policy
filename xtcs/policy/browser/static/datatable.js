require([
  'jquery',
//  'datatables.net-pdfmake',
//  'datatables.net-jszip',
//  'datatables.net-vfs-fonts',
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
  var xianjinTotal;
 $('#datatable').DataTable({
        "order": [[ 3, 'desc' ]],
        "columnDefs": [{ "orderable": false, "targets":[0,1,2] }],
 	"processing": true,
 	"serverSide": true,
// 	 dom: 'Bfrtip',
// 	 buttons: ['copy', 'csv', 'excel', 'pdf', 'print'],
 	"ajax":{
 		'url':ajax_url,
 		'type':'POST',
        "data": function ( d ) {                
             d.xiangmu_id = $('#xiangmuId').val();
             d.total_col = $('#totalCol').val();                
            },
         "dataSrc": function ( data ) {
           xianjinTotal = data.xianjinTotal;
           return data.data;
         }     		
 	},
 	'language':{
 		'url':'http://cdn.datatables.net/plug-ins/1.10.20/i18n/Chinese.json'
 	},
     "drawCallback": function( settings ) {
        var api = this.api();

        $( api.column( 1 ).footer() ).html(
         xianjinTotal +'元'
            );
        }
    }); 
  });
});
