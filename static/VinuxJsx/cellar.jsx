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
              <div className={this.props.backdropClassName} style={backdropStyle}
                   onClick={e => this.close(e)}/>}
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
      $.ajax({
          url: '/Vinux/getAreasFirstLevel/',
          type:'GET',
          dataType: 'json',
          success: function(data) {
              this.setState({areas_level_1: data.areas});
          }.bind(this),
          error:function (xhr, ajaxOptions, thrownError) {
              alert(xhr.status);
              alert(thrownError);
            }
        });
  }
  
  openModal1() {
      this.setState( { modalLevel: 1 });
  }
  
  openModal2(val) {
      $.ajax({
          url: '/Vinux/getAreasSecondLevel/',
          data: {'parent_area':val.label},
          type:'GET',
          dataType: 'json',
          success: function(data) {
              this.setState({areas_level_2: data.areas});
          }.bind(this),
          error:function (xhr, ajaxOptions, thrownError) {
              alert(xhr.status);
              alert(thrownError);
            }
        });
      this.setState( { area_level_1: val.label });
      this.setState( { modalLevel: 2 });
  }
  
  openModal3(val) {
      $.ajax({
          url: '/Vinux/getDenominations/',
          data: {'parent_area':this.state.area_level_1, 'area':val.label},
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
      this.setState( { modalLevel: 3 });
  }
  
  openModal4(val) {
      $.ajax({
          url: '/Vinux/getProducers/',
          data: {'denomination':val.label},
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
      this.setState( { denomination: val.label });
      this.setState( { modalLevel: 4 });
  }
  
  openModal5(val) {
      this.setState( { producer_id: val.id });
      this.setState( { modalLevel: 5 });
  }
  
  handlePriceChange(form)
  {
      this.setState( { price: form.currentTarget.value });;
  }
  handleVintageChange(form)
  {
      this.setState( { vintage: form.currentTarget.value });;
  }
  handleNameChange(form)
  {
      this.setState( { name: form.currentTarget.value });
  }
  
  finishAddingBottle()
  {
      $.ajax({
          url: '/Vinux/addBottle/',
          data: {'denomination':this.state.denomination, 'producer_id':this.state.producer_id, 'price':this.state.price, 'vintage':this.state.vintage, 'name':this.state.name},
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
  
  closeModal() {
      this.setState( { price: '' });
      this.setState( { modalLevel: 0 });
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
                  <button onClick={() => this.openModal1()}>Nvlle bouteille</button>
                  <Modal isOpen={this.state.modalLevel == 1} onClose={() => this.closeModal()}>
                      <p><button onClick={() => this.closeModal()}>Annuler</button></p>
                      <p>Choisir une région:</p>
                      <Select options={this.state.areas_level_1} onChange={this.openModal2.bind(this)}></Select>
                  </Modal>
                 <Modal isOpen={this.state.modalLevel == 2} onClose={() => this.closeModal()}>
                    <p><button onClick={() => this.closeModal()}>Annuler</button></p>
                    <p>Choisir une sous-région:</p>
                    <Select options={this.state.areas_level_2} onChange={this.openModal3.bind(this)}></Select>
                 </Modal>
                 <Modal isOpen={this.state.modalLevel == 3} onClose={() => this.closeModal()}>
                    <p><button onClick={() => this.closeModal()}>Annuler</button></p>
                    <p>Choisir une dénomination:</p>
                    <Select options={this.state.denominations} onChange={this.openModal4.bind(this)}></Select>
                 </Modal>
                 <Modal isOpen={this.state.modalLevel == 4} onClose={() => this.closeModal()}>
                     <p><button onClick={() => this.closeModal()}>Annuler</button></p>
                     <p>Choisir un producteur:</p>
                     <Select options={this.state.producers} onChange={this.openModal5.bind(this)}></Select>
                 </Modal>
                 <Modal isOpen={this.state.modalLevel == 5} onClose={() => this.closeModal()}>
                     <p><button onClick={() => this.closeModal()}>Annuler</button></p>
                     <form onSubmit={() => this.finishAddingBottle()}>
                         <p>Prix (Euros): <input type="number" step="0.01" id="price" onChange={this.handlePriceChange.bind(this)}></input></p>
                         <p>Milésime: <input type="number" step="1" id="vintage" onChange={this.handleVintageChange.bind(this)}></input></p>
                         <p>Nom: <input type="text" id="name" onChange={this.handleNameChange.bind(this)}  ></input></p>
                         <p><button onClick={() => this.finishAddingBottle()}>Ajouter</button></p>
                     </form>
                  </Modal>
                      
                      
                  <BootstrapTable exportCSV  
                      data={ this.state.cellarData.storedWineBottles } stripped>
                      <TableHeaderColumn dataField="denomination" isKey>Dénomination</TableHeaderColumn>
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
}// end var Cellar

////////////////////////////////////////////////////////////////////////////////
//------------------------------------------------------------------------------
// main
ReactDOM.render(
  // usernameFromDjangoTestOnly is not a proper way to go
  <Cellar  />,
  document.getElementById('cellar-div')
);
