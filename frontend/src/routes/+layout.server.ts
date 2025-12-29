import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({ cookies, fetch }) => {
    const token = cookies.get('access_token');

    let user = null;

    if (token) {
        try {
            const response = await fetch('http://127.0.0.1:8000/users/me', {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            if (response.ok) {
                user = await response.json();
            } else {
                console.warn('Token nieważny');
            }
        } catch (error) {
            console.error('Błąd połączenia z backendem w layout:', error);
        }
    }

    return {
        user,
    };
};
