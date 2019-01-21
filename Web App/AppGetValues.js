var Value = new Vue({


  data: {
    info:[],
    id:null,
    value:null,
    x:null,
    y:null,

  },


  mounted () {
    this.getData();
  },

  methods: {

      //Return Temperature
      getTempData : function(){
        return axios
        //URL not perfect but works  TODO : change url
        .get('http://localhost:8080/fuseki/TestCPS2/query?query=PREFIX+rdf%3A+++++%3Chttp%3A%2F%2Fwww.w3.org%2F1999%2F02%2F22-rdf-syntax-ns%23%3E+%0D%0APREFIX+rdfs%3A++++%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E+%0D%0APREFIX+xsd%3A+++++%3Chttp%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema%23%3E+%0D%0APREFIX+sosa%3A++++%3Chttp%3A%2F%2Fwww.w3.org%2Fns%2Fsosa%2F%3E+%0D%0APREFIX+cdt%3A+++++%3Chttp%3A%2F%2Fw3id.org%2Flindt%2Fcustom_datatypes%23%3E+%0D%0APREFIX+geo%3A+++++%3Chttp%3A%2F%2Fwww.w3.org%2F2003%2F01%2Fgeo%2Fwgs84_pos%23%3E+%0D%0APREFIX+geom%3A++%3Chttp%3A%2F%2Fdata.ign.fr%2Fdef%2Fgeometrie%2F%3E+%0D%0ABase+%3Chttp%3A%2F%2Flocalhost%3A8080%3E%0D%0ASELECT+%3Fx+%3Fy+%3Ftime+%3Ftemp+WHERE+%7B%0D%0A++%3Fobs+sosa%3AhasSimpleResult+%3Ftemp.%0D%0A++%3Fobs+sosa%3AobservedProperty+%3Ctemperature%3E.%0D%0A++%3Fobs+sosa%3AhasFeatureOfInterest++%5B+geo%3Alat+++%3Flat+%3B%0D%0A++++++++++++++++++++++++++++++++++++geo%3Along++%3Flong+%3B+%0D%0A++++++++++++++++++++++++++++++++++++geom%3Ax+%3Fx%3B%0D%0A++++++++++++++++++++++++++++++++++++geom%3Ay+%3Fy+%5D+.%0D%0A++%3Fobs+sosa%3AresultTime+%3Ftime+.%0D%0A%7DORDER+BY+DESC%28%3Ftime%29+LIMIT+1')
        .then(response => {
          this.info = response.data;
          return this.info;
        })
        .catch(error => console.log(error))
      },

      //Return Humidity
      getHumData : function(){
        return axios
        //URL not perfect but works  TODO : change url
        .get('http://localhost:8080/fuseki/TestCPS2/query?query=PREFIX+rdf%3A+++++%3Chttp%3A%2F%2Fwww.w3.org%2F1999%2F02%2F22-rdf-syntax-ns%23%3E+%0D%0APREFIX+rdfs%3A++++%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E+%0D%0APREFIX+xsd%3A+++++%3Chttp%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema%23%3E+%0D%0APREFIX+sosa%3A++++%3Chttp%3A%2F%2Fwww.w3.org%2Fns%2Fsosa%2F%3E+%0D%0APREFIX+cdt%3A+++++%3Chttp%3A%2F%2Fw3id.org%2Flindt%2Fcustom_datatypes%23%3E+%0D%0APREFIX+geo%3A+++++%3Chttp%3A%2F%2Fwww.w3.org%2F2003%2F01%2Fgeo%2Fwgs84_pos%23%3E+%0D%0APREFIX+geom%3A++%3Chttp%3A%2F%2Fdata.ign.fr%2Fdef%2Fgeometrie%2F%3E+%0D%0ABase+%3Chttp%3A%2F%2Flocalhost%3A8080%3E%0D%0ASELECT+%3Fx+%3Fy+%3Ftime+%3Fhum+WHERE+%7B%0D%0A++%3Fobs+sosa%3AhasSimpleResult+%3Fhum.%0D%0A++%3Fobs+sosa%3AobservedProperty+%3Chumidity%3E.%0D%0A++%3Fobs+sosa%3AhasFeatureOfInterest++%5B+geo%3Alat+++%3Flat+%3B%0D%0A++++++++++++++++++++++++++++++++++++geo%3Along++%3Flong+%3B+%0D%0A++++++++++++++++++++++++++++++++++++geom%3Ax+%3Fx%3B%0D%0A++++++++++++++++++++++++++++++++++++geom%3Ay+%3Fy+%5D+.%0D%0A++%3Fobs+sosa%3AresultTime+%3Ftime+.%0D%0A%7DORDER+BY+DESC%28%3Ftime%29+LIMIT+1')
        .then(response => {
          this.info = response.data;
          return this.info;
        })
        .catch(error => console.log(error))
      },

      //Return Luminosity
      getLumData : function(){
        return axios
        //URL not perfect but works  TODO : change url
        .get('http://localhost:8080/fuseki/TestCPS2/query?query=PREFIX+rdf%3A+++++%3Chttp%3A%2F%2Fwww.w3.org%2F1999%2F02%2F22-rdf-syntax-ns%23%3E+%0D%0APREFIX+rdfs%3A++++%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E+%0D%0APREFIX+xsd%3A+++++%3Chttp%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema%23%3E+%0D%0APREFIX+sosa%3A++++%3Chttp%3A%2F%2Fwww.w3.org%2Fns%2Fsosa%2F%3E+%0D%0APREFIX+cdt%3A+++++%3Chttp%3A%2F%2Fw3id.org%2Flindt%2Fcustom_datatypes%23%3E+%0D%0APREFIX+geo%3A+++++%3Chttp%3A%2F%2Fwww.w3.org%2F2003%2F01%2Fgeo%2Fwgs84_pos%23%3E+%0D%0APREFIX+geom%3A++%3Chttp%3A%2F%2Fdata.ign.fr%2Fdef%2Fgeometrie%2F%3E+%0D%0ABase+%3Chttp%3A%2F%2Flocalhost%3A8080%3E%0D%0A%0D%0ASELECT+%3Fx+%3Fy+%3Ftime+%3Flum+WHERE+%7B%0D%0A++%3Fobs+sosa%3AhasSimpleResult+%3Flum.%0D%0A++%3Fobs+sosa%3AobservedProperty+%3Cluminosity%3E.%0D%0A++%3Fobs+sosa%3AhasFeatureOfInterest++%5B+geo%3Alat+++%3Flat+%3B%0D%0A++++++++++++++++++++++++++++++++++++geo%3Along++%3Flong+%3B+%0D%0A++++++++++++++++++++++++++++++++++++geom%3Ax+%3Fx%3B%0D%0A++++++++++++++++++++++++++++++++++++geom%3Ay+%3Fy+%5D+.%0D%0A++%3Fobs+sosa%3AresultTime+%3Ftime+.%0D%0A%7DORDER+BY+DESC%28%3Ftime%29+LIMIT+1')
        .then(response => {
          this.info = response.data;
          return this.info;
        })
        .catch(error => console.log(error))
      },

      //Return sound
      getSndData : function(){
        return axios
        //URL not perfect but works TODO : change url
        .get('http://localhost:8080/fuseki/TestCPS2/query?query=PREFIX+rdf%3A+++++%3Chttp%3A%2F%2Fwww.w3.org%2F1999%2F02%2F22-rdf-syntax-ns%23%3E+%0D%0APREFIX+rdfs%3A++++%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E+%0D%0APREFIX+xsd%3A+++++%3Chttp%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema%23%3E+%0D%0APREFIX+sosa%3A++++%3Chttp%3A%2F%2Fwww.w3.org%2Fns%2Fsosa%2F%3E+%0D%0APREFIX+cdt%3A+++++%3Chttp%3A%2F%2Fw3id.org%2Flindt%2Fcustom_datatypes%23%3E+%0D%0APREFIX+geo%3A+++++%3Chttp%3A%2F%2Fwww.w3.org%2F2003%2F01%2Fgeo%2Fwgs84_pos%23%3E+%0D%0APREFIX+geom%3A++%3Chttp%3A%2F%2Fdata.ign.fr%2Fdef%2Fgeometrie%2F%3E+%0D%0ABase+%3Chttp%3A%2F%2Flocalhost%3A8080%3E%0D%0A%0D%0ASELECT+%3Fx+%3Fy+%3Ftime+%3Fsnd+WHERE+%7B%0D%0A++%3Fobs+sosa%3AhasSimpleResult+%3Fsnd.%0D%0A++%3Fobs+sosa%3AobservedProperty+%3Csound%3E.%0D%0A++%3Fobs+sosa%3AhasFeatureOfInterest++%5B+geo%3Alat+++%3Flat+%3B%0D%0A++++++++++++++++++++++++++++++++++++geo%3Along++%3Flong+%3B+%0D%0A++++++++++++++++++++++++++++++++++++geom%3Ax+%3Fx%3B%0D%0A++++++++++++++++++++++++++++++++++++geom%3Ay+%3Fy+%5D+.%0D%0A++%3Fobs+sosa%3AresultTime+%3Ftime+.%0D%0A%7DORDER+BY+DESC%28%3Ftime%29+LIMIT+1')
        .then(response => {
          this.info = response.data;
          return this.info;
        })
        .catch(error => console.log(error))
      }

  }

});
