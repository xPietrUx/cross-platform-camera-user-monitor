import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ cookies, fetch }) => {
    const token = cookies.get('access_token');

    if (!token) {
        throw redirect(302, '/login');
    }

    const [userRes, dailyStatsRes, historyRes, activityRes] = await Promise.all([
        fetch('http://127.0.0.1:8000/users/me', {
            headers: { Authorization: `Bearer ${token}` },
        }),
        fetch('http://127.0.0.1:8000/video/stats/daily', {
            headers: { Authorization: `Bearer ${token}` },
        }),
        fetch('http://127.0.0.1:8000/video/history', {
            headers: { Authorization: `Bearer ${token}` },
        }),
        fetch('http://127.0.0.1:8000/video/stats/activity', {
            headers: { Authorization: `Bearer ${token}` },
        }),
    ]);

    if (!userRes.ok) {
        cookies.delete('access_token', { path: '/' });
        throw redirect(302, '/login');
    }

    const user = await userRes.json();

    const productivityData = dailyStatsRes.ok
        ? await dailyStatsRes.json()
        : { labels: [], datasets: [] };

    const focusData = historyRes.ok ? await historyRes.json() : { labels: [], datasets: [] };

    const activityData = activityRes.ok ? await activityRes.json() : { labels: [], datasets: [] };

    return {
        user,
        productivityData,
        focusData,
        activityData,
    };
};
