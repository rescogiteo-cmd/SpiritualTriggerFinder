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
            
            if (!status.running && status.progress > 0) {
                clearInterval(statusInterval);
                await loadResults();
            }
        } catch (error) {
            console.error('Error polling status:', error);
        }
    }, 1000);
}

function updateStatus(status) {
    const messageEl = document.getElementById('statusMessage');
    const progressFill = document.getElementById('progressFill');
    const progressText = document.getElementById('progressText');
    
    messageEl.textContent = status.message || 'Processing...';
    
    if (status.total > 0) {
        const percentage = (status.progress / status.total) * 100;
        progressFill.style.width = percentage + '%';
        progressText.textContent = `${status.progress} / ${status.total} communities processed`;
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
