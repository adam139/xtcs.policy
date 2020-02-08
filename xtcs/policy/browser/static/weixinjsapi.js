  function setCookie(cname,cvalue,exdays){
    var d = new Date();
    d.setTime(d.getTime()+(exdays*24*60*60*1000));
    var expires = "expires="+d.toGMTString();
    document.cookie = cname + "=" + cvalue + "; " + expires;
  }
function getCookie(cname){
   var name = cname + "=";
   var ca = document.cookie.split(';');
   for(var i=0; i<ca.length; i++){
     var c = ca[i].trim();
     if (c.indexOf(name)==0) return c.substring(name.length,c.length);
    }
    return "";
  }

function getUrlParams (url) {
  var urlParams = new Object();
  // eslint-disable-next-line eqeqeq
  if (url.indexOf('?') != -1) {
      var str = url.substr(1);
      var strs = str.split('&');
      for (var i = 0; i < strs.length; i++) {
        urlParams[strs[i].split('=')[0]] = unescape(strs[i].split('=')[1]);
      }
    }
    return urlParams;
  }
function isEmpty (obj) {
  if (obj === null) return true;
  if (typeof obj === 'undefined') {
    return true;
  }
  if (typeof obj === 'string') {
    if (obj === '') {
      return true;
    }
    var reg = new RegExp('^([ ]+)|([　]+)$');
    return reg.test(obj);
  }
  return false;
  }
function init(base) {
  var url = decodeURIComponent(location.search);
  var params = Object.assign(getUrlParams(url));
  if (isEmpty(params.code)){
    window.location.href = base +"/@@auth.html";
  } 
    // 获取openid
  var data = {'code':params.code};
  $(".ajaxform input[name='code']").attr("value", data);
  var action = base +"/@@token_ajax";
  $.post(action,data,function(res) {        
    if (!isEmpty(res.errcode)&&res.errcode===40029) {
       window.location.href = base +"/@@auth.html";
       } else {
    //setCookie("openid",openid,7200)
    $(".ajaxform input[name='openid']").attr("value", res.openid);
       }
    },'json');
  }

$(document).ready(function(){
	var base = $("#juankuan_workflow").attr('data-ajax-target');
    init(base);
    $(".ajaxform button[name='ok']").on("click",function(base) {
	var aname = $(".ajaxform input[name='name']").val();
	var money = $(".ajaxform input[name='money']").val();
	if (isEmpty(parseFloat(money)))  {
	    alert( "必须输入有效的数字,可以有两位小数" );
		return false;
		}
	var project = $(".ajaxform .radio input:radio[name='project']:checked").val();
	var openid = $(".ajaxform input[name='openid']").val();
	var code = $(".ajaxform input[name='code']").val();
	var data = {'aname':aname,'fee':money,'did':project,'openid':openid,'code':code};
	$.post(base + "/@@pay_ajax",data,function(callback) {
      console.log(JSON.stringify(callback));
      function onBridgeReady(){
      WeixinJSBridge.invoke(
      'getBrandWCPayRequest', {
         "appId":callback.appId,     //公众号名称，由商户传入     
         "timeStamp":callback.timeStamp,         //时间戳，自1970年以来的秒数     
         "nonceStr":callback.nonceStr, //随机串     
         "package":callback.package,     
         "signType":callback.signType,         //微信签名方式：     
         "paySign":callback.paySign //微信签名 
      },
      function(res){
      if(res.err_msg == "get_brand_wcpay_request:ok" ){
      	//var zhifu_result = "ok";
      	//$.post("http://weixin.315ok.org/@@successnotify",
      	//       {"result":zhifu_result},function(callback){  },'json');
        // 使用以上方式判断前端返回,微信团队郑重提示：
        //res.err_msg将在用户支付成功后返回ok，但并不保证它绝对可靠。
      } 
   }); 
 }
if (typeof WeixinJSBridge == "undefined"){
   if( document.addEventListener ){
       document.addEventListener('WeixinJSBridgeReady', onBridgeReady, false);
    }
   else if (document.attachEvent){
       document.attachEvent('WeixinJSBridgeReady', onBridgeReady); 
       document.attachEvent('onWeixinJSBridgeReady', onBridgeReady);
    }
   }
 else{
   onBridgeReady();
 }							
},'json');
		return false;
	});			
}
);