import React from 'react';

/* This is the wrapper component */
class App extends React.Component {

    state = initialData // from server? database/Gameplan table?

    render() {
        return (
            <div className="app">
                <Sidebar startTime={startTime} endTime={endTime}/>
                <DragDropArea />
                <Content tasks={tasks} />
            </div>
        ) 
    }
}

/* Sidebar that displays the time */
class Sidebar extends React.Component {
    render() {
        return (
            <div className="sidebar">
                <span className="time"></span>
            </div>
        )
    }
}

/* Area where tasks will be dragged/dropped to arrange the order.*/
class DragDropArea extends React.Component {
    render() {
        return (
            <div className="dndarea">
            </div>
        )
    }
}

/* What will be displayed inside the draggable components*/
class Content extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            tasks: []
        };
    }

    /* GET request just before mounted into the DOM--> get from DB? */
    componentWillMount() {
        this.setState({ tasks: data});
    }

    render() {
        const {tasks} = this.props;

        return(
            <div className="content">
                {/* gameplan task item */}
                {tasks.map((task) => (
                    <TaskItem
                        task={task} />
                ))}
            </div>
        )
    }
}

/* Individual Task component */
class TaskItem extends React.Component {
    render() {
        const {tasks} = this.props; 

        return (
            <div className="item">
                <div className="taskName">
                    { task.name }
                </div>
                <div className="taskStartTime">
                    { task.startTime}
                </div>
                <div className="taskEndTime">
                    {task.endTime}
                </div>
                <div className="markComplete"></div>
                <div className="deleteTask"></div>
            </div>
        )
    }
}

export default App;

ReactDOM.render(<App />, document.getElementById('root'));

// if want to handle any form input, can create a Form class --> real time 
// editing or updating the database

//class Form extends React.Component {
    //..
    //render() {
        //return (
        //<form onSubmit={this.submitForm.bind(this)}>
            //<input
            //type, etc.../>
        //</form>
        //)
    //}
//}