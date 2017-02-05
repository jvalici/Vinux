
var RandomMessage = React.createClass({
  getInitialState: function() {
    return { message: 'Hello, Universe' };
  },
  onClick: function() {
    var messages = ['Hello, World', 'Hello, Planet', 'Hello, Universe'];
    var randomMessage = messages[Math.floor((Math.random() * 3))];

    this.setState({ message: randomMessage });
  },
  render: function() {
    return (
      <div>
        <MessageView message={ this.state.message }/>
        <p><input type="button" onClick={ this.onClick } value="Change Message"/></p>
      </div>
    );
  }
});

var MessageView = React.createClass({
  render: function() {
    return (
      <p>{ this.props.message }</p>
    );
  }
});

ReactDOM.render(
  <RandomMessage />,
  document.getElementById('greeting-div')
);
