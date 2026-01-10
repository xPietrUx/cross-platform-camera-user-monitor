const { app, BrowserWindow, protocol } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs');
const { pathToFileURL } = require('url');

protocol.registerSchemesAsPrivileged([
    {
        scheme: 'app',
        privileges: {
            standard: true,
            secure: true,
            supportFetchAPI: true,
            corsEnabled: true,
        },
    },
]);

let backendProcess = null;
let mainWindow = null;

const gotTheLock = app.requestSingleInstanceLock();

if (!gotTheLock) {
    console.log('Aplikacja już działa, zamykam duplikat...');
    app.quit();
} else {
    app.on('second-instance', () => {
        if (mainWindow) {
            if (mainWindow.isMinimized()) mainWindow.restore();
            mainWindow.focus();
        }
    });

    function startBackend() {
        if (backendProcess) {
            console.log('Backend już działa, pomijam uruchomienie...');
            return;
        }

        const resourcesPath = process.resourcesPath;
        console.log('process.resourcesPath =', resourcesPath);

        const backendPath = path.join(resourcesPath, 'api.exe');
        console.log('Backend path =', backendPath);

        console.log('Backend exists =', fs.existsSync(backendPath));

        if (!fs.existsSync(backendPath)) {
            console.error('Nie znaleziono api.exe!');
            return;
        }

        backendProcess = spawn(backendPath, [], {
            cwd: resourcesPath,
            stdio: ['ignore', 'pipe', 'pipe'],
            detached: false,
            windowsHide: true,
        });

        backendProcess.stdout?.on('data', (data) => {
            console.log('Backend stdout:', data.toString().trim());
        });
        backendProcess.stderr?.on('data', (data) => {
            console.log('Backend stderr:', data.toString().trim());
        });
        backendProcess.on('exit', (code, signal) => {
            console.log('Backend exited:', { code, signal });
            backendProcess = null;
        });
    }

    function stopBackend() {
        if (backendProcess && !backendProcess.killed) {
            console.log('Zamykam backend...');

            if (process.platform === 'win32') {
                // Windows: użyj taskkill
                const { exec } = require('child_process');
                exec(`taskkill /pid ${backendProcess.pid} /T /F`, (error) => {
                    if (error) {
                        console.error('Błąd przy zamykaniu backendu:', error);
                    } else {
                        console.log('Backend zamknięty (taskkill)');
                    }
                    backendProcess = null;
                });
            } else {
                // Linux/Mac: SIGTERM
                backendProcess.kill('SIGTERM');
                setTimeout(() => {
                    if (backendProcess && !backendProcess.killed) {
                        backendProcess.kill('SIGKILL');
                    }
                    backendProcess = null;
                }, 2000);
            }
        }
    }

    function registerAppProtocol() {
        // UWAGA: build jest w app.asar/build (u Ciebie działa z loadURL na app.asar)
        const buildRoot = path.join(app.getAppPath(), 'build');

        protocol.registerFileProtocol('app', (request, callback) => {
            try {
                const u = new URL(request.url);

                // pathname np. "/", "/mainpage", "/_app/immutable/....js"
                let relPath = decodeURIComponent(u.pathname || '/');

                // katalog/route -> fallback na index.html (SPA)
                if (relPath === '/' || relPath === '') relPath = '/index.html';

                let resolved = path.join(buildRoot, relPath);

                // harden: wyjście poza buildRoot
                if (!resolved.startsWith(buildRoot)) {
                    resolved = path.join(buildRoot, 'index.html');
                }

                // jeśli nie istnieje (np. /mainpage), albo to katalog -> index.html
                if (!fs.existsSync(resolved) || fs.statSync(resolved).isDirectory()) {
                    resolved = path.join(buildRoot, 'index.html');
                }

                callback({ path: resolved });
            } catch (e) {
                callback({ path: path.join(buildRoot, 'index.html') });
            }
        });
    }

    function createWindow() {
        if (mainWindow) {
            console.log('Okno już istnieje, pomijam tworzenie...');
            return;
        }

        mainWindow = new BrowserWindow({
            width: 1200,
            height: 800,
            webPreferences: {
                preload: path.join(__dirname, 'preload.cjs'),
                contextIsolation: true,
                nodeIntegration: false,
            },
        });

        mainWindow.webContents.session.setPermissionRequestHandler(
            (webContents, permission, callback) => {
                if (permission === 'media') return callback(true);
                callback(false);
            }
        );

        if (app.isPackaged) {
            // Ładuj root, żeby SvelteKit widział pathname = "/" (a nie "/index.html")
            const indexURL = 'app://-/';
            console.log('Ładuję index.html z:', indexURL);
            mainWindow.loadURL(indexURL);
        } else {
            mainWindow.loadURL('http://localhost:5173');
        }

        // (opcjonalnie) nie otwieraj devtools w produkcji
        mainWindow.webContents.openDevTools();

        mainWindow.on('closed', () => {
            console.log('Okno zamknięte');
            mainWindow = null;
        });
    }

    app.whenReady().then(() => {
        registerAppProtocol();
        startBackend();
        setTimeout(createWindow, 2000);
    });

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });

    app.on('window-all-closed', () => {
        console.log('Wszystkie okna zamknięte, zamykam backend...');
        stopBackend();

        if (process.platform !== 'darwin') {
            setTimeout(() => app.quit(), 1000);
        }
    });

    app.on('before-quit', (event) => {
        if (backendProcess && !backendProcess.killed) {
            console.log('before-quit: Zamykam backend...');
            event.preventDefault();

            stopBackend();

            setTimeout(() => {
                app.exit(0);
            }, 2000);
        }
    });
}
