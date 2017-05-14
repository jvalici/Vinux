////////////////////////////////////////////////////////////////////////////////
//------------------------------------------------------------------------------
 class GoneBottles extends React.Component {
  //------------------------------------------------------------------------------
  // initialise the data  
   constructor(props) {
     super(props);
     this.state = {modalLeve: 0};
  }
  
  //------------------------------------------------------------------------------
  //get the data
  componentDidMount() {
      this.loadData();
  }
  
  //------------------------------------------------------------------------------
  // call to get the data
  loadData() {
      $.ajax({
          url: '/Vinux/getGoneBottles/',
          dataType: 'json',
          success: function(data) {
              this.setState({goneBottles: data});
          }.bind(this),
          error:function (xhr, ajaxOptions, thrownError) {
              alert("loadData 2; " + xhr.status + " " + thrownError )
            }
        });
  }
  
  //------------------------------------------------------------------------------
  // remove a bottle
  deleteBottle(rowKeys)
  {
      $.ajax({
          url: '/Vinux/deleteBottle/',
          data: {'bottle_ids':rowKeys},
          type:'POST',
          dataType: 'json',
          traditional:true,
          success: function(data) {
              // this is the redirection to getGoneBottles
              this.setState({goneBottles: data});
              alert('Byebye bouteille!');
          }.bind(this),
          error:function (xhr, ajaxOptions, thrownError) {
              alert("deleteBottle; " + xhr.status + " " + thrownError )
            }
        });
  }

  //------------------------------------------------------------------------------
  // does nothing but defining this allow to search the table
  afterSearch(searchText, result) {
  }

  //------------------------------------------------------------------------------
  // all the rows can be extended
  isExpandableRow(row) {
       return true;
  }
 
  //------------------------------------------------------------------------------
  // get the row extension
  expandComponent(row) {
      return (  
              <RowExtension data={ row }/>
      );
  }

  //------------------------------------------------------------------------------
  // render the data  
  render() {

      // issue with the Ajax call to get the data
      if ( this.state.goneBottles == undefined ) {
          return ( <div><p>Dev error</p></div> );
      }
      
      else { // display the bottles
          return (
               <div>
                  <p>Coquin, voila ce que tu t'es déjà mis dans le gosier:</p>
                  <BootstrapTable 
                         exportCSV  
                         data={ this.state.goneBottles.bottles }
                         pagination={ true } 
                         hover={ true } 
                         selectRow={ {mode: 'checkbox', clickToSelect: false, clickToExpand: true} } 
                         search={ true } 
                         deleteRow={ true }
                         expandableRow={ this.isExpandableRow.bind(this) }
                         expandComponent={ this.expandComponent.bind(this) }
                         expandColumnOptions={ { expandColumnVisible: true } }
                         options={{afterDeleteRow:this.deleteBottle.bind(this), afterSearch: this.afterSearch.bind(this), expandRowBgColor: 'rgb(242, 255, 163)'}}>
                      <TableHeaderColumn dataField="id" isKey hidden>id</TableHeaderColumn>
                      <TableHeaderColumn dataField="denomination" dataSort={ true } tdStyle={ { whiteSpace: 'normal' } }>Dénomination</TableHeaderColumn>
                      <TableHeaderColumn dataField="producer" dataSort={ true } tdStyle={ { whiteSpace: 'normal' } }>Producteur</TableHeaderColumn>
                      <TableHeaderColumn dataField="name" width='150' dataSort={ true }>Name</TableHeaderColumn>
                      <TableHeaderColumn dataField="vintage" width='110' dataSort={ true }>Milésime</TableHeaderColumn>
                      <TableHeaderColumn dataField="productionArea" width='150' dataSort={ true }>Région</TableHeaderColumn>
                      <TableHeaderColumn  dataField="priceIn" width='80' dataSort={ true }>Prix</TableHeaderColumn>
                  </BootstrapTable>
              </div>
          );
      }

  } // end render()
}// end class GoneBottles

////////////////////////////////////////////////////////////////////////////////
//------------------------------------------------------------------------------
// main
ReactDOM.render(
  <GoneBottles/>,
  document.getElementById('goneBottles-div')
);


