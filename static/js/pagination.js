let currentPage = 1;
const hiddenDivs = document.querySelectorAll('.gr');
const currentPageSpan = document.querySelector('.current-page');

function showPage(pageNumber) {
    const startIndex = pageNumber - 1;
    currentPageSpan.innerHTML = pageNumber + ' / ' + hiddenDivs.length;

    hiddenDivs.forEach((div, index) => {
        if (index == startIndex) {
            div.style.display = 'block';
        } else {
            div.style.display = 'none';
        }
    });
}

function prevPage() {
    if (currentPage > 1) {
        currentPage--;
        showPage(currentPage);
    }
}

function nextPage() {
    if (currentPage < hiddenDivs.length) {
        currentPage++;
        showPage(currentPage);
    }
}

showPage(currentPage);