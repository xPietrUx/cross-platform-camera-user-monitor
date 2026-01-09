const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

app.disableHardwareAcceleration();

const isDev = !app.isPackaged;
let backendProcess = null;

function startBackend() {
    if (isDev) {
        console.log('Tryb DEV: Uruchom backend ręcznie lub odkomentuj kod w main.cjs');
    } else {
        // WYKRYWANIE NAZWY PLIKU ZALEŻNIE OD PLATFORMY
        let executableName = 'api';
        if (process.platform === 'win32') {
            executableName = 'api.exe';
        }

        const backendPath = path.join(process.resourcesPath, executableName);

        console.log('Uruchamianie backendu z:', backendPath);

        backendProcess = spawn(backendPath, [], {
            cwd: process.resourcesPath, // Ustaw katalog roboczy, żeby baza SQLite tworzyła się obok exe
        });

        backendProcess.stdout.on('data', (data) => {
            console.log(`Backend stdout: ${data}`);
        });

        backendProcess.stderr.on('data', (data) => {
            console.error(`Backend stderr: ${data}`);
        });
    }
}

function createWindow() {
    const win = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            nodeIntegration: false,
        },
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

// Uruchom backend przy starcie Electrona
app.whenReady().then(() => {
    startBackend(); // <--- WYWOŁANIE FUNKCJI
    createWindow();
});

// Zabij backend przy zamykaniu aplikacji
app.on('will-quit', () => {
    if (backendProcess) {
        backendProcess.kill();
        backendProcess = null;
    }
});

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
