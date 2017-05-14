'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

////////////////////////////////////////////////////////////////////////////////
//------------------------------------------------------------------------------
var GoneBottles = function (_React$Component) {
    _inherits(GoneBottles, _React$Component);

    //------------------------------------------------------------------------------
    // initialise the data  
    function GoneBottles(props) {
        _classCallCheck(this, GoneBottles);

        var _this = _possibleConstructorReturn(this, (GoneBottles.__proto__ || Object.getPrototypeOf(GoneBottles)).call(this, props));

        _this.state = { modalLeve: 0 };
        return _this;
    }

    //------------------------------------------------------------------------------
    //get the data


    _createClass(GoneBottles, [{
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
                url: '/Vinux/getGoneBottles/',
                dataType: 'json',
                success: function (data) {
                    this.setState({ goneBottles: data });
                }.bind(this),
                error: function error(xhr, ajaxOptions, thrownError) {
                    alert("loadData 2; " + xhr.status + " " + thrownError);
                }
            });
        }

        //------------------------------------------------------------------------------
        // remove a bottle

    }, {
        key: 'deleteBottle',
        value: function deleteBottle(rowKeys) {
            $.ajax({
                url: '/Vinux/deleteBottle/',
                data: { 'bottle_ids': rowKeys },
                type: 'POST',
                dataType: 'json',
                traditional: true,
                success: function (data) {
                    // this is the redirection to getGoneBottles
                    this.setState({ goneBottles: data });
                    alert('Byebye bouteille!');
                }.bind(this),
                error: function error(xhr, ajaxOptions, thrownError) {
                    alert("deleteBottle; " + xhr.status + " " + thrownError);
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
            return React.createElement(RowExtension, { data: row });
        }

        //------------------------------------------------------------------------------
        // render the data  

    }, {
        key: 'render',
        value: function render() {

            // issue with the Ajax call to get the data
            if (this.state.goneBottles == undefined) {
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
                        'Coquin, voila ce que tu t\'es d\xE9j\xE0 mis dans le gosier:'
                    ),
                    React.createElement(
                        BootstrapTable,
                        {
                            exportCSV: true,
                            data: this.state.goneBottles.bottles,
                            pagination: true,
                            hover: true,
                            selectRow: { mode: 'checkbox', clickToSelect: false, clickToExpand: true },
                            search: true,
                            deleteRow: true,
                            expandableRow: this.isExpandableRow.bind(this),
                            expandComponent: this.expandComponent.bind(this),
                            expandColumnOptions: { expandColumnVisible: true },
                            options: { afterDeleteRow: this.deleteBottle.bind(this), afterSearch: this.afterSearch.bind(this), expandRowBgColor: 'rgb(242, 255, 163)' } },
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

    return GoneBottles;
}(React.Component); // end class GoneBottles

////////////////////////////////////////////////////////////////////////////////
//------------------------------------------------------------------------------
// main


ReactDOM.render(React.createElement(GoneBottles, null), document.getElementById('goneBottles-div'));