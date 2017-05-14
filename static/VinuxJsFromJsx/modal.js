'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

////////////////////////////////////////////////////////////////////////////////
//------------------------------------------------------------------------------
var Modal = function (_React$Component) {
    _inherits(Modal, _React$Component);

    function Modal() {
        _classCallCheck(this, Modal);

        return _possibleConstructorReturn(this, (Modal.__proto__ || Object.getPrototypeOf(Modal)).apply(this, arguments));
    }

    _createClass(Modal, [{
        key: 'render',
        value: function render() {
            var _this2 = this;

            if (this.props.isOpen === false) return null;

            var modalStyle = {
                position: 'absolute',
                top: '50%',
                left: '50%',
                width: '80%',
                height: '80%',
                transform: 'translate(-50%, -50%)',
                zIndex: '9999',
                background: '#fff'
            };

            if (this.props.width && this.props.height) {
                modalStyle.width = this.props.width + 'px';
                modalStyle.height = this.props.height + 'px';
                modalStyle.marginLeft = '-' + this.props.width / 1.5 + 'px', modalStyle.marginTop = '-' + this.props.height / 2 + 'px', modalStyle.transform = null;
            }

            if (this.props.style) {
                for (var key in this.props.style) {
                    modalStyle[key] = this.props.style[key];
                }
            }

            var backdropStyle = {
                position: 'absolute',
                width: '100%',
                height: '100%',
                top: '0px',
                left: '0px',
                zIndex: '9998',
                background: 'rgba(0, 0, 0, 0.3)'
            };

            if (this.props.backdropStyle) {
                for (var _key in this.props.backdropStyle) {
                    backdropStyle[_key] = this.props.backdropStyle[_key];
                }
            }

            return React.createElement(
                'div',
                { className: this.props.containerClassName },
                React.createElement(
                    'div',
                    { className: this.props.className, style: modalStyle },
                    this.props.children
                ),
                !this.props.noBackdrop && React.createElement('div', { className: this.props.backdropClassName, style: backdropStyle, onClick: function onClick(e) {
                        return _this2.close(e);
                    } })
            );
        }
    }, {
        key: 'close',
        value: function close(e) {
            e.preventDefault();

            if (this.props.onClose) {
                this.props.onClose();
            }
        }
    }]);

    return Modal;
}(React.Component);