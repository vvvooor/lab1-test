// Массив для хранения задач
let tasks = [];

// Переменная для текущего фильтра (все задачи, выполненные, невыполненные)
let currentFilter = 'all';

// Добавление новой задачи
function addTask() {
    const input = document.getElementById('taskInput'); // Получаем поле ввода
    const taskText = input.value; 

    
        tasks = [...tasks, { text: taskText, completed: false }]; // Добавляем новую задачу
        input.value = ''; // Очищаем поле ввода
        renderTasks(); // Перерисовываем список задач
    
}

// Переключение статуса задачи
function toggleTask(index) {
    tasks = tasks.map((task, i) =>
        i === index ? { ...task, completed: !task.completed } : task
    ); // Меняем статус задачи
    renderTasks(); // Перерисовываем список
}

// Удаление задачи
function deleteTask(index) {
    tasks = tasks.filter((_, i) => i !== index); // Удаляем задачу
    renderTasks(); // Перерисовываем список
}

// Фильтрация задач
function filterTasks(filter) {
    currentFilter = filter; // Устанавливаем текущий фильтр
    renderTasks(); // Перерисовываем список
}

// Отображение задач
function renderTasks() {
    const taskList = document.getElementById('taskList'); // Получаем список задач
    taskList.innerHTML = ''; // Очищаем текущий список

    const filteredTasks = tasks.filter(task => { // Фильтруем задачи
        if (currentFilter === 'completed') return task.completed; // Выполненные
        if (currentFilter === 'active') return !task.completed; // Невыполненные
        return true; // Все задачи
    });

    filteredTasks.forEach((task, index) => {
        const li = document.createElement('li'); 
        li.className = 'task'; 

        const text = document.createElement('span'); 
        text.textContent = task.text; 
        if (task.completed) text.classList.add('completed');

        const checkbox = document.createElement('input'); 
        checkbox.type = 'checkbox';
        checkbox.checked = task.completed;
        checkbox.onchange = () => toggleTask(index);

        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Удалить'; 
        deleteButton.onclick = () => deleteTask(index); 

        li.appendChild(checkbox); 
        li.appendChild(text); 
        li.appendChild(deleteButton);
        taskList.appendChild(li); 
    });
}
