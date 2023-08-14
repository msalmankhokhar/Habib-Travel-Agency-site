let delBtns = document.querySelectorAll('.btn.cardbtn.del');

delBtns.forEach(delbtn => {
    delbtn.addEventListener('click', (e)=>{
        e.preventDefault();
        confirmation = window.confirm('Are you sure to delete this Package ?');
        if (confirmation) {
            window.location.href = delbtn.href;
        }
    })
});