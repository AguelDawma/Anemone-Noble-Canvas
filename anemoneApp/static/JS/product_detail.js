function scrollGallery(direction){
    const container = document.getElementById('productGallery')
    const itemWidth = container.querySelector('.scroll-item').clientWidth + 10;

    container.scrollBy({
        left: direction * itemWidth,
        behavior: 'smooth',
    });
};

function openModal(src, altText){
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('fullImage');
    const captionText = document.getElementById('caption');

    modal.style.display = "block";
    modalImg.src = src;
    captionText.innerHTML = altText;
}

document.querySelector('.close-modal').onclick = function() {
    document.getElementById('imageModal').style.display = "none"
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}