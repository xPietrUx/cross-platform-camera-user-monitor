import { writable } from 'svelte/store';

export const isCameraPageActive = writable(false);
export const accessToken = writable<string | null>(null);

// Store do zarządzania stanem kamery
export const cameraActive = writable<boolean>(false);
export const cameraStream = writable<MediaStream | null>(null);

// Funkcja do zatrzymania kamery
export function stopCamera() {
    cameraStream.update((stream) => {
        if (stream) {
            stream.getTracks().forEach((track) => {
                track.stop();
            });
        }
        return null;
    });
    cameraActive.set(false);

    const images = document.querySelectorAll('img[alt="Strumień wideo z kamery"]');
    images.forEach((img: HTMLImageElement) => {
        img.src = '';
        img.srcset = '';
        img.removeAttribute('src');
    });
    accessToken.set(null);
}
