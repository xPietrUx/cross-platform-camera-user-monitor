<script lang="ts">
    import { onMount } from 'svelte';

    let currentSlide = 0;
    const slides = [
        {
            title: 'Monitorowanie w Czasie Rzeczywistym',
            description:
                'Aplikacja śledzi Twoją aktywność i skupienie, analizując obraz z kamery, aby pomóc Ci lepiej zarządzać czasem.',
            imageUrl:
                'https://images.unsplash.com/photo-1526628953301-3e589a6a8b74?q=80&w=2006&auto=format&fit=crop',
        },
        {
            title: 'Inteligentna Analiza Otoczenia',
            description:
                'Program wykrywa potencjalne rozproszenia w Twoim otoczeniu, pomagając utrzymać maksymalną koncentrację.',
            imageUrl:
                'https://images.pexels.com/photos/256219/pexels-photo-256219.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1',
        },
        {
            title: 'Prywatność jest Priorytetem',
            description:
                'Cała analiza obrazu odbywa się lokalnie na Twoim komputerze. Żadne dane wideo nie opuszczają Twojego urządzenia.',
            imageUrl:
                'https://images.unsplash.com/photo-1555949963-ff9fe0c870eb?q=80&w=2070&auto=format&fit=crop',
        },
        {
            title: 'Szczegółowe Raporty',
            description:
                'Przeglądaj podsumowania i statystyki swoich sesji, aby zrozumieć, co wpływa na Twoją efektywność.',
            imageUrl:
                'https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=2070&auto=format&fit=crop',
        },
    ];

    let interval: ReturnType<typeof setInterval>;

    // Funkcja do automatycznego przełączania slajdów
    function autoNextSlide() {
        currentSlide = (currentSlide + 1) % slides.length;
    }

    // Funkcja resetująca timer
    function resetTimer() {
        clearInterval(interval);
        interval = setInterval(autoNextSlide, 5000);
    }

    function nextSlide() {
        currentSlide = (currentSlide + 1) % slides.length;
        resetTimer(); // Resetuj timer
    }

    function prevSlide() {
        currentSlide = (currentSlide - 1 + slides.length) % slides.length;
        resetTimer(); // Resetuj timer
    }

    function goToSlide(index: number) {
        currentSlide = index;
        resetTimer(); // Resetuj timer
    }

    onMount(() => {
        // Uruchom timer po załadowaniu komponentu
        interval = setInterval(autoNextSlide, 5000);
        return () => clearInterval(interval);
    });
</script>

<style>
    .background-carousel {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -1;
        overflow: hidden;
    }

    .carousel {
        width: 100%;
        height: 100%;
        position: relative;
    }

    .page-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
        text-align: center;
        width: 100%;
        height: 100%;
        box-sizing: border-box;
    }

    .welcome-header {
        width: 100%;
        padding-top: 3vh; /* Dodano padding, aby odsunąć od góry */
    }

    .welcome-header h1 {
        text-shadow: var(--text-shadow);
        font-size: 2.5rem;
    }

    .welcome-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-top: var(--spacing-sm);
    }

    .slide {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        opacity: 0;
        transition: opacity 1s ease-in-out;
        visibility: hidden;
        background-size: cover;
        background-position: center;
    }

    .slide::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(25, 8, 40, 0.85);
    }

    .slide.active {
        opacity: 1;
        visibility: visible;
    }

    /* Styl dla tekstu karuzeli */
    .carousel-text-content {
        position: relative;
        width: 100%;
        max-width: 800px;
        flex-grow: 1; /* Pozwala zająć dostępną przestrzeń */
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .text-slide {
        position: absolute;
        width: 100%;
        height: auto; /* Wysokość dopasuje się do treści */
        opacity: 0;
        visibility: hidden;
        transition: opacity 0.5s ease-in-out;
    }

    .text-slide.active {
        opacity: 1;
        visibility: visible;
    }

    .text-slide h2 {
        font-size: 2rem;
        text-shadow: var(--text-shadow);
    }

    .text-slide p {
        margin-top: var(--spacing-md);
        font-size: 1.1rem;
        line-height: 1.5;
    }

    .page-footer {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: var(--spacing-md); /* Zmniejszony odstęp */
        width: 100%;
        padding-bottom: 2vh;
    }

    /* Nowy kontener dla głównego rzędu przycisków */
    .main-controls {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: var(--spacing-lg); /* Odstęp między przyciskami */
    }

    /* Nowa klasa dla przycisków nawigacyjnych */
    .nav-button {
        background: rgba(0, 0, 0, 0.3);
        color: var(--text-color);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 50%;
        width: 45px;
        height: 45px;
        font-size: 1.5rem;
        line-height: 45px;
        transition: background-color var(--animation-time);
        flex-shrink: 0; /* Zapobiega kurczeniu się przycisków */
    }

    .nav-button:hover {
        background: rgba(0, 0, 0, 0.5);
    }

    .dots {
        display: flex;
        gap: var(--spacing-md);
    }

    .dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background-color: rgba(255, 255, 255, 0.4);
        transition: background-color 0.3s;
    }

    .dot.active {
        background-color: var(--text-color);
    }

    .start-button {
        padding: var(--spacing-md) var(--spacing-xl);
        font-size: 1.2rem;
        font-weight: var(--font-weight-bold);
        color: var(--text-color);
        background: linear-gradient(45deg, #c83279, #8e2de2);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow-lg);
        transition: all var(--animation-time) ease;
    }

    .start-button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 15px rgba(200, 50, 121, 0.7);
    }
</style>

<!-- Karuzela jako tło -->
<div class="background-carousel">
    <div class="carousel">
        {#each slides as slide, i}
            <div
                class="slide"
                class:active={currentSlide === i}
                style="background-image: url({slide.imageUrl})"
            ></div>
        {/each}
    </div>
</div>

<!-- Treść na wierzchu -->
<div class="page-container">
    <header class="welcome-header">
        <h1>Witaj w Monitorze Aktywności</h1>
        <p>Twoje centrum dowodzenia produktywnością</p>
    </header>

    <!-- Dynamiczny tekst karuzeli na środku -->
    <div class="carousel-text-content">
        {#each slides as slide, i}
            <div class="text-slide" class:active={currentSlide === i}>
                <h2>{slide.title}</h2>
                <p>{slide.description}</p>
            </div>
        {/each}
    </div>

    <!-- Kontrolki i przycisk na dole -->
    <footer class="page-footer">
        <div class="main-controls">
            <button class="nav-button" on:click={prevSlide} aria-label="Poprzedni slajd"
                >&#10094;</button
            >
            <button class="start-button">Rozpocznij monitorowanie</button>
            <button class="nav-button" on:click={nextSlide} aria-label="Następny slajd"
                >&#10095;</button
            >
        </div>
        <div class="dots">
            {#each slides as _, i}
                <button
                    class="dot"
                    class:active={currentSlide === i}
                    on:click={() => goToSlide(i)}
                    aria-label="Przejdź do slajdu {i + 1}"
                ></button>
            {/each}
        </div>
    </footer>
</div>
