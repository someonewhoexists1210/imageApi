let currentPage = 1;
const hiddenDivs = document.querySelectorAll('.gr');

function showPage(pageNumber) {
    const startIndex = pageNumber - 1;

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