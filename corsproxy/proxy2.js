var http_proxy = require("http-proxy");
createCorsProxy("http://www.hel.fi",1235)

function createCorsProxy(target,sourcePort) {
	var cors_proxy = require("corsproxy");
	cors_proxy.options = { target: target };
	http_proxy.createServer(cors_proxy).listen(sourcePort);
	console.log("Listening on port " + sourcePort)
}
