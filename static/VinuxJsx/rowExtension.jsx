var Button = ReactBootstrap.Button;
var Modal = ReactBootstrap.Modal;
var FormControl = ReactBootstrap.FormControl;
////////////////////////////////////////////////////////////////////////////////
//------------------------------------------------------------------------------
///  Modal to comment the producer
class CommentProducer extends React.Component {
    //------------------------------------------------------------------------------
    // initialise the data  
    constructor( props ) {
        super( props );
        this.state = { comment: "", mark: "" };
    }

    //------------------------------------------------------------------------------
    // set the mark
    handleMarkChange( value ) {
        this.setState( { mark: value.currentTarget.value });
    }
    
    //------------------------------------------------------------------------------
    // set the comment
    handleCommentChange( value ) {
        this.setState( { comment: value.currentTarget.value });
    }

    //------------------------------------------------------------------------------
    // post the new bottle
    commentProducer() {
        if ( this.state.comment == "" ) {
        }
        else {
            $.ajax( {
                url: '/Vinux/commentProducer/',
                data: { 'producer_id': this.props.producer_id, 'comment': this.state.comment, 'mark': this.state.mark },
                type: 'POST',
                dataType: 'json',
                success: function( data ) {
                    // this is the output of the request being redirected to getCellar
                    this.closeModal();
                }.bind( this ),
                error: function( xhr, ajaxOptions, thrownError ) {
                    alert( "commentProducer; - " + xhr.status + "  - " + thrownError );
                }
            });
            this.closeModal();
        }
    }


    //------------------------------------------------------------------------------
    // close modal window
    closeModal() {
        this.props.closeModal();
        this.setState( { comment: "" });
    }

    render() {
        return (
            <Modal className="static-modal" show={this.props.showModal}  onHide={()=>this.closeModal()} bsSize="large">
                <Modal.Header closeButton>
                    <Modal.Title>Commenter le producteur</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <p>Commentaire:</p>
                    <FormControl componentClass="textarea" onChange={this.handleCommentChange.bind( this )}/>
                    <p></p>
                    <p>Note (de 1 à 20): <input type="number" min="0" max="20" step="1" onChange={this.handleMarkChange.bind( this )}></input></p>
                </Modal.Body>
                <Modal.Footer>
                    <Button onClick={() => this.closeModal()}>Annuler</Button>
                    <Button bsStyle="primary" onClick={() => this.commentProducer()}>Commenter</Button>
                </Modal.Footer>
            </Modal>
        );
    }
}

////////////////////////////////////////////////////////////////////////////////
//------------------------------------------------------------------------------
///  Modal to comment the bottle
class CommentBottle extends React.Component {
    //------------------------------------------------------------------------------
    // initialise the data  
    constructor( props ) {
        super( props );
        this.state = { comment: "", mark: "", flavor: "", pairing: "" };
    }

    //------------------------------------------------------------------------------
    // set the mark
    handleMarkChange( value ) {
        this.setState( { mark: value.currentTarget.value });
    }
    
    //------------------------------------------------------------------------------
    // set the flavor
    handleFlavorChange( value ) {
        this.setState( { flavor: value.currentTarget.value });
    }
    
    //------------------------------------------------------------------------------
    // set the pairing
    handlePairingChange( value ) {
        this.setState( { pairing: value.currentTarget.value });
    }
    
    //------------------------------------------------------------------------------
    // set the comment
    handleCommentChange( value ) {
        this.setState( { comment: value.currentTarget.value });
    }

    //------------------------------------------------------------------------------
    // post the new bottle
    commentBottle() {
        if ( this.state.comment == "" ) {
        }
        else {
            $.ajax( {
                url: '/Vinux/commentBottle/',
                data: { 'bottle_id': this.props.bottle_id, 'comment': this.state.comment, 'mark': this.state.mark, 'pairing':this.state.mark, 'flavor':this.state.flavor },
                type: 'POST',
                dataType: 'json',
                success: function( data ) {
                    // this is the output of the request being redirected to getCellar
                    this.closeModal();
                }.bind( this ),
                error: function( xhr, ajaxOptions, thrownError ) {
                    alert( "commentBottle; - " + xhr.status + "  - " + thrownError );
                }
            });
            this.closeModal();
        }
    }


    //------------------------------------------------------------------------------
    // close modal window
    closeModal() {
        this.props.closeModal();
        this.setState( { comment: "" });
    }

    render() {
        return (
            <Modal className="static-modal" show={this.props.showModal}  onHide={()=>this.closeModal()} bsSize="large">
                <Modal.Header closeButton>
                    <Modal.Title>Commenter la bouteille</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <p>Commentaire:</p>
                    <FormControl componentClass="textarea" onChange={this.handleCommentChange.bind( this )}/>
                    <p></p>
                    <p>Nez: <input type="text" onChange={this.handleFlavorChange.bind( this )}></input></p>
                    <p></p>
                    <p>Assortiment: <input type="text"  onChange={this.handleFlavorChange.bind( this )}></input></p>
                    <p></p>
                    <p>Note (de 1 à 20): <input type="number" min="0" max="20" step="1" onChange={this.handleMarkChange.bind( this )}></input></p>
                </Modal.Body>
                <Modal.Footer>
                    <Button onClick={() => this.closeModal()}>Annuler</Button>
                    <Button bsStyle="primary" onClick={() => this.commentBottle()}>Commenter</Button>
                </Modal.Footer>
            </Modal>
        );
    }
}


////////////////////////////////////////////////////////////////////////////////
//------------------------------------------------------------------------------
// information to show when the row is expended
class RowExtension extends React.Component {

    // initialise the data  
    constructor( props ) {
        super( props );
        this.state= { showCommentProducer: 0, showCommentBottle: 0, comments:{producerComments:null} };
    }
    
    //------------------------------------------------------------------------------
    //get the data
    componentDidMount() {
        this.getComments();
    }

    //------------------------------------------------------------------------------
    // call to get the data
    getComments() {
        $.ajax( {
            url: '/Vinux/getComments/',
            data: { 'producer_id': this.props.bottle.producer_id, 'bottle_id': this.props.bottle.underlying_id },
            dataType: 'json',
            success: function( commentRes ) {
                this.setState( { comments: commentRes });
            }.bind( this ),
            error: function( xhr, ajaxOptions, thrownError ) {
                alert( "getComments; " + xhr.status + " " + thrownError )
            }
        });
    }

    
    //------------------------------------------------------------------------------
    // delete selected producer comments
    deleteSelectedComments(commentKeys) {
        $.ajax({
            url: '/Vinux/deleteSelectedComments/',
            data: {'comment_ids':commentKeys},
            type:'POST',
            dataType: 'json',
            traditional:true,
            success: function(commentRes) {
                // get the remaining comments
                this.getComments();
            }.bind(this),
            error:function (xhr, ajaxOptions, thrownError) {
                alert("deleteSelectedComments; " + xhr.status + " " + thrownError );
              }
          });
    }
    
    //------------------------------------------------------------------------------
    // open modal window
    commentProducer() {
        this.setState( { showCommentProducer: 1 });
    }
    commentBottle() {
        this.setState( { showCommentBottle: 1 });
    }
    
    //------------------------------------------------------------------------------
    // add the same bottle
    addTheSameBottle()  {
        $.ajax({
            url: '/Vinux/addTheSameBottle/',
            data: {'bottle_id': this.props.bottle.id},
            type:'POST',
            dataType: 'json',
            traditional:true,
            success: function(commentRes) {
                // load the data (passed by the main table)
                this.props.onAddSame();
            }.bind(this),
            error:function (xhr, ajaxOptions, thrownError) {
                alert("deleteSelectedProducerComments; " + xhr.status + " " + thrownError );
              }
          });
    }

    //------------------------------------------------------------------------------
    // open modal window
    closeModal() {
        this.setState( { showCommentProducer: 0 });
        this.setState( { showCommentBottle: 0 });
        this.getComments();
    }
    
    //------------------------------------------------------------------------------
    // does nothing but defining this allow to search the table
    afterSearch( searchText, result ) {
    }
    
    //------------------------------------------------------------------------------
    // get unselectable comments
    getUnselectableComments( comments ) {
        var tmp = [];
        if ( comments != null ) {
            var j = 0;
            for ( var i = 0; i < comments.length; ++i ) {
                if ( !comments[i].is_from_user ) {
                    tmp[j] = comments[i].comment_id;
                    ++j;
                }
            }
        }
        return tmp;
    }
    
    //------------------------------------------------------------------------------
    render() {
        const selectRowPropProducers = {
                mode: 'checkbox',
                clickToSelect: false,
                unselectable: this.getUnselectableComments( this.state.comments.producerComments )
              };
        const selectRowPropBottles = {
                mode: 'checkbox',
                clickToSelect: false,
                unselectable: this.getUnselectableComments( this.state.comments.bottleComments )
              };

        if ( this.props.bottle.removalDate == "" ) {
            return (
                <div>
                    <p>Date d'ajout: {this.props.bottle.additionDate}</p>
                    <Button bsStyle="danger" onClick={() => this.addTheSameBottle()} >Ajouter la même</Button>
                    <Button bsStyle="success" onClick={() => this.commentProducer()}>Commenter le producteur</Button>
                    <CommentProducer producer_id={this.props.bottle.producer_id} showModal={this.state.showCommentProducer == 1} closeModal={this.closeModal.bind( this )}></CommentProducer>
                    <Button bsStyle="info" onClick={() => this.commentBottle()}>Commenter la bouteille</Button>
                    <CommentBottle bottle_id={this.props.bottle.underlying_id} showModal={this.state.showCommentBottle == 1} closeModal={this.closeModal.bind( this )}></CommentBottle>
                    <BootstrapTable
                        data={this.state.comments.producerComments}
                        pagination={true}
                        hover={true}
                        search={true}
                        deleteRow={true}
                        selectRow={ selectRowPropProducers } 
                        options={{ afterDeleteRow: this.deleteSelectedComments.bind( this ), afterSearch: this.afterSearch.bind( this ) }}>
                        <TableHeaderColumn dataField="comment_id" isKey hidden>comment_id</TableHeaderColumn>
                        <TableHeaderColumn dataField="author" width='120' dataSort={true} tdStyle={{ whiteSpace: 'normal' }}>Auteur</TableHeaderColumn>
                        <TableHeaderColumn dataField="mark" width='120' dataSort={true} tdStyle={{ whiteSpace: 'normal' }}>Note</TableHeaderColumn>
                        <TableHeaderColumn dataField="date" width='120' dataSort={true} tdStyle={{ whiteSpace: 'normal' }}>Date</TableHeaderColumn>
                        <TableHeaderColumn dataField="comment" dataSort={true} tdStyle={{ whiteSpace: 'normal' }}  >Commentaire sur le producteur</TableHeaderColumn>
                    </BootstrapTable>
                    <p></p>
                    <BootstrapTable
                        data={this.state.comments.bottleComments}
                        pagination={true}
                        hover={true}
                        search={true}
                        deleteRow={true}
                        selectRow={selectRowPropBottles}
                        options={{ afterDeleteRow: this.deleteSelectedComments.bind( this ), afterSearch: this.afterSearch.bind( this ) }}>
                        <TableHeaderColumn dataField="comment_id" isKey hidden>comment_id</TableHeaderColumn>
                        <TableHeaderColumn dataField="author" width='120' dataSort={true} tdStyle={{ whiteSpace: 'normal' }}>Auteur</TableHeaderColumn>
                        <TableHeaderColumn dataField="mark" width='120' dataSort={true} tdStyle={{ whiteSpace: 'normal' }}>Note</TableHeaderColumn>
                        <TableHeaderColumn dataField="date" width='120' dataSort={true} tdStyle={{ whiteSpace: 'normal' }}>Date</TableHeaderColumn>
                        <TableHeaderColumn dataField="pairing" width='120' dataSort={true} tdStyle={{ whiteSpace: 'normal' }}>Assortiment</TableHeaderColumn>
                        <TableHeaderColumn dataField="flavor" width='120' dataSort={true} tdStyle={{ whiteSpace: 'normal' }}>Nez</TableHeaderColumn>
                        <TableHeaderColumn dataField="comment" dataSort={true} tdStyle={{ whiteSpace: 'normal' }}  >Commentaire sur la bouteille</TableHeaderColumn>
                    </BootstrapTable>
                </div> );
        }
        else {
            return (
                <div>
                    <p>Date d'ajout: {this.props.bottle.additionDate}</p>
                    <p>Date de retrait: {this.props.bottle.removalDate}</p>
                </div> );
        }

    }
}

