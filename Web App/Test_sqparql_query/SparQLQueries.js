
var http = require('http');

//adding rdflib library : https://github.com/linkeddata/rdflib.js/
const $rdf = require('rdflib');
var store  = $rdf.graph();

var url = "http://localhost:8080/fuseki/TestCPS2/query";

//With sparqlQuery
const sparqlQuery = 'SELECT ?s ?p ?o WHERE { ?s ?p ?o }.';
const query = $rdf.SPARQLToQuery(sparqlQuery, false, store);

store.query(query, function(result) {
  console.log('query ran');
  console.log(result);
});


//Test fetcher :
var timeout = 5000 // 5000 ms timeout
var fetcher = new $rdf.Fetcher(store, timeout)


var uri = "http://localhost:8080/fuseki/TestCPS2/query";
var body = '<a> <b> <c> .'
var mimeType = 'text/turtle'
var store = $rdf.graph()

fetcher.nowOrWhenFetched(url, function(ok, body, xhr) {
    if (!ok) {
        console.log("Oops, something happened and couldn't fetch data");
    } else {
      console.log("Fetcher worked !");

      try {

        console.log("try worked !");

        $rdf.parse(body, store, uri, mimeType)
        console.log(body);

      } catch (err) {
        console.log(err)
      }
    }
})





http.createServer(function (req, res) {
  res.writeHead(200, {'Content-Type': 'text/html'});
  res.end('Hello World!');
}).listen(8081);
