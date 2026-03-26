// Mode detection
const isLive = location.protocol.startsWith('http');
document.body.dataset.mode = isLive ? 'live' : 'static';
document.getElementById('mode-badge').textContent = isLive ? 'Live' : 'Static';

// Tab switching
document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(tc => tc.classList.remove('active'));
        tab.classList.add('active');
        document.getElementById('tab-' + tab.dataset.tab).classList.add('active');
    });
});

// Data loading
let galleryData = { layouts: [], themes: [] };

async function loadData() {
    if (isLive) {
        try {
            const [layoutsRes, themesRes] = await Promise.all([
                fetch('/api/layouts'),
                fetch('/api/themes'),
            ]);
            const layoutsData = await layoutsRes.json();
            const themesData = await themesRes.json();
            galleryData.layouts = layoutsData.layouts || layoutsData;
            galleryData.themes = themesData.themes || themesData;
        } catch (e) {
            console.warn('API fetch failed, falling back to embedded data', e);
            loadEmbeddedData();
        }
    } else {
        loadEmbeddedData();
    }
    renderLayouts();
    renderThemes();
    if (isLive) initGenerateForm();
}

function loadEmbeddedData() {
    const el = document.getElementById('gallery-data');
    try {
        galleryData = JSON.parse(el.textContent);
    } catch (e) {
        console.warn('No embedded gallery data');
    }
}

// Layout cards
function renderLayouts() {
    const grid = document.getElementById('layouts-grid');
    grid.innerHTML = '';
    (galleryData.layouts || []).forEach(layout => {
        const card = document.createElement('div');
        card.className = 'card';

        const imgSrc = `images/${layout.name}.png`;
        const argsHtml = (layout.required_args || [])
            .map(a => `<span>--${a.replace(/_/g, '-')}</span>`)
            .join('');

        const cliCmd = layout.example_command || `modern-graphics create --layout ${layout.name} --output ${layout.name}.html`;
        const mcpCmd = JSON.stringify({
            tool: 'generate_graphic',
            arguments: { layout: layout.name, args: {}, format: 'png' }
        }, null, 2);

        card.innerHTML = `
            <img class="card-image" src="${imgSrc}" alt="${layout.name}" onerror="this.style.display='none'" />
            <div class="card-body">
                <div class="card-title">${layout.name}</div>
                <div class="card-desc">${layout.description || ''}</div>
                <div class="card-args">${argsHtml || '<span>no required args</span>'}</div>
                <div class="command-block">
                    <label>CLI</label>
                    <code id="cli-${layout.name}">${escapeHtml(cliCmd)}</code>
                    <button class="copy-btn" onclick="copyText('cli-${layout.name}', this)">Copy</button>
                </div>
            </div>
        `;
        grid.appendChild(card);
    });
}

// Theme cards
function renderThemes() {
    const grid = document.getElementById('themes-grid');
    grid.innerHTML = '';
    (galleryData.themes || []).forEach(theme => {
        const card = document.createElement('div');
        card.className = 'card';

        const imgSrc = `theme-images/theme-${theme.name}.png`;
        const aliases = (theme.aliases || []).length ? ` (also: ${theme.aliases.join(', ')})` : '';

        card.innerHTML = `
            <img class="card-image" src="${imgSrc}" alt="${theme.name} theme" onerror="this.style.display='none'" />
            <div class="card-body">
                <div class="theme-swatches">
                    <div class="swatch" style="background:${theme.primary}" title="Primary: ${theme.primary}"></div>
                    <div class="swatch" style="background:${theme.accent}" title="Accent: ${theme.accent}"></div>
                </div>
                <div class="card-title">${theme.name}${aliases}</div>
                <div class="card-desc">${theme.description || ''}</div>
                <div class="command-block">
                    <label>Use with</label>
                    <code id="theme-${theme.name}">--theme ${theme.name}</code>
                    <button class="copy-btn" onclick="copyText('theme-${theme.name}', this)">Copy</button>
                </div>
            </div>
        `;
        grid.appendChild(card);
    });
}

// Generate form (live mode only)
function initGenerateForm() {
    const layoutSelect = document.getElementById('gen-layout');
    const themeSelect = document.getElementById('gen-theme');

    galleryData.layouts.forEach(l => {
        const opt = document.createElement('option');
        opt.value = l.name;
        opt.textContent = `${l.name} -- ${l.description || ''}`;
        layoutSelect.appendChild(opt);
    });

    themeSelect.innerHTML = '<option value="">Default (corporate)</option>';
    galleryData.themes.forEach(t => {
        const opt = document.createElement('option');
        opt.value = t.name;
        opt.textContent = t.name;
        themeSelect.appendChild(opt);
    });

    layoutSelect.addEventListener('change', () => buildArgFields(layoutSelect.value));
    buildArgFields(layoutSelect.value);

    // Format toggles
    document.querySelectorAll('.toggle').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.toggle').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        });
    });

    // Submit
    document.getElementById('gen-submit').addEventListener('click', handleGenerate);
}

function buildArgFields(layoutName) {
    const container = document.getElementById('gen-args');
    const layout = galleryData.layouts.find(l => l.name === layoutName);
    if (!layout) return;
    container.innerHTML = '';
    (layout.required_args || []).forEach(arg => {
        const div = document.createElement('div');
        div.className = 'form-group';
        const label = arg.replace(/_/g, ' ');
        div.innerHTML = `
            <label for="arg-${arg}">${label}</label>
            <input type="text" id="arg-${arg}" data-arg="${arg}" placeholder="${arg}" />
        `;
        container.appendChild(div);
    });
}

async function handleGenerate() {
    const layout = document.getElementById('gen-layout').value;
    const theme = document.getElementById('gen-theme').value;
    const format = document.querySelector('.toggle.active').dataset.format;

    const args = {};
    document.querySelectorAll('#gen-args input').forEach(input => {
        if (input.value.trim()) {
            args[input.dataset.arg] = input.value.trim();
        }
    });

    const btn = document.getElementById('gen-submit');
    const loading = document.getElementById('gen-loading');
    const result = document.getElementById('gen-result');

    btn.disabled = true;
    loading.style.display = 'block';
    result.style.display = 'none';

    try {
        const res = await fetch('/api/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ layout, args, theme: theme || undefined, format }),
        });
        const data = await res.json();

        if (data.error) {
            alert('Error: ' + data.error);
            return;
        }

        const img = document.getElementById('gen-result-img');
        if (data.file_url) {
            img.src = data.file_url;
        }

        // Build CLI command
        let cli = `modern-graphics create --layout ${layout}`;
        for (const [k, v] of Object.entries(args)) {
            cli += ` --${k.replace(/_/g, '-')} "${v}"`;
        }
        if (theme) cli += ` --theme ${theme}`;
        if (format === 'png') cli += ' --png';
        cli += ` --output ./output/${layout}.${format}`;
        document.getElementById('gen-cli-cmd').textContent = cli;

        // Build MCP command
        const mcpObj = {
            tool: 'generate_graphic',
            arguments: { layout, args, format, ...(theme ? { theme } : {}) }
        };
        document.getElementById('gen-mcp-cmd').textContent = JSON.stringify(mcpObj, null, 2);

        result.style.display = 'block';
    } catch (e) {
        alert('Generation failed: ' + e.message);
    } finally {
        btn.disabled = false;
        loading.style.display = 'none';
    }
}

// Utilities
function copyText(elementId, btn) {
    const text = document.getElementById(elementId).textContent;
    navigator.clipboard.writeText(text).then(() => {
        btn.textContent = 'Copied';
        btn.classList.add('copied');
        setTimeout(() => { btn.textContent = 'Copy'; btn.classList.remove('copied'); }, 1500);
    });
}

function escapeHtml(str) {
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

// Init
loadData();
