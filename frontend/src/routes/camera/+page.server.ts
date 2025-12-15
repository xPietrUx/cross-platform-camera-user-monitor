import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ cookies, fetch }) => {
    const token = cookies.get('access_token');

    if (!token) {
        throw redirect(302, '/login');
    }

    // Weryfikacja tokena w backend
    const response = await fetch('http://127.0.0.1:8000/users/me', {
        method: 'GET',
        headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
        },
    });

    if (!response.ok) {
        cookies.delete('access_token', { path: '/' });
        throw redirect(302, '/login');
    }

    const userData = await response.json();

    return {
        user: userData,
    };
};
