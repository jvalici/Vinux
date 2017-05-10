////////////////////////////////////////////////////////////////////////////////
//------------------------------------------------------------------------------
class Modal extends React.Component {
    render() {
      if (this.props.isOpen === false)
        return null

      let modalStyle = {
        position: 'absolute',
        top: '50%',
        left: '50%',
        width: '80%',
        height: '80%',
        transform: 'translate(-50%, -50%)',
        zIndex: '9999',
        background: '#fff'
      }

      if (this.props.width && this.props.height) {
        modalStyle.width = this.props.width + 'px'
        modalStyle.height = this.props.height + 'px'
        modalStyle.marginLeft = '-' + (this.props.width/1.5) + 'px',
        modalStyle.marginTop = '-' + (this.props.height/2) + 'px',
        modalStyle.transform = null
      }

      if (this.props.style) {
        for (let key in this.props.style) {
          modalStyle[key] = this.props.style[key]
        }
      }

      let backdropStyle = {
        position: 'absolute',
        width: '100%',
        height: '100%',
        top: '0px',
        left: '0px',
        zIndex: '9998',
        background: 'rgba(0, 0, 0, 0.3)'
      }

      if (this.props.backdropStyle) {
        for (let key in this.props.backdropStyle) {
          backdropStyle[key] = this.props.backdropStyle[key]
        }
      }

      return (
        <div className={this.props.containerClassName}>
          <div className={this.props.className} style={modalStyle}>
            {this.props.children}
          </div>
          {!this.props.noBackdrop &&
              <div className={this.props.backdropClassName} style={backdropStyle} onClick={e => this.close(e)}/>}
        </div>
      )
    }

    close(e) {
      e.preventDefault()

      if (this.props.onClose) {
        this.props.onClose()
      }
    }
  }

////////////////////////////////////////////////////////////////////////////////
//------------------------------------------------------------------------------
 class Cellar extends React.Component {
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
  }

  //------------------------------------------------------------------------------
  // get the list of the producers based on multiple of 3 letters
  getProducers(val)
  {
      if( val.length % 3 == 0){
          $.ajax({
              url: '/Vinux/getProducers/',
              data: {'hint':val},
              type:'GET',
              dataType: 'json',
              success: function(data) {
                  this.setState({producers: data.prods});
              }.bind(this),
              error:function (xhr, ajaxOptions, thrownError) {
                  alert(xhr.status);
                  alert(thrownError);
                }
            });
      }
  }
  
  //------------------------------------------------------------------------------
  // get the list of the products based on multiple of 3 letters
  getDenominations(val)
  {
      if( val.length % 3 == 0){
          $.ajax({
              url: '/Vinux/getDenominations/',
              data: {'hint':val},
              type:'GET',
              dataType: 'json',
              success: function(data) {
                  this.setState({denominations: data.denoms});
              }.bind(this),
              error:function (xhr, ajaxOptions, thrownError) {
                  alert(xhr.status);
                  alert(thrownError);
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
      this.setState( { modalLevel: 1 });
  }
  //------------------------------------------------------------------------------
  // close modal window
  closeModal() {
      this.setState( { price: '' });
      this.setState( { denomination: null });
      this.setState( { producer: null });
      this.setState( { modalLevel: 0 });
  }
  
  //------------------------------------------------------------------------------
  // post the new bottle
  finishAddingBottle()
  {
      $.ajax({
          url: '/Vinux/addBottle/',
          data: {'denomination_id':this.state.denomination.id, 'producer_id':this.state.producer.id, 'price':this.state.price, 'vintage':this.state.vintage, 'name':this.state.name},
          type:'POST',
          dataType: 'json',
          success: function(data) {
              alert('Bravo pour cette nouvelle bouteille!');
          }.bind(this),
          error:function (xhr, ajaxOptions, thrownError) {
              alert(xhr.status);
              alert(thrownError);
            }
        });
      closeModal();
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
              alert('Byebye bouteille!');
          }.bind(this),
          error:function (xhr, ajaxOptions, thrownError) {
              alert(xhr.status);
              alert(thrownError);
            }
        });
  }

  //------------------------------------------------------------------------------
  // does nothing but defining this allow to search the table
  afterSearch(searchText, result) {
  }


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
                  <button onClick={() => this.openModal()}>Nvlle bouteille</button>
                  <Modal isOpen={this.state.modalLevel == 1} onClose={() => this.closeModal()}>
                     <p><button onClick={() => this.closeModal()}>Annuler</button></p>
                     <form>
                         <p>Choisir un produit:</p>
                         <Select options={this.state.denominations} onInputChange={this.getDenominations.bind(this)} onChange={this.handleDenominationChange.bind(this)} value={this.state.denomination}></Select>
                         <p>Choisir un producteur:</p>
                         <Select options={this.state.producers} onInputChange={this.getProducers.bind(this)}  onChange={this.handleProducerChange.bind(this)} value={this.state.producer}></Select>
                         <p>Prix (Euros): <input type="number" step="0.01" id="price" onChange={this.handlePriceChange.bind(this)}></input></p>
                         <p>Milésime: <input type="number" step="1" id="vintage" onChange={this.handleVintageChange.bind(this)}></input></p>
                         <p>Nom: <input type="text" id="name" onChange={this.handleNameChange.bind(this)}  ></input></p>
                         <p><button onClick={() => this.finishAddingBottle()}>Ajouter</button></p>
                     </form>
                  </Modal>
                      
                      
                  <BootstrapTable 
                         exportCSV  
                         data={ this.state.cellarData.storedWineBottles }
                         stripped={ true } 
                         selectRow={ {mode: 'checkbox'} } 
                         search={ true } 
                         deleteRow={ true }
                         options={{afterDeleteRow:this.removeBottle.bind(this), afterSearch: this.afterSearch.bind(this)}}>
                      <TableHeaderColumn dataField="id" isKey hidden>id</TableHeaderColumn>
                      <TableHeaderColumn dataField="denomination">Dénomination</TableHeaderColumn>
                      <TableHeaderColumn dataField="vintage">Milésime</TableHeaderColumn>
                      <TableHeaderColumn dataField="productionArea">Région</TableHeaderColumn>
                      <TableHeaderColumn dataField="producer">Producteur</TableHeaderColumn>
                      <TableHeaderColumn dataField="name">Name</TableHeaderColumn>
                      <TableHeaderColumn  dataField="priceIn" >Prix</TableHeaderColumn>
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
