document.addEventListener('DOMContentLoaded', function(){
    const paintings = document.querySelectorAll('.painting');
    const positionSelector = document.getElementById('positions-selector');

    paintings.forEach(item => {
        item.addEventListener('click' , function(){
            paintings.forEach(otherItem => {
                otherItem.classList.remove('selected');
            });

            item.classList.add('selected');

            const pElement = item.querySelector('p');
            if(pElement){
                const selectedText = pElement.textContent;
                console.log("You have chosen to paint on the", selectedText);
            }

            if(item.id=='chest'){
                positionSelector.value = "left-chest";
            }else if(item.id=='back'){
                positionSelector.value = "back";
            }else if(item.id=='shoulder'){
                positionSelector.value = "left-shoulder";
            }
        });
    });
});