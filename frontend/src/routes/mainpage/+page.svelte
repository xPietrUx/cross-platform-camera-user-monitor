<script lang="ts">
    import { onMount } from 'svelte';
    import type { PageData } from './$types';

    const { data } = $props<{ data: PageData }>();
    const { focusData, productivityData, activityData } = data;

    let focusChartRef: HTMLElement;
    let prodChartRef: HTMLElement;
    let activityChartRef: HTMLElement;

    onMount(async () => {
        const module = await import('frappe-charts/dist/frappe-charts.min.esm');
        const Chart = module.Chart;

        const commonHeight = 240;

        // Wykres 1: Skupienie
        if (focusChartRef) {
            new Chart(focusChartRef, {
                data: focusData,
                type: 'bar',
                colors: ['#8e2de2'],
                height: commonHeight,
                axisOptions: { xAxisMode: 'tick' },
            });
        }

        // Wykres 2: Produktywność
        if (prodChartRef) {
            new Chart(prodChartRef, {
                data: productivityData,
                type: 'line',
                colors: ['#c31432'],
                height: commonHeight,
            });
        }

        // Wykres 3: Podział aktywności
        if (activityChartRef) {
            new Chart(activityChartRef, {
                data: activityData,
                type: 'percentage',
                height: commonHeight,
                colors: ['#28a745', '#ffc107', '#17a2b8'],
            });
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
</div>
