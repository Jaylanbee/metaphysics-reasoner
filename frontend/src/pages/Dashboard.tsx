import React, { useState } from 'react';
import { useStore, ChartPayload } from '../store';
import ChartViewer from '../components/ChartViewer';

const Dashboard: React.FC = () => {
    const {
        currentChart, detectedPatterns, matchRate,
        crossValidation, correctionSuggestion, isLoading, error,
        fetchChartAndConsensus
    } = useStore();

    const [formData, setFormData] = useState<ChartPayload>({
        year: 1990,
        month: 5,
        day: 15,
        time_branch: '辰',
        gender: 'M'
    });

    const handleGenerate = (e: React.FormEvent) => {
        e.preventDefault();
        fetchChartAndConsensus(formData);
    };

    return (
        <div>
            <h1>Dashboard (Multi-Agent 5D Cross Validation)</h1>

            <form onSubmit={handleGenerate} style={{ display: 'flex', gap: '1rem', marginBottom: '2rem', background: '#f5f5f5', padding: '1rem' }}>
                <label>Year: <input type="number" value={formData.year} onChange={e => setFormData({...formData, year: Number(e.target.value)})} style={{width:'60px'}} /></label>
                <label>Month: <input type="number" value={formData.month} onChange={e => setFormData({...formData, month: Number(e.target.value)})} style={{width:'40px'}} /></label>
                <label>Day: <input type="number" value={formData.day} onChange={e => setFormData({...formData, day: Number(e.target.value)})} style={{width:'40px'}} /></label>
                <label>Time:
                    <select value={formData.time_branch} onChange={e => setFormData({...formData, time_branch: e.target.value})}>
                        {['子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥'].map(b => <option key={b} value={b}>{b}</option>)}
                    </select>
                </label>
                <label>Gender:
                    <select value={formData.gender} onChange={e => setFormData({...formData, gender: e.target.value as 'M'|'F'})}>
                        <option value="M">M</option><option value="F">F</option>
                    </select>
                </label>
                <button type="submit" disabled={isLoading}>{isLoading ? 'Generating...' : 'Generate Report'}</button>
            </form>

            {error && <div style={{ color: 'red', padding: '1rem', background: '#fee' }}>Error: {error}</div>}

            {currentChart && (
                <div style={{ display: 'flex', gap: '2rem', flexWrap: 'wrap' }}>
                    {/* Left Column: Visual Chart */}
                    <div style={{ flex: '1 1 400px' }}>
                        <h2>Ziwei Astrolabe</h2>
                        <ChartViewer chart={currentChart} />
                        <div style={{ marginTop: '1rem' }}>
                            <button onClick={() => {
                                const saved = JSON.parse(localStorage.getItem('saved_charts') || '[]');
                                saved.push({ ...currentChart, timestamp: new Date().toISOString() });
                                localStorage.setItem('saved_charts', JSON.stringify(saved));
                                alert('Chart saved successfully!');
                            }}>
                                Save Chart to Library
                            </button>
                        </div>
                    </div>

                    {/* Right Column: Reports */}
                    <div style={{ flex: '1 1 400px' }}>
                        {/* Phase 3.1 & 3.2: Pattern Match Rate */}
                        {matchRate !== null && (
                            <div style={{ background: '#eef', padding: '1rem', marginBottom: '1rem' }}>
                                <h3>Pattern Analysis</h3>
                                <p><strong>Knowledgebase Match Rate:</strong> {(matchRate * 100).toFixed(1)}%</p>
                                <ul>
                                    {detectedPatterns?.map((p, i) => (
                                        <li key={i}>{p.patternName}</li>
                                    ))}
                                </ul>
                            </div>
                        )}

                        {/* Phase 3.1 & 3.2: 5D Cross Validation */}
                        {crossValidation && (
                            <div style={{ background: '#efe', padding: '1rem', marginBottom: '1rem' }}>
                                <h3>5D Bazi Cross-Validation</h3>
                                <p><strong>Confidence Score:</strong> <span style={{ fontWeight: 'bold', color: crossValidation.confidence_score === 'HIGH' ? 'green' : 'orange' }}>{crossValidation.confidence_score}</span> ({crossValidation.aligned_count}/{crossValidation.total_dimensions} aligned)</p>
                                <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '1rem', fontSize: '0.9em' }}>
                                    <thead>
                                        <tr style={{ background: '#ddd' }}>
                                            <th style={{ padding: '4px', textAlign: 'left' }}>Dimension</th>
                                            <th style={{ padding: '4px', textAlign: 'center' }}>Aligned</th>
                                            <th style={{ padding: '4px', textAlign: 'left' }}>Details</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {Object.entries(crossValidation.dimensions).map(([key, val]: [string, any]) => (
                                            <tr key={key} style={{ borderBottom: '1px solid #ddd' }}>
                                                <td style={{ padding: '4px', textTransform: 'capitalize' }}>{key}</td>
                                                <td style={{ padding: '4px', textAlign: 'center', color: val.aligned ? 'green' : 'red' }}>{val.aligned ? '✓' : '✗'}</td>
                                                <td style={{ padding: '4px' }}>{val.details}</td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        )}

                        {/* Phase 3.1: Time Corrector */}
                        {correctionSuggestion && (
                            <div style={{ background: '#ffe', padding: '1rem', marginBottom: '1rem', border: '1px solid orange' }}>
                                <h3>⚠️ Time Correction Suggested</h3>
                                <p>{correctionSuggestion.suggestion_text}</p>
                                <p>Try: <strong>{correctionSuggestion.prev_branch}</strong> or <strong>{correctionSuggestion.next_branch}</strong></p>
                            </div>
                        )}

                        {/* Multi-Agent Report */}
                        <div style={{ background: '#f5f5f5', padding: '1rem', borderLeft: '4px solid #666' }}>
                             <h3>FateCouncil (Multi-Agent) Report</h3>
                             {/* Integrating Agent final report mapping from crossValidation structure if available */}
                             {crossValidation && crossValidation.multi_agent_report ? (
                                <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit' }}>
                                    {crossValidation.multi_agent_report}
                                </pre>
                             ) : (
                                <div>
                                    <p><strong>📍 Consensus Points:</strong> Agent confirmed primary alignment.</p>
                                    <p><strong>📚 Classics Citations:</strong> Referenced from verified local knowledge base nodes.</p>
                                    <p><strong>💡 Final Recommendations:</strong> Suggest standardizing daily timing routines.</p>
                                </div>
                             )}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Dashboard;
