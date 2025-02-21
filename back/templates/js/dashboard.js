document.addEventListener('DOMContentLoaded', function() {
    // Inicializar todos los carruseles
    const swipers = document.querySelectorAll('.swiper-container');
    swipers.forEach(swiperContainer => {
        new Swiper(swiperContainer, {
            slidesPerView: 'auto',
            spaceBetween: 20,
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
            breakpoints: {
                320: {
                    slidesPerView: 1,
                    spaceBetween: 10
                },
                480: {
                    slidesPerView: 2,
                    spaceBetween: 20
                },
                768: {
                    slidesPerView: 3,
                    spaceBetween: 30
                },
                1024: {
                    slidesPerView: 4,
                    spaceBetween: 30
                }
            }
        });
    });

    // Manejar favoritos
    document.querySelectorAll('.btn-favorite').forEach(button => {
        button.addEventListener('click', function() {
            const movieId = this.dataset.movieId;
            toggleFavorite(movieId);
        });
    });

    // Manejar watchlist
    document.querySelectorAll('.btn-watchlist').forEach(button => {
        button.addEventListener('click', function() {
            const movieId = this.dataset.movieId;
            toggleWatchlist(movieId);
        });
    });
});

function toggleFavorite(movieId) {
    this.classList.toggle('active');
    // Aquí irá la lógica para guardar en favoritos
}

function toggleWatchlist(movieId) {
    this.classList.toggle('active');
    // Aquí irá la lógica para guardar en watchlist
} 