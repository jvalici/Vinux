////////////////////////////////////////////////////////////////////////////////
//------------------------------------------------------------------------------
// information to show when the row is expended
class RowExtension extends React.Component {
    render() {
        if ( this.props.data.removalDate == "" ) {
            return (
                <div>
                    <p>Date d'ajout: {this.props.data.additionDate}</p>
                </div> );
        }
        else {
            return (
                <div>
                    <p>Date d'ajout: {this.props.data.additionDate}</p>
                    <p>Date de retrait: {this.props.data.removalDate} </p>
                </div> );
        }

    }
}

