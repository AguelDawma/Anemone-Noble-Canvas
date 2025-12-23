let lastChecked = null;

function toggleRadio(radio){
    if(lastChecked == radio){
        radio.checked = false;
        lastChecked = null;
    }else{
        lastChecked = radio;
    }
}

document.addEventListener('DOMContentLoaded' , function(){
    const arts = document.querySelectorAll('.art');
    const garments = document.querySelectorAll('.garment');
    const next = document.getElementById('next');
    
    const main = document.querySelectorAll('main');
    const errorMessage = document.getElementById('error-message');

    if(next){
        next.disabled = true;
        function nextButtonState(){
            const selectedArt =document.querySelector('.art.selected');
            const selectedGarment = document.querySelector('.garment.selected');

            next.disabled = !(selectedArt && selectedGarment);

            if(next.disabled){
                errorMessage.textContent = "Please choose an art and a garment to continue.";
            }else{
                errorMessage.textContent = "";
            }
        }

        function deselect(item){
            item.classList.remove('selected');
        }

        arts.forEach(item=>{
            item.addEventListener('click' , function(){

                if(item.classList.contains('selected')){
                    deselect(item);
                    nextButtonState();
                }else{
                    arts.forEach(otherItem=>{
                        otherItem.classList.remove('selected');
                    });
                    item.classList.add('selected');
                    nextButtonState();
                }
            })
        })

        garments.forEach(item=>{
            item.addEventListener('click' , function(){
                
                if(item.classList.contains('selected')){
                    deselect(item);
                    nextButtonState();
                }else{
                    garments.forEach(otherItem=>{
                        otherItem.classList.remove('selected');
                    });
                    item.classList.add('selected');
                    nextButtonState();
                }
            })
        })

        nextButtonState()
    }

})