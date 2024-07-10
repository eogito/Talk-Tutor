const words = document.querySelectorAll('.word');

let currentIndex = 0;

function animateWords() {
    if (currentIndex < words.length) {
        words[currentIndex].style.opacity = '1';
        words[currentIndex].style.transform = 'translateY(0)';
        currentIndex++;
    } else {
        currentIndex = 0; 
        words.forEach(word => {
            word.style.opacity = '0';
        });
    }
}

setInterval(animateWords, 700); 

const wrds = document.querySelectorAll('.wrd');

let current = 0;

function animateWrds() {
    if (current < wrds.length) {
        wrds[current].style.opacity = '1';
        wrds[current].style.transform = 'translateY(0)';
        current++;
    }
}

setInterval(animateWrds, 500); 
