var Button = ReactBootstrap.Button;
var Modal = ReactBootstrap.Modal;

////////////////////////////////////////////////////////////////////////////////
//------------------------------------------------------------------------------
 class Cellar extends React.Component {
  //------------------------------------------------------------------------------
  // initialise the data  
   constructor(props) {
     super(props);
     this.state = {modalLevel: 0, name:''};
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
          url: '/Vinux/getCellar/',
          dataType: 'json',
          success: function(data) {
              this.setState({cellarData: data});
          }.bind(this),
          error:function (xhr, ajaxOptions, thrownError) {
              alert("loadData 1; " + xhr.status + " " + thrownError )
          }
      });
  }

  //------------------------------------------------------------------------------
  // get the list of the producers based on multiple of 3 letters
  getProducers(val)
  {
      if( val.length % 3 == 0 && val.length!=0 ){
          $.ajax({
              url: '/Vinux/getProducers/',
              data: {'hint':val},
              type:'GET',
              dataType: 'json',
              success: function(data) {
                  this.setState({producers: data.prods});
              }.bind(this),
              error:function (xhr, ajaxOptions, thrownError) {
                  alert("getProducers; " + xhr.status + " " + thrownError )
                }
            });
      }
  }
  
  //------------------------------------------------------------------------------
  // get the list of the products based on multiple of 3 letters
  getDenominations(val)
  {
      if( val.length % 3 == 0 && val.length!=0 ){
          $.ajax({
              url: '/Vinux/getDenominations/',
              data: {'hint':val},
              type:'GET',
              dataType: 'json',
              success: function(data) {
                  this.setState({denominations: data.denoms});
              }.bind(this),
              error:function (xhr, ajaxOptions, thrownError) {
                  alert("getDenominations; " + xhr.status + " " + thrownError )
                }
            });
      }
  }
  
  //------------------------------------------------------------------------------
  // set the denomination
  handleDenominationChange(val)
  {
      this.setState( { denomination: val });
  }
  //------------------------------------------------------------------------------
  // set the producer
  handleProducerChange(val)
  {
      this.setState( { producer: val });
  }
  //------------------------------------------------------------------------------
  // set the price
  handlePriceChange(form)
  {
      this.setState( { price: form.currentTarget.value });
  }
  //------------------------------------------------------------------------------
  // set the vintage
  handleVintageChange(form)
  {
      this.setState( { vintage: form.currentTarget.value });
  }
  //------------------------------------------------------------------------------
  // set the name
  handleNameChange(form)
  {
      this.setState( { name: form.currentTarget.value });
  }
  
  //------------------------------------------------------------------------------
  // open modal window
  openModal() {
      this.setState({ modalLevel: 1 });
  }
  //------------------------------------------------------------------------------
  // close modal window
  closeModal() {
      this.setState( { price: '' });
      this.setState( { name: '' });
      this.setState( { denomination: null });
      this.setState( { producer: null });
      this.setState( { modalLevel: 0 });
  }
  
  //------------------------------------------------------------------------------
  // post the new bottle
  finishAddingBottle()
  {
      if( this.state.vintage < 1900 || this.state.vintage > 2050 ) {
          alert("Le milésime doit être entre 1900 et 2050");
      }
      else {
          $.ajax({
              url: '/Vinux/addBottle/',
              data: {'denomination_id':this.state.denomination.id, 'producer_id':this.state.producer.id, 'price':this.state.price, 'vintage':this.state.vintage, 'name':this.state.name},
              type:'POST',
              dataType: 'json',
              success: function(data) {
                  // this is the output of the request being redirected to getCellar
                  this.setState({cellarData: data});
                  this.closeModal();
              }.bind(this),
              error:function (xhr, ajaxOptions, thrownError) {
                  alert("finishAddingBottle; - " + xhr.status + "  - " + thrownError );
                }
            });
          this.closeModal();
      }
  }

  //------------------------------------------------------------------------------
  // remove a bottle
  removeBottle(rowKeys)
  {
      $.ajax({
          url: '/Vinux/removeBottle/',
          data: {'bottle_ids':rowKeys},
          type:'POST',
          dataType: 'json',
          traditional:true,
          success: function(data) {
              // this is the redirection to getGoneBottles
          }.bind(this),
          error:function (xhr, ajaxOptions, thrownError) {
              alert("removeBottle; " + xhr.status + " " + thrownError );
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
              <RowExtension bottle={row} onAddSame={this.loadData.bind(this)}></RowExtension>
      );
  }

  //------------------------------------------------------------------------------
  // render the data  
  render() {

      // issue with the Ajax call to get the data
      if ( this.state.cellarData == undefined ) {
          return ( <div><p>Dev error</p></div> );
      }
      
      else { // display the bottles
          return (
               <div>
                  <p>Attention, il ne reste plus que ça dans ta cave:</p>
                  <Button bsStyle="primary" onClick={() => this.openModal()}>Nvlle bouteille</Button>
                  <Modal className="static-modal" show={this.state.modalLevel == 1} onHide={() => this.closeModal()} bsSize="large">
                      <Modal.Header closeButton>
                          <Modal.Title>Ajouter une bouteille</Modal.Title>
                      </Modal.Header>
                     <Modal.Body>
                         <p>Choisir un produit:</p>
                         <Select options={this.state.denominations} onInputChange={this.getDenominations.bind(this)} onChange={this.handleDenominationChange.bind(this)} value={this.state.denomination}></Select>
                         <p>Choisir un producteur:</p>
                         <Select options={this.state.producers} onInputChange={this.getProducers.bind(this)}  onChange={this.handleProducerChange.bind(this)} value={this.state.producer}></Select>
                         <p>Prix (Euros): <input type="number" step="0.01" id="price" onChange={this.handlePriceChange.bind(this)}></input></p>
                         <p>Milésime: <input type="number" step="1" id="vintage" onChange={this.handleVintageChange.bind(this)}></input></p>
                         <p>Nom: <input type="text" id="name" onChange={this.handleNameChange.bind(this)}  ></input></p>
                     </Modal.Body>
                     <Modal.Footer>
                             <Button onClick={() => this.closeModal()}>Annuler</Button>
                             <Button bsStyle="primary" onClick={() => this.finishAddingBottle()}>Ajouter</Button>
                     </Modal.Footer>
                  </Modal>   
                  <BootstrapTable 
                         data={ this.state.cellarData.bottles }
                         pagination={ true } 
                         hover={ true } 
                         selectRow={ {mode: 'checkbox', clickToSelect: false, clickToExpand: true} } 
                         search={ true }
                         deleteRow={ true }
                         exportCSV={ true }
                         expandableRow={ this.isExpandableRow.bind(this) }
                         expandComponent={ this.expandComponent.bind(this) }
                         expandColumnOptions={ { expandColumnVisible: true } }
                         options={{
                             afterDeleteRow:this.removeBottle.bind(this),
                             afterSearch: this.afterSearch.bind(this),
                             expandRowBgColor: 'rgb(242, 255, 163)',
                             deleteText: 'Supprimer les bouteilles selectionnées',
                             }}>
                      <TableHeaderColumn dataField="id" isKey hidden>id</TableHeaderColumn>
                      <TableHeaderColumn dataField="denomination" dataSort={ true } tdStyle={ { whiteSpace: 'normal' } }>Dénomination</TableHeaderColumn>
                      <TableHeaderColumn dataField="producer" dataSort={ true } tdStyle={ { whiteSpace: 'normal' } }>Producteur</TableHeaderColumn>
                      <TableHeaderColumn dataField="name" width='150' dataSort={ true }>Name</TableHeaderColumn>
                      <TableHeaderColumn dataField="vintage" width='110' dataSort={ true }>Milésime</TableHeaderColumn>
                      <TableHeaderColumn dataField="productionArea" width='150' dataSort={ true }>Région</TableHeaderColumn>
                      <TableHeaderColumn dataField="priceIn" width='80' dataSort={ true }>Prix</TableHeaderColumn>
                  </BootstrapTable>
              </div>
          );
      }

  } // end render()
}// end class Cellar

////////////////////////////////////////////////////////////////////////////////
//------------------------------------------------------------------------------
// main
ReactDOM.render(
  <Cellar  />,
  document.getElementById('cellar-div')
);
