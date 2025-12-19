document.addEventListener('DOMContentLoaded', ()=>{
    const categories = document.querySelectorAll('.category-bar span')
    const track = document.querySelector('.slider-track');

    categories.forEach((span, index) => {

        span.addEventListener('click', () => {

            categories.forEach(s => {
                s.classList.remove('active');
            });

            span.classList.add('active');

            const movePercentage = index * -100;
            track.style.transform = `translateX(${movePercentage}vw)`;

        });
    });
});