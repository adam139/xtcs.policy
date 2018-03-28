(function(e) {
  e.fn.marquee = function(t) {
    function d() {
      if(t.direction == "left") {
        var e = i.scrollLeft();
        if(t.step < 0) {
          i.scrollLeft((e <= 0 ? h : e) + t.step)
        } else {
          i.scrollLeft((e >= h ? 0 : e) + t.step)
        }
        if(e % l === 0) {
          v()
        }
      } else {
        var n = i.scrollTop();
        if(t.step < 0) {
          i.scrollTop((n <= 0 ? p : n) + t.step)
        } else {
          i.scrollTop((n >= p ? 0 : n) + t.step)
        }
        if(n % c === 0) {
          v()
        }
      }
    }
    function v() {
      if(t.pause > 0) {
        var e = t.step;
        t.step = 0;
        setTimeout(function() {
          t.step = e
        }, t.pause)
      }
    }
    t = e.extend({
      speed: parseInt(e(this).attr("data-speed"), 10),
      step: parseInt(e(this).attr("data-step"), 10),
      direction: e(this).attr("data-direction"),
      pause: parseInt(e(this).attr("data-pause"), 10)
    }, t || {});
    var n = jQuery.inArray(t.direction, ["right", "down"]);
    if(n > -1) {
      t.direction = ["left", "up"][n];
      t.step = -t.step
    }
    var r;
    var i = e(this);
    var s = i.innerWidth();
    var o = i.innerHeight();
    var u = e("ul", i);
    var a = e("li", u);
    var f = a.size();
    var l = a.width();
    var c = a.height();
    var h = l * f;
    var p = c * f;
    if(t.direction == "left" && h > s || t.direction == "up" && p > o) {
      if(t.direction == "left") {
        u.width(2 * f * l + 1 * l);
        if(t.step < 0) {
          i.scrollLeft(h)
        }
      } else {
        u.height(2 * f * c);
        if(t.step < 0) {
          i.scrollTop(p)
        }
      }
      u.append(a.clone());
      r = setInterval(d, t.speed);
      i.hover(function() {
        clearInterval(r)
      }, function() {
        r = setInterval(d, t.speed)
      })
    }
  }
})(jQuery)
function rolltext(e) {
  $(e).each(function() {
    $(this).marquee()
    })
}
function MarqueeV(){var a=document.getElementById("oRollV"),b=document.getElementById("oRollV1"),c=document.getElementById("oRollV2");c.offsetTop-a.scrollTop<=0?a.scrollTop-=b.offsetHeight:a.scrollTop++}
function MarqueeVs(){var a=document.getElementById("sRollV"),b=document.getElementById("sRollV1"),c=document.getElementById("sRollV2");c.offsetTop-a.scrollTop<=0?a.scrollTop-=b.offsetHeight:a.scrollTop++}
function StartRollV(){var a=document.getElementById("oRollV"),b=document.getElementById("oRollV1"),c=document.getElementById("oRollV2");if(a){if(parseInt(a.style.height,10)>=c.offsetTop)return void(a.style.height=c.offsetTop);c.innerHTML=b.innerHTML;var d,e=50;d=setInterval(MarqueeV,e),a.onmouseover=function(){clearInterval(d)},a.onmouseout=function(){d=setInterval(MarqueeV,e)}}}
function StartRollVs(){var a=document.getElementById("sRollV"),b=document.getElementById("sRollV1"),c=document.getElementById("sRollV2");if(a){if(parseInt(a.style.height,10)>=c.offsetTop)return void(a.style.height=c.offsetTop);c.innerHTML=b.innerHTML;var d,e=50;d=setInterval(MarqueeVs,e),a.onmouseover=function(){clearInterval(d)},a.onmouseout=function(){d=setInterval(MarqueeVs,e)}}}
