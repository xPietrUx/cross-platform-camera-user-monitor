const { app, BrowserWindow } = require('electron');
const path = require('path');

<<<<<<< HEAD
app.disableHardwareAcceleration();

// Sprawdzenie, czy aplikacja jest w trybie deweloperskim, czy produkcyjnym
=======
>>>>>>> a73ca12a048a5209ac7b7ca1c91a1a4c40240f31
const isDev = !app.isPackaged;

function createWindow() {
    const win = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            nodeIntegration: false,
        },
        autoHideMenuBar: !isDev,
    });

    if (isDev) {
        win.loadURL('http://localhost:5173');
        win.webContents.openDevTools();
    } else {
        win.loadFile(path.join(__dirname, '../build/index.html'));
    }

    win.webContents.on('did-fail-load', () => {
        console.error('Failed to load application');
    });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});
