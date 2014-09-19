/*
  Part of Open311 on Fi-Ware project
  (c) 2014, Juho Vuori

  http://www.forumvirium.fi/

  jshint browser:true
  global MashupPlatform
*/

(function() {

  "use strict";

  function Open311Info() {
    moment.locale("fi-FI");
    $.get("popup.html", function(data) {this.popupTemplate = data;Mustache.parse(this.popupTemplate)}.bind(this))
  };

  Open311Info.prototype.init = function init() {
    if (window.MashupPlatform) {
      MashupPlatform.wiring.registerCallback("open311Data",this.render.bind(this))
    } else {
      $.get("dev.json").done(this.render.bind(this));
    }

  };

  Open311Info.prototype.render = function (data) {
      $("#content").html(this.createPopupContent(data.data,data.extraData));
  };

  Open311Info.prototype.createContextAttribute = function (key,value) {
    return {key:key,value:value};
  };
  Open311Info.prototype.createContextAttributes = function (key,value) {
    if (typeof value === "object") {
      var attrs = [];
      for (var k in value) {
        attrs.push.apply(attrs,this.createContextAttributes(key+"."+k,value[k]));
      }
      return attrs
    } else {
      return [this.createContextAttribute(key,value)];
    }
  };

  Open311Info.prototype.addOpen311Attribute = function (context,key,value) {
    var attr = this.createContextAttribute(key,value)
    switch (key) {
      case "type":
      case "id":
        break; //Context Broker specific

      case "service_request_id":
      case "status_notes":
      case "service_name":
      case "service_code":
      case "status":
      case "description":
      case "agency_responsible":
      case "service_notice":
      case "requested_datetime":
      case "updated_datetime":
      case "expected_datetime":
      case "address":
        context.coreOpen311.push(attr)
        break;

      case "position":
        var vals = value.split(",")
        context.coreOpen311.push(this.createContextAttribute('lat',vals[1]))
        context.coreOpen311.push(this.createContextAttribute('lon',vals[0]))
        break;

      case "title":
      case "detailed_status":
      case "service_object_id":
      case "service_object_type":
      case "media_urls":
        context.extendedOpen311.push(attr)
        break;

      default:
        context.extendedOpen311.push(attr)
        console.log("Unknown extra open311 attribute", key);
    }
  };

  Open311Info.prototype.addServiceObjectAttribute = function (context,key,value) {
    var attrs = this.createContextAttributes(key,value);
    for (var i in attrs) {
      context.serviceObject.push(attrs[i])
    }
  };

  Open311Info.prototype.createPopupContent = function (data,extra) {
    var context = {coreOpen311:[],extendedOpen311:[],serviceObject:[]};
    for (var key in data) this.addOpen311Attribute(context,key,data[key])
    for (var key in extra) this.addServiceObjectAttribute(context,key,extra[key])
    return Mustache.render(this.popupTemplate,context);
  };

  window.Open311Info = Open311Info;

})();

var open311Info = new Open311Info();

window.addEventListener("load", open311Info.init.bind(open311Info), false);
