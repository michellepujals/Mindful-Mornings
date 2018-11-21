/* This is the wrapper component for the entire app*/
class Hello extends React.Component {
    render() {
        return <p>Hi World!</p>;
    }
}

//Puts the App into the DOM
ReactDOM.render(<Hello />, document.getElementById('root'));