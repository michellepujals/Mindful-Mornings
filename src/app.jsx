import React from 'react';
import { DragDropContext } from 'react-beautiful-dnd';
import initialData from './initial-data.js';
import Column from './column.jsx';

/* This is the wrapper component for the entire app*/
export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = initialData;
  }

  onDragEnd(result) { 

    const { destination, source, draggableId } = result;

    if (!destination) {
      return;
    }

    if (
      destination.droppableId === source.droppableId &&
      destination.index === source.index
    ) {
      return;
    }

    const column = this.state.columns[source.droppableId];
    const newTaskIds = Array.from(column.taskIds);
    newTaskIds.splice(source.index, 1);
    newTaskIds.splice(destination.index, 0, draggableId);

    const newColumn = {
      ...column, 
      taskIds: newTaskIds,
    };

    this.setState((state) => {
      return {
        columns: {
          ...this.state.columns,
          [newColumn.id]: newColumn
        }
      }
    });
  }

  render() {
    return (
      <DragDropContext onDragEnd={(result) => this.onDragEnd(result)}>
        {this.state.columnOrder.map(columnId => {
          const column = this.state.columns[columnId];
          const tasks = column.taskIds.map(taskId => this.state.tasks[taskId]);

          return <Column key={column.id} column={column} tasks={tasks} />;
        })}
      </DragDropContext>
    );
  }
}
