/*
  Part of Open311 on Fi-Ware project
  (c) 2014, Juho Vuori

  http://www.forumvirium.fi/

  jshint browser:true
  global MashupPlatform
*/

(function() {

  "use strict";

  function myRequest (url, options) {
    var settings = {
      data: options.postBody,
      error:options.onError,
      success:function (data,textStatus,jqXHR) { return options.onSuccess(jqXHR) },
      complete:options.onComplete,
      headers:options.requestHeaders,
      contentType:options.contentType,
      method:options.method
    };
    var params = ""
    for (var k in options.parameters) {
      var separator = params.length == 0 ? '?' : '&'
      params += separator + k + "=" + options.parameters[k]
    }
    return $.ajax(url+params,settings)
  }

  function createIconSet(name) {
    return [
      L.AwesomeMarkers.icon({ icon: name, prefix: 'fa', iconColor: 'white', markerColor: 'green' }),
      L.AwesomeMarkers.icon({ icon: name, prefix: 'fa', iconColor: 'white', markerColor: 'red' }),
      L.AwesomeMarkers.icon({ icon: name, prefix: 'fa', iconColor: 'white', markerColor: 'lightgray' })
    ];
  }

  Open311Map.prototype.selectedMarkerIcon = L.AwesomeMarkers.icon({ markerColor: 'white' })
  Open311Map.prototype.iconSet = {
    "": createIconSet("circle"),
    "171": createIconSet("flask"),       //171 Potholes
    "172": createIconSet("bolt"),        //172 Vandalism
    "174": createIconSet("folder"),      //174 Parks
    "176": createIconSet("cog"),         //176 Graffiti removal
    "180": createIconSet("coffee"),      //180 Other issue to be fixed
    "198": createIconSet("gears"),       //198 Traffic signs
    "199": createIconSet("exclamation"), //199 Info signs
    "211": createIconSet("futbol-o"),    //211 Playgrounds and sports parks
    "246": createIconSet("male")         //246 Sanitation violation
  };

  function Open311Map() {

    // To ease development, we create a mock MashupPlatform if a real one doesn't exits.
    if (!window.MashupPlatform) {
      window.MashupPlatform = {
        wiring: {
          pushEvent: function(eventId,data) {
            console.log("push", eventId, data);
          }
        },
        http: { makeRequest: myRequest }
      };
    }
  }

  Open311Map.prototype.NGSIURL = 'http://130.206.82.148:1234';
  Open311Map.prototype.extraDataURLBase = 'http://130.206.82.148:1235/palvelukarttaws/rest/v2/unit/';

  Open311Map.prototype.init = function init() {

    this.initNGSI();
    this.retrieveNextEntityBatch();
    this.entities = {};

    // initialize map
    //
    this.map = L.map('map').setView([60.17, 24.955], 13);
    //var tiles = 'http://{s}.tiles.mapbox.com/v3/MapID/{z}/{x}/{y}.png';
    var tiles = 'http://a.tile.openstreetmap.org/{z}/{x}/{y}.png';
    L.tileLayer(tiles, {
      attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
      maxZoom: 19
    }).addTo(this.map);

  };
  Open311Map.prototype.queryNGSI = function (entityIdList,attrs,queryOptions) {
    this.ngsi_connection.query(entityIdList, attrs, queryOptions);
  };
  Open311Map.prototype.initNGSI = function () {
    var connection_options = {
      use_user_fiware_token: true,
      requestFunction: myRequest
    };
    this.ngsi_connection = new MyNGSI.Connection(this.NGSIURL, connection_options);
    this.batchQueryOptions = {flat: true, limit: 200, offset: 0, onSuccess: this.entityBatchReceived.bind(this)};
  }

  Open311Map.prototype.oldEntityThreshold = moment().subtract("days",7).format("YYYY-MM-DDThh:mm:ssZZ");
  Open311Map.prototype.getIconFor = function (status,code,datetime) {
      var iconSet = this.iconSet[code]
      if (!iconSet) iconSet = this.iconSet[""]
      if (status === 'open') return iconSet[1]                          // open issue
      else if (datetime < this.oldEntityThreshold) return iconSet[2]    // old closed issue
      else return iconSet[0]                                            // recently closed issue
  }

  Open311Map.prototype.retrieveNextEntityBatch = function () {
    var entityIdList = [{type: 'Open311', id: '.*', isPattern: true}];
    var attributeList = ['position','status','service_code','updated_datetime'];
    this.queryNGSI(entityIdList,attributeList,this.batchQueryOptions);
  };

  Open311Map.prototype.entityBatchReceived = function (data) {
    this.batchQueryOptions.offset += this.batchQueryOptions.limit
    if (Object.keys(data).length > 0) this.retrieveNextEntityBatch();
    var ngsi_subscriptionId = data.subscriptionId;
    for (var id in data) this.createEntityMarker(id,data[id]);
  };

  Open311Map.prototype.createEntityMarker = function (id,obj) {
    try {
      var position = obj.position.split(',').map(function(s){return s.trim();});
      var lat = parseFloat(position[1]);
      var lng = parseFloat(position[0]);
    } catch (e) {
      return; // no location
    }
    var icon = this.getIconFor(obj.status,obj.service_code,obj.updated_datetime)
    if (this.service_codes === undefined) this.service_codes = {};
    this.service_codes[obj.service_code] = obj.service_name
    var marker = L.marker([lat, lng],{entityId:id,icon:icon,preferredIcon:icon}).addTo(this.map);
    this.entities[id] = {detailsLoaded:false,data:obj};
    marker.on('click',this.markerSelected.bind(this));
  };

  Open311Map.prototype.markerSelected = function (e) {

    var marker = e.target;
    var entityId = marker.options.entityId;
    var entityData = this.entities[entityId];

    function dataReceived (data) {
      entityData.data = data[entityId];
      var service_object_id = data[entityId].service_object_id
      if (service_object_id) {
        /*
        MashupPlatform.http.makeRequest(
            this.extraDataURLBase+service_object_id,
            {onSuccess:extraDataReceived.bind(this)} );
        */
        $.ajax(this.extraDataURLBase+service_object_id)
          .done(extraDataReceived.bind(this));
      }
      MashupPlatform.wiring.pushEvent("selectedEntity", entityData)
    }

    function extraDataReceived (extraData) {
      entityData.extraData = extraData
      MashupPlatform.wiring.pushEvent("selectedEntity", entityData)
    }

    // switch marker icon to indicate selection
    if (this.selectedMarker) this.selectedMarker.setIcon(this.selectedMarker.options.preferredIcon);
    marker.setIcon(this.selectedMarkerIcon);
    this.selectedMarker = marker;

    // load extra content for entity
    if (!entityData.detailsLoaded) {
      entityData.detailsLoaded = true; 
      var entityIdList = [{type: 'Open311', id: entityId, isPattern: false}];
      this.queryNGSI(entityIdList, [], {flat: true, onSuccess: dataReceived.bind(this)});
    }
    MashupPlatform.wiring.pushEvent("selectedEntity", entityData)
  };

  window.Open311Map = Open311Map;

})();

var open311Map = new Open311Map();

window.addEventListener("load", open311Map.init.bind(open311Map), false);
