<div class="cover">
<h1>Przykład wyglądu naszego projektu</h1>
<div class="card">
    <p>oto przykład karty</p>
</div>
<p>Wszelkie zmienne są w ../styles/base/_variables</p>
<p>Powodzenia :)</p>
</div>

<style>
    /* style możemy nazywać w różnych plikach tak 
    samo a dać inne wyglądy do póki piszem je w 
    sekcji style w danym pliku .svlete, 
    a nie np w example.css */
    .cover {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }

    .card{
        border: var(--border);
        border-radius: var(--border-radius-sm);
        padding: var(--spacing-md);
    }

</style>

