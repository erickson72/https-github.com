const modalBtns = [...document.getElementsByClassName('modal-button')]
const modalBody = document.getElementById('modal-body-confirm')

const url =  window.location.href


modalBtns.forEach(modalBtn=> modalBtn.addEventListener('click',()=>{
    const pk = modalBtn.getAttribute('data-pk')
    const categoryName = modalBtn.getAttribute('data-category')
    const numberOfQuestions = modalBtn.getAttribute('data-numbers-questions')
    const difficulty = modalBtn.getAttribute('data-difficulty')
    const scorreToPass = modalBtn.getAttribute('data-score-pass')
    const time = modalBtn.getAttribute('data-time')
    const startButton = document.getElementById('start-button')

    modalBody.innerHTML = 
    `<div class="h5 mb-3">Deseja realmente jogar <b>${categoryName}</b>?</div>
    
    <div class="text-muted">
        <ul class="list-group list-group-flush">
            <li class="list-group-item"> Nível: <b>${difficulty}</b>
            <li class="list-group-item"> Total de questões: <b>${numberOfQuestions}</b>
            <li class="list-group-item"> Pontuação desejável: <b>${scorreToPass}%</b>
            <li class="list-group-item"> Tempo estimado: <b>${time} minutos</b>
        </ul>
    </div>
    `

    startButton.addEventListener('click',()=>{
        window.location.href = url + pk
    })
})) 




