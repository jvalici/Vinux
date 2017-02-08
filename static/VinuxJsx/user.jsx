
var GreatingMessage = React.createClass({
  getInitialState: function( userName ) {
    return { message: 'Hello, ' + userName };
  },
  render: function() {
    return (
      <div>
        <MessageView message={ this.state.message }/>
      </div>
    );
  }
});

ReactDOM.render(
  <GreatingMessage />,
  document.getElementById('greeting-div')
);
