require([
  'jquery',
  'datatables.net',
  'datatables.net-bs',
  'datatables.net-buttons',
  "datatables.net-buttons-colvis",
  "datatables.net-buttons-flash",
  "datatables.net-buttons-html5",
  "datatables.net-buttons-print",
  'datatables.net-buttons-bs',
  'datatables.net-colreorder',
  'datatables.net-rowreorder',
  'datatables.net-fixedcolumns',
  'datatables.net-fixedheader',
  'datatables.net-select'
], function($, Dt) {
  'use strict';
$(document).ready(function(){ 
 $('#datatable').DataTable();
	});
});
