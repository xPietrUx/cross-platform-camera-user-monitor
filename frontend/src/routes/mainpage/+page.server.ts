import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ cookies, fetch }) => {
    const token = cookies.get('access_token');

    if (!token) {
        throw redirect(302, '/login');
    }

    // Weryfikacja tokena
    const response = await fetch('http://127.0.0.1:8000/users/me', {
        headers: { Authorization: `Bearer ${token}` },
    });

    if (!response.ok) {
        cookies.delete('access_token', { path: '/' });
        throw redirect(302, '/login');
    }

    return {
        user: await response.json(),
    };
};
