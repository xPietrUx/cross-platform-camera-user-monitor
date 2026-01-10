<script lang="ts">
    import { onMount, onDestroy } from 'svelte';
    import { goto } from '$app/navigation';
    import { isCameraPageActive } from '../../stores';

    onMount(() => {
        isCameraPageActive.set(true);
    });

    onDestroy(() => {
        isCameraPageActive.set(false);
    });

    function close() {
        isCameraPageActive.set(false);
        goto('/mainpage');
    }
</script>

<style>
    .camera-page {
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 60vh;
        color: white;
        text-align: center;
    }
    .btn {
        margin-top: 16px;
        padding: 10px 14px;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.25);
        background: rgba(0, 0, 0, 0.25);
        color: white;
        cursor: pointer;
    }
</style>

<div class="camera-page">
    <div>
        <h2>Podgląd kamery</h2>
        <p>Strumień jest renderowany globalnie (bez drugiego połączenia).</p>
        <button class="btn" on:click={close}>Zamknij</button>
    </div>
</div>
