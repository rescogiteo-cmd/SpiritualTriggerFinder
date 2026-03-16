let communities = ['spirituality', 'meditation', 'Mindfulness', 'awakened'];
let statusInterval = null;

function updateValue(elementId, value) {
    document.getElementById(elementId).textContent = value;
}

function addSubreddit() {
    const input = document.getElementById('subredditInput');
    const subreddit = input.value.trim();
    
    if (!subreddit) {
        alert('Please enter a subreddit name');
        return;
    }
    
    if (communities.includes(subreddit)) {
        alert('This subreddit is already added');
        return;
    }
    
    communities.push(subreddit);
    input.value = '';
    renderCommunities();
}

function removeSubreddit(subreddit) {
    communities = communities.filter(c => c !== subreddit);
    renderCommunities();
}

function renderCommunities() {
    const listEl = document.getElementById('communityList');
    
    if (communities.length === 0) {
        listEl.innerHTML = '<p style="color: #999;">No communities added. Add one above.</p>';
        return;
    }
    
    listEl.innerHTML = communities.map(community => `
        <div class="community-tag">
            <span>${community}</span>
            <button onclick="removeSubreddit('${community}')">×</button>
        </div>
    `).join('');
}

document.getElementById('subredditInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        addSubreddit();
    }
});

document.getElementById('showComments').addEventListener('change', function(e) {
    document.getElementById('maxCommentsGroup').style.display = e.target.checked ? 'block' : 'none';
});

async function startAnalysis() {
    const analyzeBtn = document.getElementById('analyzeBtn');
    const resultsSection = document.getElementById('resultsSection');
    
    analyzeBtn.disabled = true;
    analyzeBtn.textContent = '⏳ Analyzing...';
    resultsSection.style.display = 'none';
    
    const config = {
        communities: communities,
        postsPerCommunity: parseInt(document.getElementById('postsPerCommunity').value),
        showComments: document.getElementById('showComments').checked,
        maxComments: parseInt(document.getElementById('maxComments').value),
        sleepTime: parseInt(document.getElementById('sleepTime').value)
    };
    
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(config)
        });
        
        if (!response.ok) {
            const error = await response.json();
            alert(error.error || 'Failed to start analysis');
            analyzeBtn.disabled = false;
            analyzeBtn.textContent = '🚀 Start Analysis';
            return;
        }
        
        startStatusPolling();
        
    } catch (error) {
        alert('Error: ' + error.message);
        analyzeBtn.disabled = false;
        analyzeBtn.textContent = '🚀 Start Analysis';
    }
}

function startStatusPolling() {
    if (statusInterval) {
        clearInterval(statusInterval);
    }

    statusInterval = setInterval(async () => {
        try {
            const response = await fetch('/status');
            const status = await response.json();

            updateStatus(status);

            if (!status.running && status.phase === 'done') {
                clearInterval(statusInterval);
                await loadResults();
            } else if (!status.running && status.phase === 'error') {
                clearInterval(statusInterval);
                const analyzeBtn = document.getElementById('analyzeBtn');
                analyzeBtn.disabled = false;
                analyzeBtn.textContent = '🚀 Start Analysis';
            }
        } catch (error) {
            console.error('Error polling status:', error);
        }
    }, 500);
}

function formatTime(seconds) {
    if (seconds === null || seconds === undefined) return '—';
    const s = Math.round(seconds);
    if (s < 60) return `${s}s`;
    const m = Math.floor(s / 60);
    const rem = s % 60;
    return `${m}m ${rem}s`;
}

function updateStatus(status) {
    const messageEl = document.getElementById('statusMessage');
    const progressFill = document.getElementById('progressFill');
    const postProgressText = document.getElementById('postProgressText');
    const communityProgressText = document.getElementById('communityProgressText');
    const elapsedText = document.getElementById('elapsedText');
    const etaText = document.getElementById('etaText');
    const postsFoundText = document.getElementById('postsFoundText');
    const phaseIndicator = document.getElementById('phaseIndicator');

    messageEl.textContent = status.message || 'Processing...';

    if (status.total_posts > 0) {
        const percentage = Math.min((status.posts_scanned / status.total_posts) * 100, 100);
        progressFill.style.width = percentage.toFixed(1) + '%';
        postProgressText.textContent = `${status.posts_scanned} / ${status.total_posts} posts scanned`;
    }

    communityProgressText.textContent = `${status.communities_done} / ${status.total_communities} communities done`;
    postsFoundText.textContent = status.posts_found || 0;
    elapsedText.textContent = formatTime(status.elapsed);
    etaText.textContent = status.phase === 'done' ? 'Done!' : formatTime(status.eta);

    const phaseLabels = {
        'idle': '',
        'connecting': '🔌 Connecting',
        'scanning': '🔍 Scanning',
        'sleeping': '😴 Rate limiting',
        'exporting': '💾 Saving files',
        'done': '✅ Complete',
        'error': '❌ Error'
    };
    const phaseColors = {
        'scanning': '#667eea',
        'sleeping': '#f6ad55',
        'exporting': '#48bb78',
        'done': '#48bb78',
        'error': '#e53e3e'
    };
    if (phaseIndicator) {
        phaseIndicator.textContent = phaseLabels[status.phase] || '';
        phaseIndicator.style.background = phaseColors[status.phase] || '#667eea';
    }
}

async function loadResults() {
    const analyzeBtn = document.getElementById('analyzeBtn');
    analyzeBtn.disabled = false;
    analyzeBtn.textContent = '🚀 Start Analysis';
    
    try {
        const response = await fetch('/results');
        const results = await response.json();
        
        displayResults(results);
        
    } catch (error) {
        console.error('Error loading results:', error);
    }
}

function displayResults(results) {
    const resultsSection = document.getElementById('resultsSection');
    const summaryEl = document.getElementById('resultsSummary');
    const previewEl = document.getElementById('postsPreview');
    
    resultsSection.style.display = 'block';
    
    const emotionCounts = {};
    results.forEach(post => {
        post.emotions.forEach(emotion => {
            emotionCounts[emotion] = (emotionCounts[emotion] || 0) + 1;
        });
    });
    
    const emotionEntries = Object.entries(emotionCounts).sort((a, b) => b[1] - a[1]);
    
    summaryEl.innerHTML = `
        <h4>📊 Found ${results.length} emotionally charged posts</h4>
        <div class="emotion-stats">
            ${emotionEntries.map(([emotion, count]) => {
                const percentage = ((count / results.length) * 100).toFixed(1);
                return `
                    <div class="emotion-item">
                        <h4>${emotion}</h4>
                        <div class="count">${count}</div>
                        <div class="percentage">${percentage}%</div>
                    </div>
                `;
            }).join('')}
        </div>
    `;
    
    const previewPosts = results.slice(0, 6);
    previewEl.innerHTML = `
        <h3>Recent Posts Preview (showing ${previewPosts.length} of ${results.length})</h3>
        ${previewPosts.map((post, idx) => `
            <div class="post-card">
                <h4>${idx + 1}. ${post.title}</h4>
                <div class="post-meta">
                    r/${post.community} • ${post.upvotes} ↑ • ${post.num_comments} comments • ${post.created_date}
                </div>
                <div class="post-emotions">
                    ${post.emotions.map(e => `<span class="emotion-badge">${e.toUpperCase()}</span>`).join('')}
                </div>
            </div>
        `).join('')}
    `;
}

// ── Keywords Editor ──────────────────────────────────────────────

let keywordsData = {};  // { emotion: [words] }
let keywordColors = {}; // { emotion: color }

const DEFAULT_COLORS = [
    '#e53e3e','#d69e2e','#805ad5','#2b6cb0','#c05621',
    '#2f855a','#b83280','#2c7a7b','#744210','#1a365d'
];

async function loadKeywords() {
    try {
        const res = await fetch('/keywords');
        const data = await res.json();
        keywordsData = data.patterns || {};
        keywordColors = data.colors || {};
        renderKeywordsEditor();
    } catch (e) {
        console.error('Failed to load keywords', e);
    }
}

function renderKeywordsEditor() {
    const grid = document.getElementById('keywordsEditor');
    grid.innerHTML = Object.entries(keywordsData).map(([emotion, words]) => {
        const color = keywordColors[emotion] || '#667eea';
        return `
        <div class="emotion-card" id="card-${emotion}">
            <div class="emotion-card-header">
                <input class="emotion-name-input"
                       id="name-${emotion}"
                       value="${emotion}"
                       style="background:${color}"
                       oninput="renameEmotion('${emotion}', this)"
                       onblur="commitRename('${emotion}', this)">
                <input type="color"
                       class="emotion-color-picker"
                       value="${color}"
                       title="Change color"
                       oninput="changeColor('${emotion}', this.value)">
                <button class="btn-remove-emotion"
                        onclick="removeEmotion('${emotion}')"
                        title="Remove this emotion">×</button>
            </div>
            <div class="keyword-tags" id="tags-${emotion}">
                ${words.map(w => keywordTagHTML(emotion, w)).join('')}
            </div>
            <div class="keyword-add-row">
                <input type="text"
                       id="new-kw-${emotion}"
                       placeholder="Add keyword…"
                       onkeypress="if(event.key==='Enter') addKeyword('${emotion}')">
                <button class="btn-add-keyword" onclick="addKeyword('${emotion}')">Add</button>
            </div>
        </div>`;
    }).join('');
}

function keywordTagHTML(emotion, word) {
    const safe = word.replace(/"/g, '&quot;');
    return `<span class="keyword-tag">
        ${word}
        <button onclick="removeKeyword('${emotion}', '${safe}')" title="Remove">×</button>
    </span>`;
}

function addKeyword(emotion) {
    const input = document.getElementById(`new-kw-${emotion}`);
    const word = input.value.trim();
    if (!word) return;
    if (!keywordsData[emotion].includes(word)) {
        keywordsData[emotion].push(word);
        const tagsEl = document.getElementById(`tags-${emotion}`);
        tagsEl.insertAdjacentHTML('beforeend', keywordTagHTML(emotion, word));
    }
    input.value = '';
    input.focus();
    markUnsaved();
}

function removeKeyword(emotion, word) {
    keywordsData[emotion] = keywordsData[emotion].filter(w => w !== word);
    renderKeywordsEditor();
    markUnsaved();
}

function removeEmotion(emotion) {
    if (!confirm(`Remove the "${emotion}" emotion category and all its keywords?`)) return;
    delete keywordsData[emotion];
    delete keywordColors[emotion];
    renderKeywordsEditor();
    markUnsaved();
}

function addEmotion() {
    const name = prompt('Name for the new emotion category (e.g. grief):');
    if (!name || !name.trim()) return;
    const key = name.trim().toLowerCase();
    if (keywordsData[key]) {
        alert(`"${key}" already exists.`);
        return;
    }
    keywordsData[key] = [];
    const usedColors = Object.values(keywordColors);
    keywordColors[key] = DEFAULT_COLORS.find(c => !usedColors.includes(c)) || '#667eea';
    renderKeywordsEditor();
    markUnsaved();
    document.getElementById(`new-kw-${key}`).focus();
}

function renameEmotion(oldName, inputEl) {
    const color = keywordColors[oldName] || '#667eea';
    inputEl.style.background = color;
}

function commitRename(oldName, inputEl) {
    const newName = inputEl.value.trim().toLowerCase();
    if (!newName || newName === oldName) { inputEl.value = oldName; return; }
    if (keywordsData[newName]) {
        alert(`"${newName}" already exists.`);
        inputEl.value = oldName;
        return;
    }
    keywordsData[newName] = keywordsData[oldName];
    keywordColors[newName] = keywordColors[oldName];
    delete keywordsData[oldName];
    delete keywordColors[oldName];
    renderKeywordsEditor();
    markUnsaved();
}

function changeColor(emotion, color) {
    keywordColors[emotion] = color;
    const nameInput = document.getElementById(`name-${emotion}`);
    if (nameInput) nameInput.style.background = color;
    markUnsaved();
}

function markUnsaved() {
    const btn = document.getElementById('saveKeywordsBtn');
    btn.textContent = 'Save Changes ●';
    btn.style.boxShadow = '0 0 0 3px rgba(102,126,234,0.4)';
    document.getElementById('saveStatus').textContent = '';
}

async function saveKeywords() {
    const btn = document.getElementById('saveKeywordsBtn');
    const statusEl = document.getElementById('saveStatus');
    btn.disabled = true;
    btn.textContent = 'Saving…';

    try {
        const res = await fetch('/keywords', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ patterns: keywordsData, colors: keywordColors })
        });
        const data = await res.json();
        if (res.ok) {
            keywordsData = data.patterns;
            renderKeywordsEditor();
            statusEl.className = 'save-status success';
            statusEl.textContent = '✅ Keywords saved successfully!';
        } else {
            statusEl.className = 'save-status error';
            statusEl.textContent = '❌ ' + (data.error || 'Save failed');
        }
    } catch (e) {
        statusEl.className = 'save-status error';
        statusEl.textContent = '❌ Network error';
    }

    btn.disabled = false;
    btn.textContent = 'Save Changes';
    btn.style.boxShadow = '';
}

loadKeywords();
