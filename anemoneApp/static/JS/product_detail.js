function scrollGallery(direction){
    const container = document.getElementById('productGallery')
    const itemWidth = container.querySelector('.scroll-item').clientWidth + 10;

    container.scrollBy({
        left: direction * itemWidth,
        behavior: 'smooth',
    });
};

const modal = document.getElementById('imageModal');

function openModal(src, altText){
    const modalImg = document.getElementById('fullImage');
    const captionText = document.getElementById('caption');

    if(modal){
        modal.style.display = "block";
        modalImg.src = src;
        captionText.innerHTML = altText;
    }
}

document.querySelector('.close-modal').onclick = function() {
    document.getElementById('imageModal').style.display = "none"
}

if(modal){
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
}