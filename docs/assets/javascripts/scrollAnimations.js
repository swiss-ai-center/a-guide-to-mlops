window.addEventListener('load', function () {
    const elements = document.getElementsByClassName('scroll-fade-out');
    document.addEventListener('scroll', () => scrollFadeOut(elements));
});

function scrollFadeOut(elements) {
    for (let i = 0; i < elements.length; i++) {
        const element = elements[i];
        const offset = element.getAttribute('data-offset');
        const scroll = window.scrollY;

        if (scroll > offset) {
            element.style.opacity = 0;
        } else {
            element.style.opacity = "";
        }
    }
}
