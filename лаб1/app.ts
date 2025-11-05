// Функция для добавления числа или оператора в экран
function addToInput(value: string): void {
    const input = <HTMLInputElement>document.getElementById('input'); // Получаем элемент ввода по ID 'input' и приводим его к типу HTMLInputElement
    input.value += value; // Добавляем новое значение (число или оператор) к текущему значению строки
}

// Функция для очистки ввода
function clearInput(): void {
    const input = <HTMLInputElement>document.getElementById('input'); // Получаем элемент ввода по ID 'input'
    input.value = ''; // Устанавливаем пустую строку, тем самым очищая ввод
}

// Чистая функция для выполнения математических операций
function evaluateExpression(expression: string): number {
    // Заменяем символ '^' на '**' для возведения в степень в JavaScript
    expression = expression.replace(/\^/g, '**');
    try {
        return new Function('return ' + expression)(); // Динамически вычисляем выражение из строки и возвращаем результат
    } catch (error) {
        return NaN; // Если в выражении ошибка (например, некорректные символы), возвращаем NaN
    }
}

// Функция для вычисления результата
function calculate(): void {
    const input = <HTMLInputElement>document.getElementById('input'); // Получаем элемент ввода по ID 'input'
    const result = evaluateExpression(input.value); // Передаем текущее выражение в поле ввода в функцию evaluateExpression для вычисления
    input.value = result.toString(); // Преобразуем результат в строку и отображаем его в поле ввода
}

// Новая функция для вычисления квадратного корня
function squareRoot(): void {
    const input = <HTMLInputElement>document.getElementById('input'); // Получаем элемент ввода по ID 'input'
    const value = parseFloat(input.value); // Преобразуем строку ввода в число с плавающей точкой
    if (!isNaN(value)) { // Проверяем, является ли преобразованное значение корректным числом
        input.value = Math.sqrt(value).toString(); // Вычисляем квадратный корень числа и преобразуем результат в строку
    } else {
        input.value = 'Ошибка'; // Если значение не является числом, отображаем сообщение об ошибке
    }
}