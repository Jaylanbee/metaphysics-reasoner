import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import ChartLibrary from './pages/ChartLibrary';
import Statistics from './pages/Statistics';
import { getTranslation } from './i18n';
import { useState } from 'react';

function App() {
  const [lang, setLang] = useState<'en'|'zh-TW'|'zh-CN'|'ja'>('zh-TW');

  return (
    <Router>
      <div style={{ fontFamily: 'sans-serif', margin: '0 auto', maxWidth: '1200px' }}>
        <nav style={{ padding: '1rem', borderBottom: '1px solid #ccc', marginBottom: '2rem', display: 'flex', justifyContent: 'space-between' }}>
          <ul style={{ listStyle: 'none', display: 'flex', gap: '2rem', margin: 0, padding: 0 }}>
            <li>
              <Link to="/" style={{ textDecoration: 'none', color: '#0066cc', fontWeight: 'bold' }}>{getTranslation(lang, 'dashboard')}</Link>
            </li>
            <li>
              <Link to="/library" style={{ textDecoration: 'none', color: '#0066cc', fontWeight: 'bold' }}>{getTranslation(lang, 'library')}</Link>
            </li>
            <li>
              <Link to="/stats" style={{ textDecoration: 'none', color: '#0066cc', fontWeight: 'bold' }}>Statistics</Link>
            </li>
          </ul>
          <select value={lang} onChange={e => setLang(e.target.value as any)}>
            <option value="en">English</option>
            <option value="zh-TW">繁體中文</option>
            <option value="zh-CN">简体中文</option>
            <option value="ja">日本語</option>
          </select>
        </nav>

        <main>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/library" element={<ChartLibrary />} />
            <Route path="/stats" element={<Statistics />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
