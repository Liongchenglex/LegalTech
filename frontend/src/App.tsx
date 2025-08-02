import React, { useState, useEffect } from 'react';
import './App.css';

/**
 * Main App Component
 * 
 * Entry point for the LegalTech MVP frontend application.
 * Demonstrates API connectivity and basic UI structure.
 */
function App() {
  const [apiStatus, setApiStatus] = useState<string>('Checking...');
  const [apiData, setApiData] = useState<any>(null);

  /**
   * Test API connectivity on component mount
   * Demonstrates backend integration pattern
   */
  useEffect(() => {
    const testApiConnection = async () => {
      try {
        // Test health endpoint
        const healthResponse = await fetch('http://localhost:3000/health');
        if (healthResponse.ok) {
          const healthData = await healthResponse.json();
          setApiStatus('✅ Connected');
          
          // Get API info
          const apiResponse = await fetch('http://localhost:3000/api');
          const apiInfo = await apiResponse.json();
          setApiData(apiInfo);
        } else {
          setApiStatus('❌ Health check failed');
        }
      } catch (error) {
        setApiStatus('❌ Backend not running');
        console.error('API connection error:', error);
      }
    };

    testApiConnection();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>🏛️ LegalTech MVP</h1>
        <p>A scalable Legal Technology platform</p>
        
        <div className="status-card">
          <h3>System Status</h3>
          <p><strong>Backend API:</strong> {apiStatus}</p>
          {apiData && (
            <div className="api-info">
              <p><strong>API Version:</strong> {apiData.version}</p>
              <p><strong>Last Updated:</strong> {new Date(apiData.timestamp).toLocaleString()}</p>
            </div>
          )}
        </div>

        <div className="info-grid">
          <div className="info-card">
            <h4>🚀 Ready for Development</h4>
            <ul>
              <li>✅ Frontend: React + TypeScript + Vite</li>
              <li>✅ Backend: Node.js + Express + TypeScript</li>
              <li>✅ CI/CD: GitHub Actions</li>
              <li>✅ Code Quality: ESLint + Prettier</li>
            </ul>
          </div>
          
          <div className="info-card">
            <h4>📚 Next Steps</h4>
            <ul>
              <li>🔐 Implement authentication system</li>
              <li>📄 Add document management</li>
              <li>👥 Create user management</li>
              <li>🛡️ Add legal compliance features</li>
            </ul>
          </div>
        </div>

        <div className="links">
          <a 
            href="https://github.com/Liongchenglex/LegalTech" 
            target="_blank" 
            rel="noopener noreferrer"
          >
            📖 View Documentation
          </a>
        </div>
      </header>
    </div>
  );
}

export default App;