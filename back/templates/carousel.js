document.addEventListener('DOMContentLoaded', function() {
    const movieRow = document.querySelector('.movie-row');
    const prevButton = document.querySelector('.prev');
    const nextButton = document.querySelector('.next');
    
    // Cantidad de películas a desplazar
    const scrollAmount = 3;
    
    nextButton.addEventListener('click', () => {
        const movieWidth = document.querySelector('.movie-item').offsetWidth;
        movieRow.scrollLeft += movieWidth * scrollAmount;
    });
    
    prevButton.addEventListener('click', () => {
        const movieWidth = document.querySelector('.movie-item').offsetWidth;
        movieRow.scrollLeft -= movieWidth * scrollAmount;
    });
    
    // Efecto hover mejorado
    const movieItems = document.querySelectorAll('.movie-item');
    movieItems.forEach(item => {
        item.addEventListener('mouseenter', () => {
            item.style.zIndex = '1';
        });
        
        item.addEventListener('mouseleave', () => {
            item.style.zIndex = '0';
        });
    });
}); 