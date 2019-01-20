var Value = new Vue({

  el:'#appGetValue',

  data: {
    info:[],
    id:null,
    value:null,
    x:null,
    y:null,

  },


  mounted () {
    axios
    .get('https://faircorp-arnaud-patra.cleverapps.io/api/lights')
    .then(response => (Value.info = response.data))
    .catch(error => console.log(error))
  },



});
