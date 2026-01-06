const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, '..')));

// Store connections (in production, use a database)
const connectionsFile = path.join(__dirname, 'connections.json');

function getConnections() {
    try {
        if (fs.existsSync(connectionsFile)) {
            return JSON.parse(fs.readFileSync(connectionsFile, 'utf8'));
        }
    } catch (error) {
        console.error('Error reading connections:', error);
    }
    return [];
}

function saveConnection(connection) {
    try {
        const connections = getConnections();
        connections.push({
            ...connection,
            id: Date.now(),
            connected_at: new Date().toISOString(),
            status: 'active'
        });
        fs.writeFileSync(connectionsFile, JSON.stringify(connections, null, 2));
        return true;
    } catch (error) {
        console.error('Error saving connection:', error);
        return false;
    }
}

// API Routes
app.post('/api/connect-repo', (req, res) => {
    const { provider, repo_url, branch = 'main' } = req.body;

    // Validation
    if (!provider || !repo_url) {
        return res.status(400).json({ 
            error: 'Provider and repository URL are required' 
        });
    }

    // Validate URL format
    const urlPattern = /^https?:\/\/(github|gitlab|bitbucket)\.com\/[\w\-\.]+\/[\w\-\.]+/i;
    if (!urlPattern.test(repo_url)) {
        return res.status(400).json({ 
            error: 'Invalid repository URL format' 
        });
    }

    // Validate provider matches URL
    const urlProvider = repo_url.match(/github|gitlab|bitbucket/i)[0].toLowerCase();
    if (provider !== urlProvider) {
        return res.status(400).json({ 
            error: `Provider mismatch: URL contains ${urlProvider} but you selected ${provider}` 
        });
    }

    // Save connection
    const connection = {
        provider,
        repo_url,
        branch,
    };

    if (saveConnection(connection)) {
        console.log(`Repository connected: ${repo_url} (${provider})`);
        res.json({
            success: true,
            message: 'Repository connected successfully',
            data: {
                ...connection,
                id: Date.now(),
                connected_at: new Date().toISOString()
            }
        });
    } else {
        res.status(500).json({ 
            error: 'Failed to save connection' 
        });
    }
});

// Get all connections
app.get('/api/connections', (req, res) => {
    const connections = getConnections();
    res.json({ connections });
});

// Get connection by ID
app.get('/api/connections/:id', (req, res) => {
    const connections = getConnections();
    const connection = connections.find(c => c.id === parseInt(req.params.id));
    
    if (connection) {
        res.json({ connection });
    } else {
        res.status(404).json({ error: 'Connection not found' });
    }
});

// Health check
app.get('/api/health', (req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Serve static files
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, '..', 'index.html'));
});

app.listen(PORT, () => {
    console.log(`🚀 DEIVERSE API Server running on http://localhost:${PORT}`);
    console.log(`📡 API endpoints:`);
    console.log(`   POST /api/connect-repo - Connect a repository`);
    console.log(`   GET  /api/connections - Get all connections`);
    console.log(`   GET  /api/connections/:id - Get connection by ID`);
    console.log(`   GET  /api/health - Health check`);
});

