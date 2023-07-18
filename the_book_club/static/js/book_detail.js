document.addEventListener('DOMContentLoaded', () => {
    const statusSelect = document.querySelector('#status-select');
    const currentStatus = '{{ user_book.status }}';
    statusSelect.value = currentStatus;

    statusSelect.addEventListener('change', () => {
        const selectedStatus = statusSelect.value;
        const bookId = '{{ book.id }}';
        const url = `/update_book_status/${bookId}/${selectedStatus}/`;

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Обновление статуса книги на странице
                if (data.status_text === 'Не выбрано') {
                    document.querySelector('.book-status-details').innerHTML = '';
                } else if (data.status_text === 'Хочу прочитать') {
                    document.querySelector('.book-status-details').innerHTML = '';
                } else if (data.status_text === 'Прочитана') {
                    const dateRead = data.date_read ? new Date(data.date_read).toLocaleDateString('en-US') : '';
                    document.querySelector('.book-status-details').innerHTML = '';
                }
            } else {
                // В случае ошибки отображаем сообщение пользователю
                console.log('Ошибка при обновлении статуса книги');
            }
        })
        .catch(error => {
            console.log('Ошибка при обновлении статуса книги:', error);
        });
    });
});
