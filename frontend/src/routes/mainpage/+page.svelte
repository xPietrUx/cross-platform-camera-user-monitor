<script lang="ts">
    import { onMount, onDestroy, tick } from 'svelte';
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

    // Instancje wykresów
    let focusChartInstance: any = null;
    let prodChartInstance: any = null;
    let activityChartInstance: any = null;

    // Zmienna na klasę biblioteki (ładowana dynamicznie)
    let ChartLibrary: any = null;

    let error: string | null = null;
    let loading = true;
    let refreshInterval: any;

    async function authedJson<T>(url: string, token: string): Promise<T> {
        const res = await fetch(url, { headers: { Authorization: `Bearer ${token}` } });
        if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
        return res.json() as Promise<T>;
    }

    function updateCharts() {
        if (!ChartLibrary) {
            console.warn('⚠️ Biblioteka wykresów nie jest jeszcze załadowana');
            return;
        }

        // Sprawdź czy elementy DOM są gotowe
        if (!focusChartRef || !prodChartRef || !activityChartRef) {
            console.warn('⚠️ Elementy DOM wykresów nie są jeszcze gotowe');
            return;
        }

        const commonHeight = 240;

        // --- Wykres 1: Skupienie ---
        if (focusChartInstance) {
            if (focusData) {
                focusChartInstance.update(focusData);
            }
        } else if (focusData) {
            focusChartInstance = new ChartLibrary(focusChartRef, {
                data: focusData,
                type: 'bar',
                colors: ['#8e2de2'],
                height: commonHeight,
                axisOptions: { xAxisMode: 'tick' },
            });
        }

        // --- Wykres 2: Produktywność ---
        if (prodChartInstance) {
            if (productivityData) {
                prodChartInstance.update(productivityData);
            }
        } else if (productivityData) {
            prodChartInstance = new ChartLibrary(prodChartRef, {
                data: productivityData,
                type: 'line',
                colors: ['#c31432'],
                height: commonHeight,
            });
        }

        // --- Wykres 3: Aktywność ---
        if (activityChartInstance) {
            if (activityData) {
                activityChartInstance.update(activityData);
            }
        } else if (activityData) {
            activityChartInstance = new ChartLibrary(activityChartRef, {
                data: activityData,
                type: 'percentage',
                height: commonHeight,
                colors: ['#28a745', '#ffc107', '#17a2b8'],
            });
        }
    }

    async function refreshData() {
        const token = $accessToken ?? getCookie('access_token');
        if (!token) return;

        try {
            const startTime = performance.now();

            const [f, p, a] = await Promise.all([
                authedJson<ChartData>('http://127.0.0.1:8000/video/history', token),
                authedJson<ChartData>('http://127.0.0.1:8000/video/stats/daily', token),
                authedJson<ChartData>('http://127.0.0.1:8000/video/stats/activity', token),
            ]);

            const endTime = performance.now();

            focusData = f;
            productivityData = p;
            activityData = a;

            // WAŻNE: Poczekaj na zakończenie renderowania DOM
            await tick();

            // Spróbuj zaktualizować lub stworzyć wykresy
            updateCharts();
        } catch (e) {
            console.error('❌ Błąd odświeżania danych:', e);
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
            // 1. Najpierw ładujemy bibliotekę wykresów
            const mod = await import('frappe-charts/dist/frappe-charts.min.esm');
            ChartLibrary = mod.Chart;

            // 2. Ukryj loader (aby wyrenderować kontenery wykresów)
            loading = false;

            // 3. Poczekaj na renderowanie DOM
            await tick();

            // 5. NATYCHMIAST pobierz dane (to wywoła updateCharts wewnątrz)
            await refreshData();

            // 6. Ustaw interwał odświeżania
            refreshInterval = setInterval(refreshData, 30000); // 30 sekund
        } catch (e) {
            error = 'Nie udało się pobrać danych z API. Sprawdź czy backend działa.';
            loading = false;
        }
    });

    onDestroy(() => {
        if (refreshInterval) {
            clearInterval(refreshInterval);
        }
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
                <!-- Upewnij się, że divy mają określony minimalny rozmiar -->
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
