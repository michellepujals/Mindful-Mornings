/* React components*/

class EditableText extends React.Component {
  constructor(props) {
    super(props);

    const focusInput = props.editing;

    // Creates a reference to the input's DOM node
    this.textInput = React.createRef();

    this.state = {
      focusInput,
      value: props.value,
      editing: props.editing
    };
  }

  handleInputChange = (evt) => {

    // When the input changes, set this.state.value to the
    // value of the input
    this.setState({ value: evt.target.value });
  }

  handleOnBlur = (evt) => {
    // onBlur gets fired when you can no longer type in the input

    this.setState({
      editing: false,
      value: evt.target.value
    });
  }

  handleTextClick = (evt) => {
    // Focuses the text input when this.state.editing is true

    this.setState({ editing: true });
  }

  componentDidUpdate() {

    // Every time the component updates, checks if
    // this.state.editing is true and if this.textInput exists in the DOM
    if (this.state.editing === true && this.textInput) {
      this.textInput.current.focus();
    }
  }

  render() {
    const { editing, value } = this.state;

    const input = (
      <input
        className="editable-text"
        autofocus
        type="text"
        value={value}
        onChange={this.handleInputChange}
        onBlur={this.handleOnBlur}
        ref={this.textInput}  // Need this to access the DOM node
      />
    );
    const text = (
      <p className="editable-text" onClick={this.handleTextClick}>
        {value}
      </p>
    );

    const editableText = editing ? input : text;

    return (
      <div className={this.props.className}>
        {editableText}
      </div>
    );
  }
}

ReactDOM.render(
  <EditableText value="Click on me to edit" />,
  document.getElementById('stateful-component1')
);

ReactDOM.render(
  <EditableText value="Click on me to edit" />,
  document.getElementById('stateful-component2')
);

ReactDOM.render(
  <EditableText value="Click on me to edit" />,
  document.getElementById('stateful-component3')
);
