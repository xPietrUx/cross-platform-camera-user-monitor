import type { PageLoad } from './$types';

export const ssr = false;

export const load: PageLoad = () => {
    // W przyszłości w tym miejscu wywołasz fetch() do swojego API.

    const focusData = {
        labels: ['9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00'],
        datasets: [{ name: 'Skupienie', values: [65, 70, 85, 80, 60, 75, 90, 82] }],
    };

    const productivityData = {
        labels: ['Pon', 'Wt', 'Śr', 'Czw', 'Pt', 'Sob', 'Ndz'],
        datasets: [{ name: 'Godziny produktywne', values: [5, 6, 4.5, 7, 6.5, 2, 1] }],
    };

    const distractionsData = {
        labels: ['Telefon', 'Inne osoby', 'Hałas', 'Social media', 'Inne'],
        datasets: [{ name: 'Rozproszenia', values: [40, 15, 25, 30, 10] }],
    };

    // NOWY WYKRES: Podział czasu pracy
    const activityData = {
        labels: ['Pon', 'Wt', 'Śr', 'Czw', 'Pt'],
        datasets: [
            { name: 'Kodowanie', values: [30, 40, 25, 50, 45] },
            { name: 'Spotkania', values: [10, 20, 40, 10, 15] },
            { name: 'E-mail/Slack', values: [20, 10, 15, 10, 10] },
        ],
    };

    return {
        focusData,
        productivityData,
        distractionsData,
        activityData, // Zwracamy nowe dane
    };
};
