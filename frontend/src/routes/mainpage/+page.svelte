<script lang="ts">
    import { onMount, onDestroy } from 'svelte';
    import { goto } from '$app/navigation';
    import { accessToken } from '../../stores';
    import { getCookie } from '$lib/utils';

    type ChartData = {
        labels: string[];
        datasets: Array<{ name: string; values: number[] }>;
    };

    let focusData: ChartData | null = null;
    let productivityData: ChartData | null = null;
    let activityData: ChartData | null = null;

    let focusChartRef: HTMLElement;
    let prodChartRef: HTMLElement;
    let activityChartRef: HTMLElement;

    // Instancje wykresów (aby móc je aktualizować)
    let focusChartInstance: any = null;
    let prodChartInstance: any = null;
    let activityChartInstance: any = null;

    let error: string | null = null;
    let loading = true;
    let refreshInterval: any;

    async function authedJson<T>(url: string, token: string): Promise<T> {
        const res = await fetch(url, { headers: { Authorization: `Bearer ${token}` } });
        if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
        return res.json() as Promise<T>;
    }

    // Funkcja do pobierania i aktualizacji danych
    async function refreshData() {
        const token = $accessToken ?? getCookie('access_token');
        if (!token) return;

        try {
            const [f, p, a] = await Promise.all([
                authedJson<ChartData>('http://127.0.0.1:8000/video/history', token),
                authedJson<ChartData>('http://127.0.0.1:8000/video/stats/daily', token),
                authedJson<ChartData>('http://127.0.0.1:8000/video/stats/activity', token),
            ]);

            focusData = f;
            productivityData = p;
            activityData = a;

            // Jeśli wykresy już istnieją -> aktualizuj dane
            // Jeśli nie -> zostaną utworzone w onMount (lub poniżej)
            if (focusChartInstance && focusData) focusChartInstance.update(focusData);
            if (prodChartInstance && productivityData) prodChartInstance.update(productivityData);
            if (activityChartInstance && activityData) activityChartInstance.update(activityData);
        } catch (e) {
            console.error('Błąd odświeżania danych:', e);
            // Nie ustawiamy globalnego błędu tutaj, aby nie przerywać widoku w razie chwilowego problemu z siecią
        }
    }

    onMount(async () => {
        loading = true;
        error = null;

        const token = $accessToken ?? getCookie('access_token') ?? null;
        accessToken.set(token);

        if (!token) {
            await goto('/login');
            return;
        }

        try {
            // Pierwsze pobranie danych
            await refreshData();

            const mod = await import('frappe-charts/dist/frappe-charts.min.esm');
            const Chart = mod.Chart;
            const commonHeight = 240;

            // Inicjalizacja wykresów
            if (focusChartRef && focusData?.labels?.length) {
                focusChartInstance = new Chart(focusChartRef, {
                    data: focusData,
                    type: 'bar',
                    colors: ['#8e2de2'],
                    height: commonHeight,
                    axisOptions: { xAxisMode: 'tick' },
                });
            }

            if (prodChartRef && productivityData?.labels?.length) {
                prodChartInstance = new Chart(prodChartRef, {
                    data: productivityData,
                    type: 'line',
                    colors: ['#c31432'],
                    height: commonHeight,
                });
            }

            if (activityChartRef && activityData?.labels?.length) {
                activityChartInstance = new Chart(activityChartRef, {
                    data: activityData,
                    type: 'percentage',
                    height: commonHeight,
                    colors: ['#28a745', '#ffc107', '#17a2b8'],
                });
            }

            // Ustaw interwał odświeżania co 1 minutę (60000ms)
            // Dzięki temu user zobaczy nowe dane maksymalnie minutę po ich wygenerowaniu
            refreshInterval = setInterval(refreshData, 60000);
        } catch (e) {
            console.error(e);
            error = 'Nie udało się pobrać danych z API. Sprawdź czy backend działa.';
        } finally {
            loading = false;
        }
    });

    onDestroy(() => {
        // Wyczyść interwał przy wyjściu ze strony, aby nie zwolnilo przeglądarki
        if (refreshInterval) clearInterval(refreshInterval);
    });
</script>

<style>
    .dashboard {
        display: flex;
        flex-direction: column;
        gap: var(--spacing-md);
        height: 100%;
    }

    .dashboard-header {
        text-align: center;
        margin-bottom: var(--spacing-xs);
    }

    .dashboard-header h1 {
        font-size: 2rem;
        font-weight: var(--font-weight-bold);
        color: #fff;
        margin-bottom: 0;
    }

    .dashboard-header p {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.8);
        margin-top: var(--spacing-xs);
    }

    .charts-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: var(--spacing-md);
        padding-bottom: var(--spacing-md);
    }

    .chart-container {
        background-color: rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        padding: var(--spacing-md);
        border-radius: var(--border-radius-sm);
        box-shadow: var(--box-shadow);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #fff;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .chart-container h2 {
        font-size: 1.1rem;
        font-weight: var(--font-weight-bold);
        margin-bottom: var(--spacing-sm);
        text-align: center;
        color: rgba(255, 255, 255, 0.9);
    }

    /* --- STYLE DLA FRAPPE CHARTS (OVERRIDE) --- */

    :global(.chart-container .frappe-chart text) {
        fill: #ffffff !important;
    }

    :global(.chart-container .frappe-chart .legend-label),
    :global(.chart-container .frappe-chart .chart-legend text) {
        fill: #ffffff !important;
        font-family: inherit !important;
        font-size: 10px !important;
    }

    :global(.chart-container .frappe-chart .axis-line),
    :global(.chart-container .frappe-chart .grid-line),
    :global(.chart-container .frappe-chart line) {
        stroke: rgba(255, 255, 255, 0.2) !important;
    }

    :global(.chart-container .frappe-chart .graph-svg-tip) {
        background-color: rgba(0, 0, 0, 0.9) !important;
        color: #fff !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
        z-index: 100;
    }

    :global(.chart-container .frappe-chart .graph-svg-tip::before) {
        border-top-color: rgba(0, 0, 0, 0.9) !important;
    }
</style>

<div class="dashboard">
    <header class="dashboard-header">
        <h1>Panel Główny</h1>
        <p>Oto podsumowanie Twojej aktywności i produktywności.</p>
    </header>

    {#if loading}
        <p style="text-align:center;">Ładowanie…</p>
    {:else if error}
        <p style="text-align:center; color: var(--error-color);">{error}</p>
    {:else}
        <div class="charts-grid">
            <div class="chart-container">
                <h2>Poziom skupienia (%)</h2>
                <div bind:this={focusChartRef}></div>
            </div>

            <div class="chart-container">
                <h2>Trendy produktywności</h2>
                <div bind:this={prodChartRef}></div>
            </div>

            <div class="chart-container">
                <h2>Podział aktywności</h2>
                <div bind:this={activityChartRef}></div>
            </div>
        </div>
    {/if}
</div>
