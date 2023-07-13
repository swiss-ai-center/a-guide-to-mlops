// parallax effect with image on scroll with pure javascript

// wait for the window to load
window.addEventListener('load', function () {
    // get the images
    const elements = document.getElementsByClassName('parallax');

    // listen for scroll event and call animate function
    document.addEventListener('scroll', () => parallax(elements));
});

function parallax(elements) {
    // loop through each element
    for (let i = 0; i < elements.length; i++) {
        const element = elements[i];
        // get speed data attribute
        const speed = element.getAttribute('data-speed');

        // get scroll position
        const scroll = window.scrollY;

        const offset = -scroll / speed;

        // set the transform style
        element.style.transform = 'translateY(' + offset + 'px)';
    }
}
