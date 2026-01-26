/**
 * Animaid Tutorial - Interactive property editor
 */

document.addEventListener('DOMContentLoaded', () => {
    // Tab switching
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabId = btn.dataset.tab;

            // Update button states
            tabButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            // Update content visibility
            tabContents.forEach(content => {
                content.classList.remove('active');
                if (content.id === `tab-${tabId}`) {
                    content.classList.add('active');
                }
            });
        });
    });

    // HTMLString controls
    setupStringControls();

    // HTMLInt controls
    setupIntControls();

    // HTMLFloat controls
    setupFloatControls();

    // HTMLTuple controls
    setupTupleControls();

    // HTMLSet controls
    setupSetControls();

    // HTMLList controls
    setupListControls();

    // HTMLDict controls
    setupDictControls();

    // Dict of Lists controls
    setupDictOfListsControls();

    // List of Dicts controls
    setupListOfDictsControls();

    // Setup preset buttons
    setupPresetButtons();

    // Initial render
    updateStringPreview();
    updateIntPreview();
    updateFloatPreview();
    updateTuplePreview();
    updateSetPreview();
    updateListPreview();
    updateDictPreview();
    updateDictOfListsPreview();
    updateListOfDictsPreview();
});

// -------------------------------------------------------------------------
// Preset Button Handling
// -------------------------------------------------------------------------

function setupPresetButtons() {
    document.querySelectorAll('.preset-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const preset = btn.dataset.preset;
            applyPreset(preset);
        });
    });
}

function applyPreset(preset) {
    // String presets
    if (preset === 'string-highlight') {
        resetStringControls();
        document.getElementById('string-background').value = '#fff59d';
        document.getElementById('string-padding').value = '2px 4px';
        updateStringPreview();
    } else if (preset === 'string-code') {
        resetStringControls();
        document.getElementById('string-monospace').checked = true;
        document.getElementById('string-background').value = '#f5f5f5';
        document.getElementById('string-padding').value = '2px 6px';
        document.getElementById('string-border-radius').value = '4px';
        document.getElementById('string-font-size').value = '0.9em';
        updateStringPreview();
    } else if (preset === 'string-badge') {
        resetStringControls();
        document.getElementById('string-background').value = '#e0e0e0';
        document.getElementById('string-padding').value = '4px 10px';
        document.getElementById('string-border-radius').value = '12px';
        document.getElementById('string-font-size').value = '0.85em';
        updateStringPreview();
    } else if (preset === 'string-success') {
        resetStringControls();
        document.getElementById('string-color').value = '#2e7d32';
        document.getElementById('string-background').value = '#e8f5e9';
        document.getElementById('string-padding').value = '2px 6px';
        document.getElementById('string-border-radius').value = '4px';
        updateStringPreview();
    } else if (preset === 'string-warning') {
        resetStringControls();
        document.getElementById('string-color').value = '#e65100';
        document.getElementById('string-background').value = '#fff3e0';
        document.getElementById('string-padding').value = '2px 6px';
        document.getElementById('string-border-radius').value = '4px';
        updateStringPreview();
    } else if (preset === 'string-error') {
        resetStringControls();
        document.getElementById('string-color').value = '#c62828';
        document.getElementById('string-background').value = '#ffebee';
        document.getElementById('string-padding').value = '2px 6px';
        document.getElementById('string-border-radius').value = '4px';
        updateStringPreview();
    } else if (preset === 'string-reset') {
        resetStringControls();
        updateStringPreview();
    }

    // List presets
    else if (preset === 'list-pills') {
        resetListControls();
        document.getElementById('list-direction').value = 'horizontal';
        document.getElementById('list-type').value = 'plain';
        document.getElementById('list-gap').value = '8px';
        document.getElementById('list-item-padding').value = '6px 14px';
        document.getElementById('list-item-border-radius').value = '20px';
        document.getElementById('list-item-background').value = '#e0e0e0';
        updateListPreview();
    } else if (preset === 'list-cards') {
        resetListControls();
        document.getElementById('list-direction').value = 'horizontal';
        document.getElementById('list-type').value = 'plain';
        document.getElementById('list-gap').value = '16px';
        document.getElementById('list-item-padding').value = '16px';
        document.getElementById('list-item-border').value = '1px solid #e0e0e0';
        document.getElementById('list-item-border-radius').value = '8px';
        document.getElementById('list-item-background').value = 'white';
        updateListPreview();
    } else if (preset === 'list-tags') {
        resetListControls();
        document.getElementById('list-direction').value = 'horizontal';
        document.getElementById('list-type').value = 'plain';
        document.getElementById('list-gap').value = '8px';
        document.getElementById('list-item-padding').value = '4px 10px';
        document.getElementById('list-item-border-radius').value = '4px';
        document.getElementById('list-item-background').value = '#f5f5f5';
        updateListPreview();
    } else if (preset === 'list-menu') {
        resetListControls();
        document.getElementById('list-direction').value = 'vertical';
        document.getElementById('list-type').value = 'plain';
        document.getElementById('list-item-padding').value = '12px 16px';
        document.getElementById('list-separator').value = '1px solid #e0e0e0';
        updateListPreview();
    } else if (preset === 'list-numbered') {
        resetListControls();
        document.getElementById('list-type').value = 'ordered';
        document.getElementById('list-padding').value = '0 0 0 24px';
        document.getElementById('list-item-padding').value = '4px 0';
        updateListPreview();
    } else if (preset === 'list-reset') {
        resetListControls();
        updateListPreview();
    }

    // Dict presets
    else if (preset === 'dict-card') {
        resetDictControls();
        document.getElementById('dict-format').value = 'divs';
        document.getElementById('dict-padding').value = '16px';
        document.getElementById('dict-border').value = '1px solid #e0e0e0';
        document.getElementById('dict-border-radius').value = '8px';
        document.getElementById('dict-background').value = 'white';
        document.getElementById('dict-gap').value = '8px';
        document.getElementById('dict-key-bold').checked = true;
        document.getElementById('dict-separator').value = ': ';
        updateDictPreview();
    } else if (preset === 'dict-simple') {
        resetDictControls();
        document.getElementById('dict-separator').value = ': ';
        document.getElementById('dict-key-bold').checked = true;
        document.getElementById('dict-gap').value = '4px';
        updateDictPreview();
    } else if (preset === 'dict-striped') {
        resetDictControls();
        document.getElementById('dict-format').value = 'table';
        document.getElementById('dict-border').value = '1px solid #e0e0e0';
        document.getElementById('dict-key-padding').value = '8px 12px';
        document.getElementById('dict-value-padding').value = '8px 12px';
        document.getElementById('dict-key-background').value = '#f5f5f5';
        document.getElementById('dict-key-bold').checked = true;
        updateDictPreview();
    } else if (preset === 'dict-labeled') {
        resetDictControls();
        document.getElementById('dict-format').value = 'divs';
        document.getElementById('dict-layout').value = 'vertical';
        document.getElementById('dict-gap').value = '16px';
        updateDictPreview();
    } else if (preset === 'dict-bordered') {
        resetDictControls();
        document.getElementById('dict-format').value = 'table';
        document.getElementById('dict-border').value = '1px solid #e0e0e0';
        document.getElementById('dict-key-padding').value = '8px';
        document.getElementById('dict-value-padding').value = '8px';
        updateDictPreview();
    } else if (preset === 'dict-reset') {
        resetDictControls();
        updateDictPreview();
    }

    // Int presets
    else if (preset === 'int-currency') {
        resetIntControls();
        document.getElementById('int-format').value = 'currency';
        document.getElementById('int-currency-symbol-group').style.display = 'block';
        document.getElementById('int-bold').checked = true;
        document.getElementById('int-color').value = '#2e7d32';
        updateIntPreview();
    } else if (preset === 'int-comma') {
        resetIntControls();
        document.getElementById('int-format').value = 'comma';
        document.getElementById('int-monospace').checked = true;
        updateIntPreview();
    } else if (preset === 'int-percent') {
        resetIntControls();
        document.getElementById('int-value').value = '85';
        document.getElementById('int-format').value = 'percent';
        document.getElementById('int-bold').checked = true;
        updateIntPreview();
    } else if (preset === 'int-ordinal') {
        resetIntControls();
        document.getElementById('int-value').value = '1';
        document.getElementById('int-format').value = 'ordinal';
        updateIntPreview();
    } else if (preset === 'int-badge') {
        resetIntControls();
        document.getElementById('int-format').value = 'comma';
        document.getElementById('int-background').value = '#e0e0e0';
        document.getElementById('int-padding').value = '4px 10px';
        document.getElementById('int-border-radius').value = '12px';
        updateIntPreview();
    } else if (preset === 'int-reset') {
        resetIntControls();
        updateIntPreview();
    }

    // Float presets
    else if (preset === 'float-currency') {
        resetFloatControls();
        document.getElementById('float-value').value = '1234.56';
        document.getElementById('float-format').value = 'currency';
        document.getElementById('float-currency-symbol-group').style.display = 'block';
        document.getElementById('float-decimals-group').style.display = 'block';
        document.getElementById('float-bold').checked = true;
        document.getElementById('float-color').value = '#2e7d32';
        updateFloatPreview();
    } else if (preset === 'float-percent') {
        resetFloatControls();
        document.getElementById('float-value').value = '0.856';
        document.getElementById('float-format').value = 'percent';
        document.getElementById('float-decimals-group').style.display = 'block';
        document.getElementById('float-bold').checked = true;
        updateFloatPreview();
    } else if (preset === 'float-decimal') {
        resetFloatControls();
        document.getElementById('float-format').value = 'decimal';
        document.getElementById('float-decimals-group').style.display = 'block';
        document.getElementById('float-monospace').checked = true;
        updateFloatPreview();
    } else if (preset === 'float-scientific') {
        resetFloatControls();
        document.getElementById('float-value').value = '1234567.89';
        document.getElementById('float-format').value = 'scientific';
        document.getElementById('float-precision-group').style.display = 'block';
        document.getElementById('float-monospace').checked = true;
        updateFloatPreview();
    } else if (preset === 'float-badge') {
        resetFloatControls();
        document.getElementById('float-format').value = 'decimal';
        document.getElementById('float-decimals-group').style.display = 'block';
        document.getElementById('float-background').value = '#e0e0e0';
        document.getElementById('float-padding').value = '4px 10px';
        document.getElementById('float-border-radius').value = '12px';
        updateFloatPreview();
    } else if (preset === 'float-reset') {
        resetFloatControls();
        updateFloatPreview();
    }

    // Tuple presets
    else if (preset === 'tuple-parentheses') {
        resetTupleControls();
        document.getElementById('tuple-format').value = 'parentheses';
        updateTuplePreview();
    } else if (preset === 'tuple-pills') {
        resetTupleControls();
        document.getElementById('tuple-format').value = 'plain';
        document.getElementById('tuple-direction').value = 'horizontal';
        document.getElementById('tuple-gap').value = '8px';
        document.getElementById('tuple-item-padding').value = '6px 14px';
        document.getElementById('tuple-item-border-radius').value = '20px';
        document.getElementById('tuple-item-background').value = '#e0e0e0';
        updateTuplePreview();
    } else if (preset === 'tuple-tags') {
        resetTupleControls();
        document.getElementById('tuple-format').value = 'plain';
        document.getElementById('tuple-direction').value = 'horizontal';
        document.getElementById('tuple-gap').value = '8px';
        document.getElementById('tuple-item-padding').value = '4px 10px';
        document.getElementById('tuple-item-border-radius').value = '4px';
        document.getElementById('tuple-item-background').value = '#f5f5f5';
        updateTuplePreview();
    } else if (preset === 'tuple-labeled') {
        resetTupleControls();
        document.getElementById('tuple-format').value = 'labeled';
        updateTuplePreview();
    } else if (preset === 'tuple-card') {
        resetTupleControls();
        document.getElementById('tuple-format').value = 'labeled';
        document.getElementById('tuple-padding').value = '16px';
        document.getElementById('tuple-border').value = '1px solid #e0e0e0';
        document.getElementById('tuple-border-radius').value = '8px';
        document.getElementById('tuple-background').value = 'white';
        updateTuplePreview();
    } else if (preset === 'tuple-reset') {
        resetTupleControls();
        updateTuplePreview();
    }

    // Set presets
    else if (preset === 'set-braces') {
        resetSetControls();
        document.getElementById('set-format').value = 'braces';
        updateSetPreview();
    } else if (preset === 'set-pills') {
        resetSetControls();
        document.getElementById('set-format').value = 'plain';
        document.getElementById('set-direction').value = 'horizontal';
        document.getElementById('set-gap').value = '8px';
        document.getElementById('set-item-padding').value = '6px 14px';
        document.getElementById('set-item-border-radius').value = '20px';
        document.getElementById('set-item-background').value = '#e0e0e0';
        updateSetPreview();
    } else if (preset === 'set-tags') {
        resetSetControls();
        document.getElementById('set-format').value = 'plain';
        document.getElementById('set-direction').value = 'horizontal';
        document.getElementById('set-gap').value = '8px';
        document.getElementById('set-item-padding').value = '4px 10px';
        document.getElementById('set-item-border-radius').value = '4px';
        document.getElementById('set-item-background').value = '#f5f5f5';
        updateSetPreview();
    } else if (preset === 'set-inline') {
        resetSetControls();
        document.getElementById('set-format').value = 'plain';
        document.getElementById('set-direction').value = 'horizontal';
        document.getElementById('set-gap').value = '8px';
        updateSetPreview();
    } else if (preset === 'set-reset') {
        resetSetControls();
        updateSetPreview();
    }
}

function resetStringControls() {
    document.getElementById('string-bold').checked = false;
    document.getElementById('string-italic').checked = false;
    document.getElementById('string-underline').checked = false;
    document.getElementById('string-strikethrough').checked = false;
    document.getElementById('string-monospace').checked = false;
    document.getElementById('string-uppercase').checked = false;
    document.getElementById('string-color').value = '';
    document.getElementById('string-background').value = '';
    document.getElementById('string-font-size').value = '';
    document.getElementById('string-padding').value = '';
    document.getElementById('string-border').value = '';
    document.getElementById('string-border-radius').value = '';
    document.getElementById('string-tag').value = 'span';
}

function resetListControls() {
    document.getElementById('list-direction').value = 'vertical';
    document.getElementById('list-type').value = 'unordered';
    document.getElementById('list-grid-columns').value = '3';
    document.getElementById('list-gap').value = '';
    document.getElementById('list-padding').value = '';
    document.getElementById('list-margin').value = '';
    document.getElementById('list-item-padding').value = '';
    document.getElementById('list-border').value = '';
    document.getElementById('list-border-radius').value = '';
    document.getElementById('list-item-border').value = '';
    document.getElementById('list-item-border-radius').value = '';
    document.getElementById('list-separator').value = '';
    document.getElementById('list-background').value = '';
    document.getElementById('list-item-background').value = '';
    document.getElementById('list-color').value = '';
    document.getElementById('list-align-items').value = '';
    document.getElementById('list-justify-content').value = '';
    document.getElementById('grid-columns-group').style.display = 'none';
}

function resetDictControls() {
    document.getElementById('dict-format').value = 'definition_list';
    document.getElementById('dict-layout').value = 'vertical';
    document.getElementById('dict-grid-columns').value = '2';
    document.getElementById('dict-key-bold').checked = false;
    document.getElementById('dict-key-italic').checked = false;
    document.getElementById('dict-key-color').value = '';
    document.getElementById('dict-key-background').value = '';
    document.getElementById('dict-key-width').value = '';
    document.getElementById('dict-key-padding').value = '';
    document.getElementById('dict-value-bold').checked = false;
    document.getElementById('dict-value-italic').checked = false;
    document.getElementById('dict-value-color').value = '';
    document.getElementById('dict-value-background').value = '';
    document.getElementById('dict-value-padding').value = '';
    document.getElementById('dict-separator').value = '';
    document.getElementById('dict-entry-separator').value = '';
    document.getElementById('dict-gap').value = '';
    document.getElementById('dict-padding').value = '';
    document.getElementById('dict-border').value = '';
    document.getElementById('dict-border-radius').value = '';
    document.getElementById('dict-background').value = '';
    document.getElementById('dict-width').value = '';
    document.getElementById('dict-grid-columns-group').style.display = 'none';
}

function resetIntControls() {
    document.getElementById('int-value').value = '1234567';
    document.getElementById('int-format').value = 'default';
    document.getElementById('int-currency-symbol').value = '$';
    document.getElementById('int-padded-width').value = '6';
    document.getElementById('int-bold').checked = false;
    document.getElementById('int-italic').checked = false;
    document.getElementById('int-underline').checked = false;
    document.getElementById('int-monospace').checked = false;
    document.getElementById('int-color').value = '';
    document.getElementById('int-background').value = '';
    document.getElementById('int-font-size').value = '';
    document.getElementById('int-padding').value = '';
    document.getElementById('int-border').value = '';
    document.getElementById('int-border-radius').value = '';
    document.getElementById('int-currency-symbol-group').style.display = 'none';
    document.getElementById('int-padded-width-group').style.display = 'none';
}

function resetFloatControls() {
    document.getElementById('float-value').value = '3.14159';
    document.getElementById('float-format').value = 'default';
    document.getElementById('float-currency-symbol').value = '$';
    document.getElementById('float-decimals').value = '2';
    document.getElementById('float-precision').value = '2';
    document.getElementById('float-figures').value = '3';
    document.getElementById('float-bold').checked = false;
    document.getElementById('float-italic').checked = false;
    document.getElementById('float-underline').checked = false;
    document.getElementById('float-monospace').checked = false;
    document.getElementById('float-color').value = '';
    document.getElementById('float-background').value = '';
    document.getElementById('float-font-size').value = '';
    document.getElementById('float-padding').value = '';
    document.getElementById('float-border').value = '';
    document.getElementById('float-border-radius').value = '';
    document.getElementById('float-currency-symbol-group').style.display = 'none';
    document.getElementById('float-decimals-group').style.display = 'none';
    document.getElementById('float-precision-group').style.display = 'none';
    document.getElementById('float-figures-group').style.display = 'none';
}

function resetTupleControls() {
    document.getElementById('tuple-items').value = 'Apple, Banana, Cherry';
    document.getElementById('tuple-namedtuple').checked = false;
    document.getElementById('tuple-format').value = 'parentheses';
    document.getElementById('tuple-direction').value = 'horizontal';
    document.getElementById('tuple-grid-columns').value = '3';
    document.getElementById('tuple-gap').value = '';
    document.getElementById('tuple-padding').value = '';
    document.getElementById('tuple-item-padding').value = '';
    document.getElementById('tuple-border').value = '';
    document.getElementById('tuple-border-radius').value = '';
    document.getElementById('tuple-item-border').value = '';
    document.getElementById('tuple-item-border-radius').value = '';
    document.getElementById('tuple-background').value = '';
    document.getElementById('tuple-item-background').value = '';
    document.getElementById('tuple-color').value = '';
    document.getElementById('tuple-grid-columns-group').style.display = 'none';
}

function resetSetControls() {
    document.getElementById('set-items').value = 'Apple, Banana, Cherry, Apple';
    document.getElementById('set-sorted').checked = false;
    document.getElementById('set-format').value = 'braces';
    document.getElementById('set-direction').value = 'horizontal';
    document.getElementById('set-grid-columns').value = '3';
    document.getElementById('set-gap').value = '';
    document.getElementById('set-padding').value = '';
    document.getElementById('set-item-padding').value = '';
    document.getElementById('set-border').value = '';
    document.getElementById('set-border-radius').value = '';
    document.getElementById('set-item-border').value = '';
    document.getElementById('set-item-border-radius').value = '';
    document.getElementById('set-background').value = '';
    document.getElementById('set-item-background').value = '';
    document.getElementById('set-color').value = '';
    document.getElementById('set-grid-columns-group').style.display = 'none';
}

// -------------------------------------------------------------------------
// HTMLString Controls
// -------------------------------------------------------------------------

function setupStringControls() {
    const controls = document.querySelectorAll('.string-control');
    controls.forEach(control => {
        control.addEventListener('input', debounce(updateStringPreview, 150));
        control.addEventListener('change', updateStringPreview);
    });

    // Color picker sync
    const colorPicker = document.getElementById('string-color-picker');
    const colorInput = document.getElementById('string-color');
    colorPicker.addEventListener('input', () => {
        colorInput.value = colorPicker.value;
        updateStringPreview();
    });

    const bgPicker = document.getElementById('string-background-picker');
    const bgInput = document.getElementById('string-background');
    bgPicker.addEventListener('input', () => {
        bgInput.value = bgPicker.value;
        updateStringPreview();
    });
}

function getStringData() {
    return {
        content: document.getElementById('string-content').value,
        bold: document.getElementById('string-bold').checked,
        italic: document.getElementById('string-italic').checked,
        underline: document.getElementById('string-underline').checked,
        strikethrough: document.getElementById('string-strikethrough').checked,
        monospace: document.getElementById('string-monospace').checked,
        uppercase: document.getElementById('string-uppercase').checked,
        color: document.getElementById('string-color').value,
        background: document.getElementById('string-background').value,
        font_size: document.getElementById('string-font-size').value,
        padding: document.getElementById('string-padding').value,
        border: document.getElementById('string-border').value,
        border_radius: document.getElementById('string-border-radius').value,
        tag: document.getElementById('string-tag').value,
    };
}

async function updateStringPreview() {
    const data = getStringData();

    try {
        // Render HTML for preview
        const renderResponse = await fetch('/api/render/string', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        const html = await renderResponse.text();
        document.getElementById('string-preview').innerHTML = html;

        // Get pretty-printed HTML
        const htmlResponse = await fetch('/api/html/string', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        const htmlData = await htmlResponse.json();
        document.getElementById('string-html').textContent = htmlData.html;

        // Get code
        const codeResponse = await fetch('/api/code/string', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        const codeData = await codeResponse.json();
        document.getElementById('string-code').textContent = codeData.code;
    } catch (error) {
        console.error('Error updating string preview:', error);
    }
}

// -------------------------------------------------------------------------
// HTMLInt Controls
// -------------------------------------------------------------------------

function setupIntControls() {
    const controls = document.querySelectorAll('.int-control');
    controls.forEach(control => {
        control.addEventListener('input', debounce(updateIntPreview, 150));
        control.addEventListener('change', updateIntPreview);
    });

    // Show/hide format options based on format selection
    const formatSelect = document.getElementById('int-format');
    formatSelect.addEventListener('change', () => {
        document.getElementById('int-currency-symbol-group').style.display =
            formatSelect.value === 'currency' ? 'block' : 'none';
        document.getElementById('int-padded-width-group').style.display =
            formatSelect.value === 'padded' ? 'block' : 'none';
        updateIntPreview();
    });

    // Color picker sync
    const colorPicker = document.getElementById('int-color-picker');
    const colorInput = document.getElementById('int-color');
    colorPicker.addEventListener('input', () => {
        colorInput.value = colorPicker.value;
        updateIntPreview();
    });

    const bgPicker = document.getElementById('int-background-picker');
    const bgInput = document.getElementById('int-background');
    bgPicker.addEventListener('input', () => {
        bgInput.value = bgPicker.value;
        updateIntPreview();
    });
}

function getIntData() {
    return {
        value: parseInt(document.getElementById('int-value').value) || 0,
        format: document.getElementById('int-format').value,
        currency_symbol: document.getElementById('int-currency-symbol').value,
        padded_width: parseInt(document.getElementById('int-padded-width').value) || 6,
        bold: document.getElementById('int-bold').checked,
        italic: document.getElementById('int-italic').checked,
        underline: document.getElementById('int-underline').checked,
        monospace: document.getElementById('int-monospace').checked,
        color: document.getElementById('int-color').value,
        background: document.getElementById('int-background').value,
        font_size: document.getElementById('int-font-size').value,
        padding: document.getElementById('int-padding').value,
        border: document.getElementById('int-border').value,
        border_radius: document.getElementById('int-border-radius').value,
    };
}

async function updateIntPreview() {
    const data = getIntData();

    try {
        // Render HTML for preview
        const renderResponse = await fetch('/api/render/int', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        const html = await renderResponse.text();
        document.getElementById('int-preview').innerHTML = html;

        // Get pretty-printed HTML
        const htmlResponse = await fetch('/api/html/int', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        const htmlData = await htmlResponse.json();
        document.getElementById('int-html').textContent = htmlData.html;

        // Get code
        const codeResponse = await fetch('/api/code/int', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        const codeData = await codeResponse.json();
        document.getElementById('int-code').textContent = codeData.code;
    } catch (error) {
        console.error('Error updating int preview:', error);
    }
}

// -------------------------------------------------------------------------
// HTMLFloat Controls
// -------------------------------------------------------------------------

function setupFloatControls() {
    const controls = document.querySelectorAll('.float-control');
    controls.forEach(control => {
        control.addEventListener('input', debounce(updateFloatPreview, 150));
        control.addEventListener('change', updateFloatPreview);
    });

    // Show/hide format options based on format selection
    const formatSelect = document.getElementById('float-format');
    formatSelect.addEventListener('change', () => {
        const format = formatSelect.value;
        document.getElementById('float-currency-symbol-group').style.display =
            format === 'currency' ? 'block' : 'none';
        document.getElementById('float-decimals-group').style.display =
            ['currency', 'percent', 'decimal'].includes(format) ? 'block' : 'none';
        document.getElementById('float-precision-group').style.display =
            format === 'scientific' ? 'block' : 'none';
        document.getElementById('float-figures-group').style.display =
            format === 'significant' ? 'block' : 'none';
        updateFloatPreview();
    });

    // Color picker sync
    const colorPicker = document.getElementById('float-color-picker');
    const colorInput = document.getElementById('float-color');
    colorPicker.addEventListener('input', () => {
        colorInput.value = colorPicker.value;
        updateFloatPreview();
    });

    const bgPicker = document.getElementById('float-background-picker');
    const bgInput = document.getElementById('float-background');
    bgPicker.addEventListener('input', () => {
        bgInput.value = bgPicker.value;
        updateFloatPreview();
    });
}

function getFloatData() {
    return {
        value: parseFloat(document.getElementById('float-value').value) || 0,
        format: document.getElementById('float-format').value,
        currency_symbol: document.getElementById('float-currency-symbol').value,
        decimals: parseInt(document.getElementById('float-decimals').value) || 2,
        precision: parseInt(document.getElementById('float-precision').value) || 2,
        figures: parseInt(document.getElementById('float-figures').value) || 3,
        bold: document.getElementById('float-bold').checked,
        italic: document.getElementById('float-italic').checked,
        underline: document.getElementById('float-underline').checked,
        monospace: document.getElementById('float-monospace').checked,
        color: document.getElementById('float-color').value,
        background: document.getElementById('float-background').value,
        font_size: document.getElementById('float-font-size').value,
        padding: document.getElementById('float-padding').value,
        border: document.getElementById('float-border').value,
        border_radius: document.getElementById('float-border-radius').value,
    };
}

async function updateFloatPreview() {
    const data = getFloatData();

    try {
        // Render HTML for preview
        const renderResponse = await fetch('/api/render/float', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        const html = await renderResponse.text();
        document.getElementById('float-preview').innerHTML = html;

        // Get pretty-printed HTML
        const htmlResponse = await fetch('/api/html/float', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        const htmlData = await htmlResponse.json();
        document.getElementById('float-html').textContent = htmlData.html;

        // Get code
        const codeResponse = await fetch('/api/code/float', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        const codeData = await codeResponse.json();
        document.getElementById('float-code').textContent = codeData.code;
    } catch (error) {
        console.error('Error updating float preview:', error);
    }
}

// -------------------------------------------------------------------------
// HTMLTuple Controls
// -------------------------------------------------------------------------

function setupTupleControls() {
    const controls = document.querySelectorAll('.tuple-control');
    controls.forEach(control => {
        control.addEventListener('input', debounce(updateTuplePreview, 150));
        control.addEventListener('change', updateTuplePreview);
    });

    // Show/hide grid columns based on direction
    const directionSelect = document.getElementById('tuple-direction');
    directionSelect.addEventListener('change', () => {
        document.getElementById('tuple-grid-columns-group').style.display =
            directionSelect.value === 'grid' ? 'block' : 'none';
        updateTuplePreview();
    });

    // Color picker sync
    const bgPicker = document.getElementById('tuple-background-picker');
    const bgInput = document.getElementById('tuple-background');
    bgPicker.addEventListener('input', () => {
        bgInput.value = bgPicker.value;
        updateTuplePreview();
    });

    const itemBgPicker = document.getElementById('tuple-item-background-picker');
    const itemBgInput = document.getElementById('tuple-item-background');
    itemBgPicker.addEventListener('input', () => {
        itemBgInput.value = itemBgPicker.value;
        updateTuplePreview();
    });

    const colorPicker = document.getElementById('tuple-color-picker');
    const colorInput = document.getElementById('tuple-color');
    colorPicker.addEventListener('input', () => {
        colorInput.value = colorPicker.value;
        updateTuplePreview();
    });
}

function getTupleData() {
    return {
        items: document.getElementById('tuple-items').value,
        namedtuple: document.getElementById('tuple-namedtuple').checked,
        format: document.getElementById('tuple-format').value,
        direction: document.getElementById('tuple-direction').value,
        grid_columns: parseInt(document.getElementById('tuple-grid-columns').value) || 3,
        gap: document.getElementById('tuple-gap').value,
        padding: document.getElementById('tuple-padding').value,
        item_padding: document.getElementById('tuple-item-padding').value,
        border: document.getElementById('tuple-border').value,
        border_radius: document.getElementById('tuple-border-radius').value,
        item_border: document.getElementById('tuple-item-border').value,
        item_border_radius: document.getElementById('tuple-item-border-radius').value,
        background: document.getElementById('tuple-background').value,
        item_background: document.getElementById('tuple-item-background').value,
        color: document.getElementById('tuple-color').value,
    };
}

async function updateTuplePreview() {
    const data = getTupleData();

    try {
        // Render HTML for preview
        const renderResponse = await fetch('/api/render/tuple', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        const html = await renderResponse.text();
        document.getElementById('tuple-preview').innerHTML = html;

        // Get pretty-printed HTML
        const htmlResponse = await fetch('/api/html/tuple', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        const htmlData = await htmlResponse.json();
        document.getElementById('tuple-html').textContent = htmlData.html;

        // Get code
        const codeResponse = await fetch('/api/code/tuple', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        const codeData = await codeResponse.json();
        document.getElementById('tuple-code').textContent = codeData.code;
    } catch (error) {
        console.error('Error updating tuple preview:', error);
    }
}

// -------------------------------------------------------------------------
// HTMLSet Controls
// -------------------------------------------------------------------------

function setupSetControls() {
    const controls = document.querySelectorAll('.set-control');
    controls.forEach(control => {
        control.addEventListener('input', debounce(updateSetPreview, 150));
        control.addEventListener('change', updateSetPreview);
    });

    // Show/hide grid columns based on direction
    const directionSelect = document.getElementById('set-direction');
    directionSelect.addEventListener('change', () => {
        document.getElementById('set-grid-columns-group').style.display =
            directionSelect.value === 'grid' ? 'block' : 'none';
        updateSetPreview();
    });

    // Color picker sync
    const bgPicker = document.getElementById('set-background-picker');
    const bgInput = document.getElementById('set-background');
    bgPicker.addEventListener('input', () => {
        bgInput.value = bgPicker.value;
        updateSetPreview();
    });

    const itemBgPicker = document.getElementById('set-item-background-picker');
    const itemBgInput = document.getElementById('set-item-background');
    itemBgPicker.addEventListener('input', () => {
        itemBgInput.value = itemBgPicker.value;
        updateSetPreview();
    });

    const colorPicker = document.getElementById('set-color-picker');
    const colorInput = document.getElementById('set-color');
    colorPicker.addEventListener('input', () => {
        colorInput.value = colorPicker.value;
        updateSetPreview();
    });
}

function getSetData() {
    return {
        items: document.getElementById('set-items').value,
        sorted: document.getElementById('set-sorted').checked,
        format: document.getElementById('set-format').value,
        direction: document.getElementById('set-direction').value,
        grid_columns: parseInt(document.getElementById('set-grid-columns').value) || 3,
        gap: document.getElementById('set-gap').value,
        padding: document.getElementById('set-padding').value,
        item_padding: document.getElementById('set-item-padding').value,
        border: document.getElementById('set-border').value,
        border_radius: document.getElementById('set-border-radius').value,
        item_border: document.getElementById('set-item-border').value,
        item_border_radius: document.getElementById('set-item-border-radius').value,
        background: document.getElementById('set-background').value,
        item_background: document.getElementById('set-item-background').value,
        color: document.getElementById('set-color').value,
    };
}

async function updateSetPreview() {
    const data = getSetData();

    try {
        // Render HTML for preview
        const renderResponse = await fetch('/api/render/set', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        const html = await renderResponse.text();
        document.getElementById('set-preview').innerHTML = html;

        // Get pretty-printed HTML
        const htmlResponse = await fetch('/api/html/set', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        const htmlData = await htmlResponse.json();
        document.getElementById('set-html').textContent = htmlData.html;

        // Get code
        const codeResponse = await fetch('/api/code/set', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        const codeData = await codeResponse.json();
        document.getElementById('set-code').textContent = codeData.code;
    } catch (error) {
        console.error('Error updating set preview:', error);
    }
}

// -------------------------------------------------------------------------
// HTMLList Controls
// -------------------------------------------------------------------------

function setupListControls() {
    const controls = document.querySelectorAll('.list-control');
    controls.forEach(control => {
        control.addEventListener('input', debounce(updateListPreview, 150));
        control.addEventListener('change', updateListPreview);
    });

    // Show/hide grid columns based on direction
    const directionSelect = document.getElementById('list-direction');
    const gridColumnsGroup = document.getElementById('grid-columns-group');
    directionSelect.addEventListener('change', () => {
        gridColumnsGroup.style.display = directionSelect.value === 'grid' ? 'block' : 'none';
        updateListPreview();
    });

    // Color picker sync
    setupColorPicker('list-background');
    setupColorPicker('list-item-background');
    setupColorPicker('list-color');
}

function setupColorPicker(baseName) {
    const picker = document.getElementById(`${baseName}-picker`);
    const input = document.getElementById(baseName);
    if (picker && input) {
        picker.addEventListener('input', () => {
            input.value = picker.value;
            updateListPreview();
        });
    }
}

function getListData() {
    return {
        items: document.getElementById('list-items').value,
        direction: document.getElementById('list-direction').value,
        list_type: document.getElementById('list-type').value,
        grid_columns: parseInt(document.getElementById('list-grid-columns').value) || 3,
        gap: document.getElementById('list-gap').value,
        padding: document.getElementById('list-padding').value,
        margin: document.getElementById('list-margin').value,
        item_padding: document.getElementById('list-item-padding').value,
        border: document.getElementById('list-border').value,
        border_radius: document.getElementById('list-border-radius').value,
        item_border: document.getElementById('list-item-border').value,
        item_border_radius: document.getElementById('list-item-border-radius').value,
        separator: document.getElementById('list-separator').value,
        background: document.getElementById('list-background').value,
        item_background: document.getElementById('list-item-background').value,
        color: document.getElementById('list-color').value,
        align_items: document.getElementById('list-align-items').value,
        justify_content: document.getElementById('list-justify-content').value,
    };
}

async function updateListPreview() {
    const data = getListData();

    try {
        // Render HTML for preview
        const renderResponse = await fetch('/api/render/list', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        const html = await renderResponse.text();
        document.getElementById('list-preview').innerHTML = html;

        // Get pretty-printed HTML
        const htmlResponse = await fetch('/api/html/list', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        const htmlData = await htmlResponse.json();
        document.getElementById('list-html').textContent = htmlData.html;

        // Get code
        const codeResponse = await fetch('/api/code/list', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        const codeData = await codeResponse.json();
        document.getElementById('list-code').textContent = codeData.code;
    } catch (error) {
        console.error('Error updating list preview:', error);
    }
}

// -------------------------------------------------------------------------
// HTMLDict Controls
// -------------------------------------------------------------------------

function setupDictControls() {
    const controls = document.querySelectorAll('.dict-control');
    controls.forEach(control => {
        control.addEventListener('input', debounce(updateDictPreview, 150));
        control.addEventListener('change', updateDictPreview);
    });

    // Show/hide grid columns based on layout
    const layoutSelect = document.getElementById('dict-layout');
    const gridColumnsGroup = document.getElementById('dict-grid-columns-group');
    layoutSelect.addEventListener('change', () => {
        gridColumnsGroup.style.display = layoutSelect.value === 'grid' ? 'block' : 'none';
        updateDictPreview();
    });

    // Color picker sync
    setupColorPicker('dict-key-color');
    setupColorPicker('dict-key-background');
    setupColorPicker('dict-value-color');
    setupColorPicker('dict-value-background');
    setupColorPicker('dict-background');
}

function getDictData() {
    return {
        items: document.getElementById('dict-items').value,
        format: document.getElementById('dict-format').value,
        layout: document.getElementById('dict-layout').value,
        grid_columns: parseInt(document.getElementById('dict-grid-columns').value) || 2,
        key_bold: document.getElementById('dict-key-bold').checked,
        key_italic: document.getElementById('dict-key-italic').checked,
        key_color: document.getElementById('dict-key-color').value,
        key_background: document.getElementById('dict-key-background').value,
        key_width: document.getElementById('dict-key-width').value,
        key_padding: document.getElementById('dict-key-padding').value,
        value_bold: document.getElementById('dict-value-bold').checked,
        value_italic: document.getElementById('dict-value-italic').checked,
        value_color: document.getElementById('dict-value-color').value,
        value_background: document.getElementById('dict-value-background').value,
        value_padding: document.getElementById('dict-value-padding').value,
        separator: document.getElementById('dict-separator').value,
        entry_separator: document.getElementById('dict-entry-separator').value,
        gap: document.getElementById('dict-gap').value,
        padding: document.getElementById('dict-padding').value,
        border: document.getElementById('dict-border').value,
        border_radius: document.getElementById('dict-border-radius').value,
        background: document.getElementById('dict-background').value,
        width: document.getElementById('dict-width').value,
    };
}

async function updateDictPreview() {
    const data = getDictData();

    try {
        // Render HTML for preview
        const renderResponse = await fetch('/api/render/dict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        const html = await renderResponse.text();
        document.getElementById('dict-preview').innerHTML = html;

        // Get pretty-printed HTML
        const htmlResponse = await fetch('/api/html/dict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        const htmlData = await htmlResponse.json();
        document.getElementById('dict-html').textContent = htmlData.html;

        // Get code
        const codeResponse = await fetch('/api/code/dict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        const codeData = await codeResponse.json();
        document.getElementById('dict-code').textContent = codeData.code;
    } catch (error) {
        console.error('Error updating dict preview:', error);
    }
}

// -------------------------------------------------------------------------
// Dict of Lists Controls
// -------------------------------------------------------------------------

function setupDictOfListsControls() {
    const controls = document.querySelectorAll('.dol-control');
    controls.forEach(control => {
        control.addEventListener('input', debounce(updateDictOfListsPreview, 150));
        control.addEventListener('change', updateDictOfListsPreview);
    });

    // Color picker sync
    setupColorPicker('dol-key-color');
    setupColorPicker('dol-item-background');
}

function getDictOfListsData() {
    return {
        fruits: document.getElementById('dol-fruits').value,
        vegetables: document.getElementById('dol-vegetables').value,
        grains: document.getElementById('dol-grains').value,
        dict_format: document.getElementById('dol-dict-format').value,
        key_bold: document.getElementById('dol-key-bold').checked,
        key_color: document.getElementById('dol-key-color').value,
        list_direction: document.getElementById('dol-list-direction').value,
        list_gap: document.getElementById('dol-list-gap').value,
        item_background: document.getElementById('dol-item-background').value,
        item_padding: document.getElementById('dol-item-padding').value,
        item_border_radius: document.getElementById('dol-item-border-radius').value,
    };
}

async function updateDictOfListsPreview() {
    const data = getDictOfListsData();

    try {
        const renderResponse = await fetch('/api/render/dict-of-lists', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        const html = await renderResponse.text();
        document.getElementById('dol-preview').innerHTML = html;

        const htmlResponse = await fetch('/api/html/dict-of-lists', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        const htmlData = await htmlResponse.json();
        document.getElementById('dol-html').textContent = htmlData.html;

        const codeResponse = await fetch('/api/code/dict-of-lists', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        const codeData = await codeResponse.json();
        document.getElementById('dol-code').textContent = codeData.code;
    } catch (error) {
        console.error('Error updating dict of lists preview:', error);
    }
}

// -------------------------------------------------------------------------
// List of Dicts Controls
// -------------------------------------------------------------------------

function setupListOfDictsControls() {
    const controls = document.querySelectorAll('.lod-control');
    controls.forEach(control => {
        control.addEventListener('input', debounce(updateListOfDictsPreview, 150));
        control.addEventListener('change', updateListOfDictsPreview);
    });

    // Color picker sync
    setupColorPicker('lod-card-background');
}

function getListOfDictsData() {
    return {
        record1_name: document.getElementById('lod-record1-name').value,
        record1_role: document.getElementById('lod-record1-role').value,
        record2_name: document.getElementById('lod-record2-name').value,
        record2_role: document.getElementById('lod-record2-role').value,
        record3_name: document.getElementById('lod-record3-name').value,
        record3_role: document.getElementById('lod-record3-role').value,
        list_direction: document.getElementById('lod-list-direction').value,
        list_gap: document.getElementById('lod-list-gap').value,
        card_format: document.getElementById('lod-card-format').value,
        card_padding: document.getElementById('lod-card-padding').value,
        card_border: document.getElementById('lod-card-border').value,
        card_border_radius: document.getElementById('lod-card-border-radius').value,
        card_background: document.getElementById('lod-card-background').value,
        key_bold: document.getElementById('lod-key-bold').checked,
    };
}

async function updateListOfDictsPreview() {
    const data = getListOfDictsData();

    try {
        const renderResponse = await fetch('/api/render/list-of-dicts', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        const html = await renderResponse.text();
        document.getElementById('lod-preview').innerHTML = html;

        const htmlResponse = await fetch('/api/html/list-of-dicts', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        const htmlData = await htmlResponse.json();
        document.getElementById('lod-html').textContent = htmlData.html;

        const codeResponse = await fetch('/api/code/list-of-dicts', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        const codeData = await codeResponse.json();
        document.getElementById('lod-code').textContent = codeData.code;
    } catch (error) {
        console.error('Error updating list of dicts preview:', error);
    }
}

// -------------------------------------------------------------------------
// Utility functions
// -------------------------------------------------------------------------

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
