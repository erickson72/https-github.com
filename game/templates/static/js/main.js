const modalBtns = [...document.getElementsByClassName('modal-button')]
const modalBody = document.getElementById('modal-body-confirm')



modalBtns.forEach(modalBtn => modalBtn.addEventListener('click', () => {
    const pk = modalBtn.getAttribute('data-pk')
    const categoryName = modalBtn.getAttribute('data-category')
    const startButton = document.getElementById('start-button')

    

    const id = modalBtn.getAttribute('data-id')
    const difficulty = modalBtn.getAttribute('difficulty')

   console.log(difficulty)
   console.log(id)

    modalBody.innerHTML =
        `<div class="h5 mb-3">Deseja realmente jogar <b>${categoryName}</b>?</div>

        `

       

    startButton.addEventListener('click', () => {
        window.location.href = url + pk
    })
}))




