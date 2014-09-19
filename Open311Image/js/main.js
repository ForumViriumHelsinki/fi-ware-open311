/*
  Part of Open311 on Fi-Ware project
  (c) 2014, Juho Vuori

  http://www.forumvirium.fi/

  jshint browser:true
  global MashupPlatform
*/

(function() {

  "use strict";

  function Open311Image() {
  };

  Open311Image.prototype.init = function init() {
    if (window.MashupPlatform) {
      MashupPlatform.wiring.registerCallback("open311Data",this.render.bind(this))
    } else {
      this.render({data:{media_url:"https://asiointi.hel.fi/palautews/rest/v1/attachment/s44qb12472altbo4ut7n"}});
      //this.render({data:{}});
    }
  };

  Open311Image.prototype.render = function (data) {
      var url = data.data.media_url || "images/no-photo.png";
      var $img = $("<img class=\"issue-image\">").attr("src",url);
      $("#content").html($img);
  };

  window.Open311Image = Open311Image;

})();

var open311Image = new Open311Image();
window.addEventListener("load", open311Image.init.bind(open311Image), false);
