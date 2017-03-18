
var Cellar = React.createClass({
  getInitialState: function() {
    return { message: 'Il ne reste plus que ça dans votre cave:' };
  },
  render: function() {
    return (
      <div>
            <p>{ this.state.message }</p>
      </div>
    );
  }
});

ReactDOM.render(
  // usernameFromDjangoTestOnly is not a proper way to go
  <Cellar  />,
  document.getElementById('cellar-div')
);
