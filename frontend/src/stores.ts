import { writable } from 'svelte/store';

export const isCameraPageActive = writable(false);
export const accessToken = writable<string | null>(null);
