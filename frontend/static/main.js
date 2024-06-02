document.addEventListener("DOMContentLoaded", function () {
    fetchTasks();
});

function fetchTasks() {
    fetch('http://localhost:5000/api/tasks', {
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
        }
    })
    .then(response => response.json())
    .then(data => {
        const tasksList = document.getElementById('tasks');
        tasksList.innerHTML = '';
        data.forEach(task => {
            const taskItem = document.createElement('li');
            taskItem.className = 'list-group-item d-flex justify-content-between align-items-center';
            taskItem.innerHTML = `
                <span>${task.title}</span>
                <div>
                    <button class="btn btn-sm btn-success" onclick="toggleTask(${task.id}, ${task.completed})">${task.completed ? 'Pending' : 'Completed'}</button>
                    <button class="btn btn-sm btn-danger" onclick="deleteTask(${task.id})">Delete</button>
                </div>
            `;
            tasksList.appendChild(taskItem);
        });
    });
}

function addTask() {
    const newTask = document.getElementById('new-task').value;
    fetch('http://localhost:5000/api/tasks', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
        },
        body: JSON.stringify({ title: newTask })
    })
    .then(response => response.json())
    .then(data => {
        fetchTasks();
        document.getElementById('new-task').value = '';
    });
}

function toggleTask(id, completed) {
    fetch(`http://localhost:5000/api/tasks/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
        },
        body: JSON.stringify({ completed: !completed })
    })
    .then(response => response.json())
    .then(() => {
        fetchTasks();
    });
}

function deleteTask(id) {
    fetch(`http://localhost:5000/api/tasks/${id}`, {
        method: 'DELETE',
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
        }
    })
    .then(response => response.json())
    .then(() => {
        fetchTasks();
    });
}
