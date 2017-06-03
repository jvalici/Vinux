'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var Button = ReactBootstrap.Button;
var Modal = ReactBootstrap.Modal;

////////////////////////////////////////////////////////////////////////////////
//------------------------------------------------------------------------------

var Cellar = function (_React$Component) {
    _inherits(Cellar, _React$Component);

    //------------------------------------------------------------------------------
    // initialise the data  
    function Cellar(props) {
        _classCallCheck(this, Cellar);

        var _this = _possibleConstructorReturn(this, (Cellar.__proto__ || Object.getPrototypeOf(Cellar)).call(this, props));

        _this.state = { modalLevel: 0 };
        return _this;
    }

    //------------------------------------------------------------------------------
    //get the data


    _createClass(Cellar, [{
        key: 'componentDidMount',
        value: function componentDidMount() {
            this.loadData();
        }

        //------------------------------------------------------------------------------
        // call to get the data

    }, {
        key: 'loadData',
        value: function loadData() {
            $.ajax({
                url: '/Vinux/getCellar/',
                dataType: 'json',
                success: function (data) {
                    this.setState({ cellarData: data });
                }.bind(this),
                error: function error(xhr, ajaxOptions, thrownError) {
                    alert("loadData 1; " + xhr.status + " " + thrownError);
                }
            });
        }

        //------------------------------------------------------------------------------
        // get the list of the producers based on multiple of 3 letters

    }, {
        key: 'getProducers',
        value: function getProducers(val) {
            if (val.length % 3 == 0 && val.length != 0) {
                $.ajax({
                    url: '/Vinux/getProducers/',
                    data: { 'hint': val },
                    type: 'GET',
                    dataType: 'json',
                    success: function (data) {
                        this.setState({ producers: data.prods });
                    }.bind(this),
                    error: function error(xhr, ajaxOptions, thrownError) {
                        alert("getProducers; " + xhr.status + " " + thrownError);
                    }
                });
            }
        }

        //------------------------------------------------------------------------------
        // get the list of the products based on multiple of 3 letters

    }, {
        key: 'getDenominations',
        value: function getDenominations(val) {
            if (val.length % 3 == 0 && val.length != 0) {
                $.ajax({
                    url: '/Vinux/getDenominations/',
                    data: { 'hint': val },
                    type: 'GET',
                    dataType: 'json',
                    success: function (data) {
                        this.setState({ denominations: data.denoms });
                    }.bind(this),
                    error: function error(xhr, ajaxOptions, thrownError) {
                        alert("getDenominations; " + xhr.status + " " + thrownError);
                    }
                });
            }
        }

        //------------------------------------------------------------------------------
        // set the denomination

    }, {
        key: 'handleDenominationChange',
        value: function handleDenominationChange(val) {
            this.setState({ denomination: val });
        }
        //------------------------------------------------------------------------------
        // set the producer

    }, {
        key: 'handleProducerChange',
        value: function handleProducerChange(val) {
            this.setState({ producer: val });
        }
        //------------------------------------------------------------------------------
        // set the price

    }, {
        key: 'handlePriceChange',
        value: function handlePriceChange(form) {
            this.setState({ price: form.currentTarget.value });
        }
        //------------------------------------------------------------------------------
        // set the vintage

    }, {
        key: 'handleVintageChange',
        value: function handleVintageChange(form) {
            this.setState({ vintage: form.currentTarget.value });
        }
        //------------------------------------------------------------------------------
        // set the name

    }, {
        key: 'handleNameChange',
        value: function handleNameChange(form) {
            this.setState({ name: form.currentTarget.value });
        }

        //------------------------------------------------------------------------------
        // open modal window

    }, {
        key: 'openModal',
        value: function openModal() {
            this.setState({ modalLevel: 1 });
        }
        //------------------------------------------------------------------------------
        // close modal window

    }, {
        key: 'closeModal',
        value: function closeModal() {
            this.setState({ price: '' });
            this.setState({ denomination: null });
            this.setState({ producer: null });
            this.setState({ modalLevel: 0 });
        }

        //------------------------------------------------------------------------------
        // post the new bottle

    }, {
        key: 'finishAddingBottle',
        value: function finishAddingBottle() {
            if (this.state.vintage < 1900 || this.state.vintage > 2050) {
                alert("Le milésime doit être entre 1900 et 2050");
            } else {
                $.ajax({
                    url: '/Vinux/addBottle/',
                    data: { 'denomination_id': this.state.denomination.id, 'producer_id': this.state.producer.id, 'price': this.state.price, 'vintage': this.state.vintage, 'name': this.state.name },
                    type: 'POST',
                    dataType: 'json',
                    success: function (data) {
                        // this is the output of the request being redirected to getCellar
                        this.setState({ cellarData: data });
                        this.closeModal();
                    }.bind(this),
                    error: function error(xhr, ajaxOptions, thrownError) {
                        alert("finishAddingBottle; - " + xhr.status + "  - " + thrownError);
                    }
                });
                this.closeModal();
            }
        }

        //------------------------------------------------------------------------------
        // remove a bottle

    }, {
        key: 'removeBottle',
        value: function removeBottle(rowKeys) {
            $.ajax({
                url: '/Vinux/removeBottle/',
                data: { 'bottle_ids': rowKeys },
                type: 'POST',
                dataType: 'json',
                traditional: true,
                success: function (data) {
                    // this is the redirection to getGoneBottles
                }.bind(this),
                error: function error(xhr, ajaxOptions, thrownError) {
                    alert("removeBottle; " + xhr.status + " " + thrownError);
                }
            });
        }

        //------------------------------------------------------------------------------
        // does nothing but defining this allow to search the table

    }, {
        key: 'afterSearch',
        value: function afterSearch(searchText, result) {}

        //------------------------------------------------------------------------------
        // all the rows can be extended

    }, {
        key: 'isExpandableRow',
        value: function isExpandableRow(row) {
            return true;
        }

        //------------------------------------------------------------------------------
        // get the row extension

    }, {
        key: 'expandComponent',
        value: function expandComponent(row) {
            return React.createElement(RowExtension, { bottle: row, onAddSame: this.loadData.bind(this) });
        }

        //------------------------------------------------------------------------------
        // render the data  

    }, {
        key: 'render',
        value: function render() {
            var _this2 = this;

            // issue with the Ajax call to get the data
            if (this.state.cellarData == undefined) {
                return React.createElement(
                    'div',
                    null,
                    React.createElement(
                        'p',
                        null,
                        'Dev error'
                    )
                );
            } else {
                // display the bottles
                return React.createElement(
                    'div',
                    null,
                    React.createElement(
                        'p',
                        null,
                        'Attention, il ne reste plus que \xE7a dans ta cave:'
                    ),
                    React.createElement(
                        Button,
                        { bsStyle: 'primary', onClick: function onClick() {
                                return _this2.openModal();
                            } },
                        'Nvlle bouteille'
                    ),
                    React.createElement(
                        Modal,
                        { className: 'static-modal', show: this.state.modalLevel == 1, onHide: function onHide() {
                                return _this2.closeModal();
                            }, bsSize: 'large' },
                        React.createElement(
                            Modal.Header,
                            { closeButton: true },
                            React.createElement(
                                Modal.Title,
                                null,
                                'Ajouter une bouteille'
                            )
                        ),
                        React.createElement(
                            Modal.Body,
                            null,
                            React.createElement(
                                'p',
                                null,
                                'Choisir un produit:'
                            ),
                            React.createElement(Select, { options: this.state.denominations, onInputChange: this.getDenominations.bind(this), onChange: this.handleDenominationChange.bind(this), value: this.state.denomination }),
                            React.createElement(
                                'p',
                                null,
                                'Choisir un producteur:'
                            ),
                            React.createElement(Select, { options: this.state.producers, onInputChange: this.getProducers.bind(this), onChange: this.handleProducerChange.bind(this), value: this.state.producer }),
                            React.createElement(
                                'p',
                                null,
                                'Prix (Euros): ',
                                React.createElement('input', { type: 'number', step: '0.01', id: 'price', onChange: this.handlePriceChange.bind(this) })
                            ),
                            React.createElement(
                                'p',
                                null,
                                'Mil\xE9sime: ',
                                React.createElement('input', { type: 'number', step: '1', id: 'vintage', onChange: this.handleVintageChange.bind(this) })
                            ),
                            React.createElement(
                                'p',
                                null,
                                'Nom: ',
                                React.createElement('input', { type: 'text', id: 'name', onChange: this.handleNameChange.bind(this) })
                            )
                        ),
                        React.createElement(
                            Modal.Footer,
                            null,
                            React.createElement(
                                Button,
                                { onClick: function onClick() {
                                        return _this2.closeModal();
                                    } },
                                'Annuler'
                            ),
                            React.createElement(
                                Button,
                                { bsStyle: 'primary', onClick: function onClick() {
                                        return _this2.finishAddingBottle();
                                    } },
                                'Ajouter'
                            )
                        )
                    ),
                    React.createElement(
                        BootstrapTable,
                        {
                            data: this.state.cellarData.bottles,
                            pagination: true,
                            hover: true,
                            selectRow: { mode: 'checkbox', clickToSelect: false, clickToExpand: true },
                            search: true,
                            deleteRow: true,
                            exportCSV: true,
                            expandableRow: this.isExpandableRow.bind(this),
                            expandComponent: this.expandComponent.bind(this),
                            expandColumnOptions: { expandColumnVisible: true },
                            options: {
                                afterDeleteRow: this.removeBottle.bind(this),
                                afterSearch: this.afterSearch.bind(this),
                                expandRowBgColor: 'rgb(242, 255, 163)',
                                deleteText: 'Supprimer les bouteilles selectionnées'
                            } },
                        React.createElement(
                            TableHeaderColumn,
                            { dataField: 'id', isKey: true, hidden: true },
                            'id'
                        ),
                        React.createElement(
                            TableHeaderColumn,
                            { dataField: 'denomination', dataSort: true, tdStyle: { whiteSpace: 'normal' } },
                            'D\xE9nomination'
                        ),
                        React.createElement(
                            TableHeaderColumn,
                            { dataField: 'producer', dataSort: true, tdStyle: { whiteSpace: 'normal' } },
                            'Producteur'
                        ),
                        React.createElement(
                            TableHeaderColumn,
                            { dataField: 'name', width: '150', dataSort: true },
                            'Name'
                        ),
                        React.createElement(
                            TableHeaderColumn,
                            { dataField: 'vintage', width: '110', dataSort: true },
                            'Mil\xE9sime'
                        ),
                        React.createElement(
                            TableHeaderColumn,
                            { dataField: 'productionArea', width: '150', dataSort: true },
                            'R\xE9gion'
                        ),
                        React.createElement(
                            TableHeaderColumn,
                            { dataField: 'priceIn', width: '80', dataSort: true },
                            'Prix'
                        )
                    )
                );
            }
        } // end render()

    }]);

    return Cellar;
}(React.Component); // end class Cellar

////////////////////////////////////////////////////////////////////////////////
//------------------------------------------------------------------------------
// main


ReactDOM.render(React.createElement(Cellar, null), document.getElementById('cellar-div'));