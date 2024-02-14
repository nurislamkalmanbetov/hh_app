document.addEventListener('DOMContentLoaded', function() {
    var currentTime = new Date();
    var hours = currentTime.getHours();
    var minutes = currentTime.getMinutes();
    var seconds = currentTime.getSeconds();
    
    // Преобразование чисел < 10 в формат "0X"
    hours = (hours < 10) ? '0' + hours : hours;
    minutes = (minutes < 10) ? '0' + minutes : minutes;
    seconds = (seconds < 10) ? '0' + seconds : seconds;
    
    // Форматирование времени в формат HH:MM:SS
    var timeString = hours + ':' + minutes + ':' + seconds;
    
    // Находим элемент с id "current-time" и заменяем его содержимое на текущее время
    var currentTimeElement = document.getElementById('current-time');
    if (currentTimeElement) {
        currentTimeElement.textContent = timeString;
    }
});
