// JavaScript for Fetching Data from Backend API


document.addEventListener('DOMContentLoaded', function() {
    // Fetch book listing data
    fetch('/books')
        .then(response => response.json())
        .then(data => {
            const bookList = document.getElementById('book-list');
            data.books.forEach(book => {
                const bookItem = document.createElement('div');
                bookItem.classList.add('book-item');
                bookItem.innerHTML = `
                    <h3>${book.title}</h3>
                    <p>Author: ${book.author}</p>
                `;
                bookList.appendChild(bookItem);
            });
        })
        .catch(error => console.error('Error fetching book listing:', error));

    // Fetch exchange history data for user with ID 1 (example)
    fetch('/exchanges/history/1')
        .then(response => response.json())
        .then(data => {
            const historyList = document.getElementById('history-list');
            data.forEach(exchange => {
                const exchangeItem = document.createElement('div');
                exchangeItem.classList.add('exchange-item');
                exchangeItem.innerHTML = `
                    <h3>Exchange ID: ${exchange.exchange_id}</h3>
                    <p>Book: ${exchange.book_title}</p>
                    <p>Status: ${exchange.status}</p>
                `;
                historyList.appendChild(exchangeItem);
            });
        })
        .catch(error => console.error('Error fetching exchange history:', error));
});
