// Bouncing Button Animation
document.querySelectorAll('button').forEach((button) => {
    button.addEventListener('mouseover', () => {
        button.style.animation = 'bounce 1s';
    });

    button.addEventListener('mouseout', () => {
        button.style.animation = '';
    });
});

// Interactive Icons (Spin on Click)
document.querySelectorAll('.icon').forEach((icon) => {
    icon.addEventListener('click', () => {
        icon.classList.add('spin');
        setTimeout(() => {
            icon.classList.remove('spin');
        }, 2000); // Remove spin class after animation
    });
});

// Quiz Interactive Effects
document.querySelectorAll('.card').forEach((card) => {
    card.addEventListener('click', () => {
        card.style.backgroundColor = '#00BFFF';
        card.style.color = '#FFF8DC';
        setTimeout(() => {
            card.style.backgroundColor = '#FFEB3B';
            card.style.color = '#228B22';
        }, 500);
    });
});

// Greeting Message on Page Load
window.addEventListener('load', () => {
    alert("Welcome to the Gamified Learning Platform! Let's have fun while learning!");
});
