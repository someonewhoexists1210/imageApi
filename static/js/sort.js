const form = document.getElementById('sort');
form.addEventListener('submit', (event) => {
    event.preventDefault(); 
    const option = document.getElementById('key');
    const action = option.value === 'date' ? '/sort' : '';
    form.action = action;
    form.method = 'post';
    if (action === '') {
        s = option.value;
        console.log(images)
    }else{
        form.submit();
    }
});