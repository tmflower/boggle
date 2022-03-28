const $form = $('.check-word')
const $word = $('.word')
const yourWords = new Set();

$form.on('submit', checkWord, startCountdown(30));

async function checkWord(evt) {
    evt.preventDefault();
    const word = $word.val();

    if (!word) return;
    const resp = await axios.get('/check-word', { params: { word: word }})

    const response = resp.data.response;
    $('#feedback').text(response);

    if (response === 'ok' && yourWords.has(word) == false) {
        keep_score();
        $(`<li>${word}</li>`).appendTo('ul')
        yourWords.add(word);
    }
    $form.trigger('reset')
}

let score = 0;
function keep_score() {    
    const word = $word.val();
    const points = word.length;
    score = score + points;  
    $('#score').text(`Score: ${score}`)
}

function startCountdown(seconds) {
    let counter = seconds;
    const interval = setInterval(() => {
    $('#timer').text(`Time remaining: ${counter} seconds`)
    counter--;

    if (counter < 0) {
        clearInterval(interval)
        $('.word').addClass('disabled').prop('disabled', true)
        $('#timer').text(`Sorry! Time's up!`)
        $('#score').text(`Game over! Your final score is ${score}`);
        $('#replay').css('display', 'block');
        endGame(); 
    }
  }, 1000);
}

async function endGame() {
    await axios.post('/game-over', { score: score });
}
