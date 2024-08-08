const form = document.getElementById('sort');
form.addEventListener('submit', (event) => {
    event.preventDefault(); 
    const option = document.getElementById('key');
    
    p = document.getElementsByName('parameters')[0].value.replace(/'/g, '"');
    params = JSON.parse(p);
    params['reverse'] = false;
    params['sort'] = option.value;


    fetch('http://127.0.0.1:5000/sort_adv', {
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