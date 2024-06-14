const urlQuiz =  window.location.href
const quizBox = document.getElementById('quizz-box')
let questions
$.ajax({
    type:'GET',
    url: `${urlQuiz}data`,
    success: function(response) {
        console.log(response)
        questions = response.data
        questions.forEach(element => {
            for (const [question, answers] of Object.defineProperties(element)){
                console.log(question)
                console.log(answers)
            }
                
           
        });
    },
    error: function(error) {
        console.log(error)
    }
})