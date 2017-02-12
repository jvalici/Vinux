
var GreatingMessage = React.createClass({
  getInitialState: function() {
    return { message: 'Hello, ' };
  },
  render: function() {
    return (
      <div>
            <p>{ this.state.message } { this.props.userName }</p>
      </div>
    );
  }
});


ReactDOM.render(
  <GreatingMessage userName={ 'bbb' } />,
  document.getElementById('greeting-div')
);
