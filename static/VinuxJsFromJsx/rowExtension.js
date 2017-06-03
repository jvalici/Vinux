"use strict";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var Button = ReactBootstrap.Button;
var Modal = ReactBootstrap.Modal;
var FormControl = ReactBootstrap.FormControl;
////////////////////////////////////////////////////////////////////////////////
//------------------------------------------------------------------------------
///  Modal to comment the producer

var CommentProducer = function (_React$Component) {
    _inherits(CommentProducer, _React$Component);

    //------------------------------------------------------------------------------
    // initialise the data  
    function CommentProducer(props) {
        _classCallCheck(this, CommentProducer);

        var _this = _possibleConstructorReturn(this, (CommentProducer.__proto__ || Object.getPrototypeOf(CommentProducer)).call(this, props));

        _this.state = { comment: "", mark: "" };
        return _this;
    }

    //------------------------------------------------------------------------------
    // set the mark


    _createClass(CommentProducer, [{
        key: "handleMarkChange",
        value: function handleMarkChange(value) {
            this.setState({ mark: value.currentTarget.value });
        }

        //------------------------------------------------------------------------------
        // set the comment

    }, {
        key: "handleCommentChange",
        value: function handleCommentChange(value) {
            this.setState({ comment: value.currentTarget.value });
        }

        //------------------------------------------------------------------------------
        // post the new bottle

    }, {
        key: "commentProducer",
        value: function commentProducer() {
            if (this.state.comment == "") {} else {
                $.ajax({
                    url: '/Vinux/commentProducer/',
                    data: { 'producer_id': this.props.producer_id, 'comment': this.state.comment, 'mark': this.state.mark },
                    type: 'POST',
                    dataType: 'json',
                    success: function (data) {
                        // this is the output of the request being redirected to getCellar
                        this.closeModal();
                    }.bind(this),
                    error: function error(xhr, ajaxOptions, thrownError) {
                        alert("commentProducer; - " + xhr.status + "  - " + thrownError);
                    }
                });
                this.closeModal();
            }
        }

        //------------------------------------------------------------------------------
        // close modal window

    }, {
        key: "closeModal",
        value: function closeModal() {
            this.props.closeModal();
            this.setState({ comment: "" });
        }
    }, {
        key: "render",
        value: function render() {
            var _this2 = this;

            return React.createElement(
                Modal,
                { className: "static-modal", show: this.props.showModal, onHide: function onHide() {
                        return _this2.closeModal();
                    }, bsSize: "large" },
                React.createElement(
                    Modal.Header,
                    { closeButton: true },
                    React.createElement(
                        Modal.Title,
                        null,
                        "Commenter le producteur"
                    )
                ),
                React.createElement(
                    Modal.Body,
                    null,
                    React.createElement(
                        "p",
                        null,
                        "Commentaire:"
                    ),
                    React.createElement(FormControl, { componentClass: "textarea", onChange: this.handleCommentChange.bind(this) }),
                    React.createElement("p", null),
                    React.createElement(
                        "p",
                        null,
                        "Note (de 1 \xE0 20): ",
                        React.createElement("input", { type: "number", min: "0", max: "20", step: "1", onChange: this.handleMarkChange.bind(this) })
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
                        "Annuler"
                    ),
                    React.createElement(
                        Button,
                        { bsStyle: "primary", onClick: function onClick() {
                                return _this2.commentProducer();
                            } },
                        "Commenter"
                    )
                )
            );
        }
    }]);

    return CommentProducer;
}(React.Component);

////////////////////////////////////////////////////////////////////////////////
//------------------------------------------------------------------------------
///  Modal to comment the bottle


var CommentBottle = function (_React$Component2) {
    _inherits(CommentBottle, _React$Component2);

    //------------------------------------------------------------------------------
    // initialise the data  
    function CommentBottle(props) {
        _classCallCheck(this, CommentBottle);

        var _this3 = _possibleConstructorReturn(this, (CommentBottle.__proto__ || Object.getPrototypeOf(CommentBottle)).call(this, props));

        _this3.state = { comment: "", mark: "", flavor: "", pairing: "" };
        return _this3;
    }

    //------------------------------------------------------------------------------
    // set the mark


    _createClass(CommentBottle, [{
        key: "handleMarkChange",
        value: function handleMarkChange(value) {
            this.setState({ mark: value.currentTarget.value });
        }

        //------------------------------------------------------------------------------
        // set the flavor

    }, {
        key: "handleFlavorChange",
        value: function handleFlavorChange(value) {
            this.setState({ flavor: value.currentTarget.value });
        }

        //------------------------------------------------------------------------------
        // set the pairing

    }, {
        key: "handlePairingChange",
        value: function handlePairingChange(value) {
            this.setState({ pairing: value.currentTarget.value });
        }

        //------------------------------------------------------------------------------
        // set the comment

    }, {
        key: "handleCommentChange",
        value: function handleCommentChange(value) {
            this.setState({ comment: value.currentTarget.value });
        }

        //------------------------------------------------------------------------------
        // post the new bottle

    }, {
        key: "commentBottle",
        value: function commentBottle() {
            if (this.state.comment == "") {} else {
                $.ajax({
                    url: '/Vinux/commentBottle/',
                    data: { 'bottle_id': this.props.bottle_id, 'comment': this.state.comment, 'mark': this.state.mark, 'pairing': this.state.mark, 'flavor': this.state.flavor },
                    type: 'POST',
                    dataType: 'json',
                    success: function (data) {
                        // this is the output of the request being redirected to getCellar
                        this.closeModal();
                    }.bind(this),
                    error: function error(xhr, ajaxOptions, thrownError) {
                        alert("commentBottle; - " + xhr.status + "  - " + thrownError);
                    }
                });
                this.closeModal();
            }
        }

        //------------------------------------------------------------------------------
        // close modal window

    }, {
        key: "closeModal",
        value: function closeModal() {
            this.props.closeModal();
            this.setState({ comment: "" });
        }
    }, {
        key: "render",
        value: function render() {
            var _this4 = this;

            return React.createElement(
                Modal,
                { className: "static-modal", show: this.props.showModal, onHide: function onHide() {
                        return _this4.closeModal();
                    }, bsSize: "large" },
                React.createElement(
                    Modal.Header,
                    { closeButton: true },
                    React.createElement(
                        Modal.Title,
                        null,
                        "Commenter la bouteille"
                    )
                ),
                React.createElement(
                    Modal.Body,
                    null,
                    React.createElement(
                        "p",
                        null,
                        "Commentaire:"
                    ),
                    React.createElement(FormControl, { componentClass: "textarea", onChange: this.handleCommentChange.bind(this) }),
                    React.createElement("p", null),
                    React.createElement(
                        "p",
                        null,
                        "Nez: ",
                        React.createElement("input", { type: "text", onChange: this.handleFlavorChange.bind(this) })
                    ),
                    React.createElement("p", null),
                    React.createElement(
                        "p",
                        null,
                        "Assortiment: ",
                        React.createElement("input", { type: "text", onChange: this.handleFlavorChange.bind(this) })
                    ),
                    React.createElement("p", null),
                    React.createElement(
                        "p",
                        null,
                        "Note (de 1 \xE0 20): ",
                        React.createElement("input", { type: "number", min: "0", max: "20", step: "1", onChange: this.handleMarkChange.bind(this) })
                    )
                ),
                React.createElement(
                    Modal.Footer,
                    null,
                    React.createElement(
                        Button,
                        { onClick: function onClick() {
                                return _this4.closeModal();
                            } },
                        "Annuler"
                    ),
                    React.createElement(
                        Button,
                        { bsStyle: "primary", onClick: function onClick() {
                                return _this4.commentBottle();
                            } },
                        "Commenter"
                    )
                )
            );
        }
    }]);

    return CommentBottle;
}(React.Component);

////////////////////////////////////////////////////////////////////////////////
//------------------------------------------------------------------------------
// information to show when the row is expended


var RowExtension = function (_React$Component3) {
    _inherits(RowExtension, _React$Component3);

    // initialise the data  
    function RowExtension(props) {
        _classCallCheck(this, RowExtension);

        var _this5 = _possibleConstructorReturn(this, (RowExtension.__proto__ || Object.getPrototypeOf(RowExtension)).call(this, props));

        _this5.state = { showCommentProducer: 0, showCommentBottle: 0, comments: { producerComments: null } };
        return _this5;
    }

    //------------------------------------------------------------------------------
    //get the data


    _createClass(RowExtension, [{
        key: "componentDidMount",
        value: function componentDidMount() {
            this.getComments();
        }

        //------------------------------------------------------------------------------
        // call to get the data

    }, {
        key: "getComments",
        value: function getComments() {
            $.ajax({
                url: '/Vinux/getComments/',
                data: { 'producer_id': this.props.bottle.producer_id, 'bottle_id': this.props.bottle.underlying_id },
                dataType: 'json',
                success: function (commentRes) {
                    this.setState({ comments: commentRes });
                }.bind(this),
                error: function error(xhr, ajaxOptions, thrownError) {
                    alert("getComments; " + xhr.status + " " + thrownError);
                }
            });
        }

        //------------------------------------------------------------------------------
        // delete selected producer comments

    }, {
        key: "deleteSelectedComments",
        value: function deleteSelectedComments(commentKeys) {
            $.ajax({
                url: '/Vinux/deleteSelectedComments/',
                data: { 'comment_ids': commentKeys },
                type: 'POST',
                dataType: 'json',
                traditional: true,
                success: function (commentRes) {
                    // get the remaining comments
                    this.getComments();
                }.bind(this),
                error: function error(xhr, ajaxOptions, thrownError) {
                    alert("deleteSelectedComments; " + xhr.status + " " + thrownError);
                }
            });
        }

        //------------------------------------------------------------------------------
        // open modal window

    }, {
        key: "commentProducer",
        value: function commentProducer() {
            this.setState({ showCommentProducer: 1 });
        }
    }, {
        key: "commentBottle",
        value: function commentBottle() {
            this.setState({ showCommentBottle: 1 });
        }

        //------------------------------------------------------------------------------
        // add the same bottle

    }, {
        key: "addTheSameBottle",
        value: function addTheSameBottle() {
            $.ajax({
                url: '/Vinux/addTheSameBottle/',
                data: { 'bottle_id': this.props.bottle.id },
                type: 'POST',
                dataType: 'json',
                traditional: true,
                success: function (commentRes) {
                    // load the data (passed by the main table)
                    this.props.onAddSame();
                }.bind(this),
                error: function error(xhr, ajaxOptions, thrownError) {
                    alert("deleteSelectedProducerComments; " + xhr.status + " " + thrownError);
                }
            });
        }

        //------------------------------------------------------------------------------
        // open modal window

    }, {
        key: "closeModal",
        value: function closeModal() {
            this.setState({ showCommentProducer: 0 });
            this.setState({ showCommentBottle: 0 });
            this.getComments();
        }

        //------------------------------------------------------------------------------
        // does nothing but defining this allow to search the table

    }, {
        key: "afterSearch",
        value: function afterSearch(searchText, result) {}

        //------------------------------------------------------------------------------
        // get unselectable comments

    }, {
        key: "getUnselectableComments",
        value: function getUnselectableComments(comments) {
            var tmp = [];
            if (comments != null) {
                var j = 0;
                for (var i = 0; i < comments.length; ++i) {
                    if (!comments[i].is_from_user) {
                        tmp[j] = comments[i].comment_id;
                        ++j;
                    }
                }
            }
            return tmp;
        }

        //------------------------------------------------------------------------------

    }, {
        key: "render",
        value: function render() {
            var _this6 = this;

            var selectRowPropProducers = {
                mode: 'checkbox',
                clickToSelect: false,
                unselectable: this.getUnselectableComments(this.state.comments.producerComments)
            };
            var selectRowPropBottles = {
                mode: 'checkbox',
                clickToSelect: false,
                unselectable: this.getUnselectableComments(this.state.comments.bottleComments)
            };

            if (this.props.bottle.removalDate == "") {
                return React.createElement(
                    "div",
                    null,
                    React.createElement(
                        "p",
                        null,
                        "Date d'ajout: ",
                        this.props.bottle.additionDate
                    ),
                    React.createElement(
                        Button,
                        { bsStyle: "danger", onClick: function onClick() {
                                return _this6.addTheSameBottle();
                            } },
                        "Ajouter la m\xEAme"
                    ),
                    React.createElement(
                        Button,
                        { bsStyle: "success", onClick: function onClick() {
                                return _this6.commentProducer();
                            } },
                        "Commenter le producteur"
                    ),
                    React.createElement(CommentProducer, { producer_id: this.props.bottle.producer_id, showModal: this.state.showCommentProducer == 1, closeModal: this.closeModal.bind(this) }),
                    React.createElement(
                        Button,
                        { bsStyle: "info", onClick: function onClick() {
                                return _this6.commentBottle();
                            } },
                        "Commenter la bouteille"
                    ),
                    React.createElement(CommentBottle, { bottle_id: this.props.bottle.underlying_id, showModal: this.state.showCommentBottle == 1, closeModal: this.closeModal.bind(this) }),
                    React.createElement(
                        BootstrapTable,
                        {
                            data: this.state.comments.producerComments,
                            pagination: true,
                            hover: true,
                            search: true,
                            deleteRow: true,
                            selectRow: selectRowPropProducers,
                            options: { afterDeleteRow: this.deleteSelectedComments.bind(this), afterSearch: this.afterSearch.bind(this) } },
                        React.createElement(
                            TableHeaderColumn,
                            { dataField: "comment_id", isKey: true, hidden: true },
                            "comment_id"
                        ),
                        React.createElement(
                            TableHeaderColumn,
                            { dataField: "author", width: "120", dataSort: true, tdStyle: { whiteSpace: 'normal' } },
                            "Auteur"
                        ),
                        React.createElement(
                            TableHeaderColumn,
                            { dataField: "mark", width: "120", dataSort: true, tdStyle: { whiteSpace: 'normal' } },
                            "Note"
                        ),
                        React.createElement(
                            TableHeaderColumn,
                            { dataField: "date", width: "120", dataSort: true, tdStyle: { whiteSpace: 'normal' } },
                            "Date"
                        ),
                        React.createElement(
                            TableHeaderColumn,
                            { dataField: "comment", dataSort: true, tdStyle: { whiteSpace: 'normal' } },
                            "Commentaire sur le producteur"
                        )
                    ),
                    React.createElement("p", null),
                    React.createElement(
                        BootstrapTable,
                        {
                            data: this.state.comments.bottleComments,
                            pagination: true,
                            hover: true,
                            search: true,
                            deleteRow: true,
                            selectRow: selectRowPropBottles,
                            options: { afterDeleteRow: this.deleteSelectedComments.bind(this), afterSearch: this.afterSearch.bind(this) } },
                        React.createElement(
                            TableHeaderColumn,
                            { dataField: "comment_id", isKey: true, hidden: true },
                            "comment_id"
                        ),
                        React.createElement(
                            TableHeaderColumn,
                            { dataField: "author", width: "120", dataSort: true, tdStyle: { whiteSpace: 'normal' } },
                            "Auteur"
                        ),
                        React.createElement(
                            TableHeaderColumn,
                            { dataField: "mark", width: "120", dataSort: true, tdStyle: { whiteSpace: 'normal' } },
                            "Note"
                        ),
                        React.createElement(
                            TableHeaderColumn,
                            { dataField: "date", width: "120", dataSort: true, tdStyle: { whiteSpace: 'normal' } },
                            "Date"
                        ),
                        React.createElement(
                            TableHeaderColumn,
                            { dataField: "pairing", width: "120", dataSort: true, tdStyle: { whiteSpace: 'normal' } },
                            "Assortiment"
                        ),
                        React.createElement(
                            TableHeaderColumn,
                            { dataField: "flavor", width: "120", dataSort: true, tdStyle: { whiteSpace: 'normal' } },
                            "Nez"
                        ),
                        React.createElement(
                            TableHeaderColumn,
                            { dataField: "comment", dataSort: true, tdStyle: { whiteSpace: 'normal' } },
                            "Commentaire sur le producteur"
                        )
                    )
                );
            } else {
                return React.createElement(
                    "div",
                    null,
                    React.createElement(
                        "p",
                        null,
                        "Date d'ajout: ",
                        this.props.bottle.additionDate
                    ),
                    React.createElement(
                        "p",
                        null,
                        "Date de retrait: ",
                        this.props.bottle.removalDate
                    )
                );
            }
        }
    }]);

    return RowExtension;
}(React.Component);