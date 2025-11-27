// See https://svelte.dev/docs/kit/types#app.d.ts
// for information about these interfaces

declare module 'svelte-frappe-charts' {
    import { SvelteComponent } from 'svelte';
    export class Chart extends SvelteComponent {}
}

declare global {
    namespace App {
        // interface Error {}
        // interface Locals {}
        // interface PageData {}
        // interface PageState {}
        // interface Platform {}
    }
}

export {};
