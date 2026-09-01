import React, { useState, useEffect } from 'react';

const ChartLibrary: React.FC = () => {
    const [savedCharts, setSavedCharts] = useState<any[]>([]);
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        // Load from LocalStorage
        const charts = localStorage.getItem('saved_charts');
        if (charts) {
            setSavedCharts(JSON.parse(charts));
        }
    }, []);

    const exportToJSON = (chart: any) => {
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(chart, null, 2));
        const downloadAnchorNode = document.createElement('a');
        downloadAnchorNode.setAttribute("href", dataStr);
        downloadAnchorNode.setAttribute("download", `chart_${chart.id || new Date().getTime()}.json`);
        document.body.appendChild(downloadAnchorNode);
        downloadAnchorNode.click();
        downloadAnchorNode.remove();
    };

    const exportToHTML = (chart: any) => {
        const htmlContent = `
        <!DOCTYPE html>
        <html>
        <head><title>Chart Poster</title></head>
        <body style="font-family: sans-serif; padding: 2rem;">
            <h1>${chart.name || chart.chartId || 'Chart Poster'}</h1>
            <p>Generated: ${new Date(chart.timestamp).toLocaleString()}</p>
            <pre>${JSON.stringify(chart.palaces, null, 2)}</pre>
        </body>
        </html>`;
        const dataStr = "data:text/html;charset=utf-8," + encodeURIComponent(htmlContent);
        const downloadAnchorNode = document.createElement('a');
        downloadAnchorNode.setAttribute("href", dataStr);
        downloadAnchorNode.setAttribute("download", `chart_poster_${chart.id || new Date().getTime()}.html`);
        document.body.appendChild(downloadAnchorNode);
        downloadAnchorNode.click();
        downloadAnchorNode.remove();
    };

    const filteredCharts = savedCharts.filter(c =>
        (c.name && c.name.includes(searchTerm)) ||
        (c.chartId && c.chartId.includes(searchTerm))
    );

    return (
        <div>
            <h1>Chart Library</h1>
            <div style={{ marginBottom: '1rem' }}>
                <input
                    type="text"
                    placeholder="Search saved charts..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    style={{ padding: '0.5rem', width: '300px' }}
                />
            </div>

            {savedCharts.length === 0 ? (
                <p>No charts saved yet. Generate one in the Dashboard and save it.</p>
            ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                    {filteredCharts.map((chart, idx) => (
                        <div key={idx} style={{ padding: '1rem', border: '1px solid #ccc', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <div>
                                <h3>{chart.name || chart.chartId || `Chart ${idx + 1}`}</h3>
                                <p>Generated on: {new Date(chart.timestamp).toLocaleString()}</p>
                            </div>
                            <div style={{ display: 'flex', gap: '0.5rem' }}>
                                <button onClick={() => exportToJSON(chart)}>Export JSON</button>
                                <button onClick={() => exportToHTML(chart)}>Export HTML Poster</button>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default ChartLibrary;
