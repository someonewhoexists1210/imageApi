const form = document.getElementById('sort');
form.addEventListener('submit', (event) => {
    event.preventDefault(); 
    const option = document.getElementById('key');
    
    params = {
        'query': document.getElementsByName('query')[0].value, 'sort': option.value,
        'num': document.getElementsByName('num')[0].value,
        'reverse': false,
    };


    fetch('http://127.0.0.1:5000/sort', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(params),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        cards = document.getElementsByClassName('image-cards');
        for (i = 0; i < cards.length; i++) {
            cards[i].innerHTML = `
                <img src="${data[i].image_link}" alt="Image could not load"><br>
                <a href="${data[i].context_link}">${data[i].title}</a>
            `;
        }
    })
});