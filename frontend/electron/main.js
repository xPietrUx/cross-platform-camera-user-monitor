const { app, BrowserWindow } = require('electron');
const path = require('path');

// Sprawdzenie, czy aplikacja jest w trybie deweloperskim, czy produkcyjnym
const isDev = !app.isPackaged;

function createWindow() {
    const win = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            // preload.js jest mostem między backendem Electrona a frontendem Svelte
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            nodeIntegration: false,
        },
    });

    // W trybie deweloperskim ładujemy adres serwera Vite
    if (isDev) {
        win.loadURL('http://localhost:5173');
        // Otwórz narzędzia deweloperskie
        win.webContents.openDevTools();
    } else {
        // W trybie produkcyjnym ładujemy zbudowany plik HTML
        win.loadFile(path.join(__dirname, '../build/index.html'));
    }
}

app.whenReady().then(createWindow);

// Zamknij aplikację, gdy wszystkie okna są zamknięte (dla Windows i Linux)
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

// Otwórz nowe okno, jeśli żadne nie jest otwarte (dla macOS)
app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});
