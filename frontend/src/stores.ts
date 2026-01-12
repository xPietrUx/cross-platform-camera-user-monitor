import { writable } from 'svelte/store';

export const isCameraPageActive = writable(false);
export const accessToken = writable<string | null>(null);

// Store do zarządzania stanem kamery
export const cameraActive = writable<boolean>(false);
export const cameraStream = writable<MediaStream | null>(null);

// Funkcja do zatrzymania kamery
export function stopCamera() {
    console.log('🛑 stopCamera() wywołana');

    // Dla MediaStream (jeśli kiedykolwiek będzie użyty)
    cameraStream.update((stream) => {
        if (stream) {
            stream.getTracks().forEach((track) => {
                console.log('Zatrzymywanie track:', track.kind);
                track.stop();
            });
        }
        return null;
    });
    cameraActive.set(false);

    // Wymuś zatrzymanie wszystkich elementów <img> ze strumieniem
    const images = document.querySelectorAll('img[alt="Strumień wideo z kamery"]');
    console.log(`🔍 Znaleziono ${images.length} elementów <img>`);
    images.forEach((img: HTMLImageElement) => {
        console.log('🗑️ Czyszczenie img.src:', img.src);
        img.src = '';
        img.srcset = '';
        // Usuń całkowicie atrybut src
        img.removeAttribute('src');
    });

    // Wyczyść token - to zatrzyma strumień MJPEG z backendu
    console.log('🔑 Czyszczenie accessToken');
    accessToken.set(null);

    console.log('✅ Kamera zatrzymana - token wyczyszczony, strumień przerwany');
}
