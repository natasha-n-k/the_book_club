document.addEventListener('DOMContentLoaded', function() {
    const clampedElements = document.querySelectorAll('.clamp');
    // Для каждого элемента добавляем обработчик клика
    clampedElements.forEach((element) => {
        element.addEventListener('click', () => {
            element.classList.toggle('expanded');
        });
    });
});
