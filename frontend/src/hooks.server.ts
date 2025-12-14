import { redirect, type Handle } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
    const token = event.cookies.get('auth_token');
    const protectedRoutes = ['/mainpage', '/camera', '/users'];
    const isProtectedRoute = protectedRoutes.some((route) => event.url.pathname.startsWith(route));

    // --- DEBUG LOGI (zobaczysz je w terminalu frontendu) ---
    if (isProtectedRoute) {
        console.log(`[HOOK] Próba wejścia na: ${event.url.pathname}`);
        console.log(`[HOOK] Czy jest token?: ${token ? 'TAK' : 'NIE'}`);
    }
    // -------------------------------------------------------

    if (isProtectedRoute && !token) {
        console.log('[HOOK] Brak tokenu -> Przekierowanie do /login');
        throw redirect(303, '/login');
    }

    return await resolve(event);
};
