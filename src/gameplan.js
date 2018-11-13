import React from 'react';
import ReactDOM from 'react-dom';


function Table(props) {
  // A list of row info. Each row will be an object.
  const rows = props.rows;
  // A list of column names. We'll use them to make the table's headers
  const colNames = props.colNames;
  
  const colNamesHtml = colNames.map(colName => {

    return <th>{colName}</th>;  // <th>Name</th>
  });
  
  // <thead>
  //   <th>Name</th>
  //   <th>Rind Color</th>
  //   <th>Flesh Color</th>
  // </thead>
  const tableHeader = <thead>{colNamesHtml}</thead>;
  
  const tableRows = rows.map(row => {
    const rowData = [];
    
    for (let rowAttr in row) {
      rowData.push(<td>{row[rowAttr]}</td>);
    }
    
    return <tr>{rowData}</tr>;
  });
  
  return (
    <table className="table">
      {tableHeader}
      {tableRows}
    </table>
  );
}

const rows = [
  {
    name: 'watermelon',
    rindColor: 'green',
    fleshColor: 'pink'
  },
  {
    name: 'cantaloupe',
    rindColor: 'tan',
    fleshColor: 'orange'
  }
];

ReactDOM.render((
  <Table
    rows={rows}
    colNames={[ 'Name', 'Rind Color', 'Flesh Color' ]}
  />
), document.getElementById('root'));


// Now let's add some interactivity!

// I want to make my table rows editable. When you click on an item,
// you'll be able to edit the text inside.

// To optimize though, we'll have to break up the Table component into smaller ones (whoops)

function EditableTableData(props) {
  // Is the data currently being edited? (true/false)
  const editing = this.props.editing;
  
  const data = this.props.data;
  const inputName = this.props.inputName;
  
  if (editing) {
    return <td><input type="text" value={data} /></td>
  } else {
    return <td>
  }
}

class TableEditor extends React.Component {
  constructor(props) {
    super(props);
    
    this.state = {
      rows: props.rows
    };
  }
  
  render() {
    
  }
}