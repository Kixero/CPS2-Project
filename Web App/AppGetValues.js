var Value = new Vue({


  data: {
    info:[],
    id:null,
    value:null,
    x:null,
    y:null,

  },


  mounted () {
    /*axios
    .get("http://localhost:8080/fuseki/TestCPS2/query?query=SELECT+*+WHERE+%7B+++%3Fsub+%3Fpred+%3Fobj+.+%7D+")
    .then(response => (this.info = response.data))
    .catch(error => console.log(error))
*/
    this.fetchTestData();
    this.getData();
/*
    axios
    .get('https://faircorp-arnaud-patra.cleverapps.io/api/rooms/-12')
    .then(response => {
      this.info = response.data;
      this.time = response.data.floor;
      this.x = response.data.name;
      this.y = response.data.id;
    })
    .catch(error => console.log(error))
    */
  },

  methods: {
      fetchTestData: function () {
          console.log("coucou");
      },
      getData : function(){
        /*axios
        .get("http://localhost:8080/fuseki/TestCPS2/query?query=SELECT+*+WHERE+%7B+++%3Fsub+%3Fpred+%3Fobj+.+%7D+")
        .then(response => (this.info = response.data))
        .catch(error => console.log(error))
        */
        return axios
        .get('https://faircorp-arnaud-patra.cleverapps.io/api/rooms/-12')
        .then(response => {
          this.info = response.data;
          console.log("info = "+this.info.id);
          return this.info;
/*
          this.x = this.info.name;
          this.y = this.info.id;
          console.log("this.x = "+this.x);
*/
        })
        .catch(error => console.log(error))
        //this.info = 'Yo'; //Test


      }
  }

});
