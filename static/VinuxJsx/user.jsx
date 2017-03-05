
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
  // usernameFromDjangoTestOnly is not a proper way to go
  <GreatingMessage userName={ usernameFromDjangoTestOnly } />,
  document.getElementById('greeting-div')
);
