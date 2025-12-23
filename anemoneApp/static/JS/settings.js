document.querySelector('input[type="file"]').onchange = function(event){
    const [file] = this.files;
    if(file){
        document.getElementById('pic-preview').src = URL.createObjectURL(file);
    }
};