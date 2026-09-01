import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Statistics: React.FC = () => {
    const [stats, setStats] = useState<any>(null);

    useEffect(() => {
        axios.get('http://localhost:8000/api/v1/statistics/summary')
            .then(res => setStats(res.data))
            .catch(console.error);
    }, []);

    if (!stats) return <div>Loading statistics...</div>;

    return (
        <div>
            <h1>Global Chart Statistics</h1>
            <p>Total Charts Analyzed: {stats.total_analyzed}</p>
            <h3>Pattern Distributions</h3>
            <ul>
                {stats.pattern_distributions.map((p: any, i: number) => (
                    <li key={i}>{p.name}: {p.value} cases</li>
                ))}
            </ul>
        </div>
    );
};
export default Statistics;
