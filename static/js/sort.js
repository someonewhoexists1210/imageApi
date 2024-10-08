const form = document.getElementById('sort');
form.addEventListener('submit', (event) => {
    event.preventDefault(); 
    const option = document.getElementById('key');
    
    params = {
        'q': document.getElementsByName('query')[0].value, 
        'num': document.getElementsByName('num')[0].value,
        'sort': option.value,
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
       images = data['images'];
        cards = document.getElementsByClassName('image-card');
        for (i = 0; i < cards.length; i++) {
            cards[i].innerHTML = `
                <img src="${images[i].image_link}" alt="Image could not load"><br>
                <a href="${images[i].context_link}">${images[i].title}</a>
            `;
        }
    })
});