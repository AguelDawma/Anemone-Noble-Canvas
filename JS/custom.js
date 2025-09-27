document.addEventListener('DOMContentLoaded' , function(){
    const arts = document.querySelectorAll('.art');
    const garments = document.querySelectorAll('.garment');
    const next = document.getElementById('next');
    
    const main = document.querySelectorAll('main');
    const errorMessage = document.getElementById('error-message');

    next.disabled = true;

    function nextButtonState(){
        const selectedArt =document.querySelector('.art.selected');
        const selectedGarment = document.querySelector('.garment.selected');

        next.disabled = !(selectedArt && selectedGarment);

        if(!(next.disabled)){
            errorMessage.textContent = "Please choose an art and a garment to continue.";
        }
    }

    arts.forEach(item=>{
        item.addEventListener('click' , function(){
            arts.forEach(otherItem=>{
                otherItem.classList.remove('selected');
            });

            item.classList.add('selected');
            nextButtonState();
        })
    })

    garments.forEach(item=>{
        item.addEventListener('click' , function(){
            garments.forEach(otherItem=>{
                otherItem.classList.remove('selected');
            });
            
            item.classList.add('selected');
            nextButtonState();
        })
    })

    nextButtonState()

    next.addEventListener('click' , function(){
        const selectedArt =document.querySelector('.art.selected');
        const selectedGarment = document.querySelector('.garment.selected');
        
        const artId = selectedArt.dataset.id;
        const garmentId = selectedGarment.dataset.id;

        const nextPage =  'custom.html?art=${encodeURIComponent(artId)}&garment=${encodeURIComponent(garmentId)}';

        window.location.href = nextPage;
    })
})