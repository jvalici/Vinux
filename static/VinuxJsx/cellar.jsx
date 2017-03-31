////////////////////////////////////////////////////////////////////////////////
//------------------------------------------------------------------------------
var Cellar = React.createClass({
  
  //------------------------------------------------------------------------------
  // initialise the data  
  getInitialState() {
    //return {cellarData:[]};
    return {};
  },
  
  //------------------------------------------------------------------------------
  //get the data
  componentDidMount() {
      this.loadData()
  },
  
  //------------------------------------------------------------------------------
  // call to get the data
  loadData() {
      $.ajax({
            url: '/Vinux/getCellar/',
            dataType: 'json',
            success: function(data) {
                this.setState({cellarData: data});
            }.bind(this),
            error:function (xhr, ajaxOptions, thrownError) {
                alert(xhr.status);
                alert(thrownError);
              }
          });
  },

//  function priceFormatter(cell, row) {
//      return "<i class='glyphicon glyphicon-eur'></i> ${cell}";
//    }
  
  //------------------------------------------------------------------------------
  // render the data  
  render() {

      // issue with the Ajax call to get the data
      if ( this.state.cellarData == undefined ) {
          return ( <div><p>Dev error</p></div> );
      }
      
      // no bottle  
      if ( this.state.cellarData.length == 0 ) {
          return (
              <div>
                  <p>Votre cave est deseperement vide</p>
              </div>
          );
      }
      else { // display the bottles
          return (
              <div>
                  <p>Il ne reste plus que ça dans votre cave:</p>

                  <BootstrapTable exportCSV  
                      data={this.state.cellarData.storedWineBottles}
                      bordered={ true }
                      stripped={ true }
                      insertRow>
                      <TableHeaderColumn  width='150' dataField="appelation">Appelation</TableHeaderColumn>
                      <TableHeaderColumn  width='50' dataField="color">Couleur</TableHeaderColumn>
                      <TableHeaderColumn  width='150' dataField="productionArea">Région</TableHeaderColumn>
                      <TableHeaderColumn  width='150' dataField="producer">Producteur</TableHeaderColumn>
                      <TableHeaderColumn  width='200' dataField="name" isKey={true}>Name</TableHeaderColumn>
                      <TableHeaderColumn  width='50' dataField="priceIn" >Prix</TableHeaderColumn>
                  </BootstrapTable>
              </div>
          );
      }

  } // end render()
});// end var Cellar

////////////////////////////////////////////////////////////////////////////////
//------------------------------------------------------------------------------
// main
ReactDOM.render(
  // usernameFromDjangoTestOnly is not a proper way to go
  <Cellar  />,
  document.getElementById('cellar-div')
);
