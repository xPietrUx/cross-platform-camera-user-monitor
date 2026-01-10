// See https://svelte.dev/docs/kit/types#app.d.ts
// for information about these interfaces

declare module 'frappe-charts/dist/frappe-charts.min.esm' {
    export class Chart {
        constructor(element: HTMLElement, options: any);
    }
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
