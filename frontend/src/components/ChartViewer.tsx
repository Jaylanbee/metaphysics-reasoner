import React from 'react';
import { ZiweiChart } from '../store';

interface ChartViewerProps {
    chart: ZiweiChart;
}

const BRANCH_GRID_MAP: Record<string, { x: number, y: number }> = {
    '巳': { x: 0, y: 0 }, '午': { x: 1, y: 0 }, '未': { x: 2, y: 0 }, '申': { x: 3, y: 0 },
    '辰': { x: 0, y: 1 },                                           '酉': { x: 3, y: 1 },
    '卯': { x: 0, y: 2 },                                           '戌': { x: 3, y: 2 },
    '寅': { x: 0, y: 3 }, '丑': { x: 1, y: 3 }, '子': { x: 2, y: 3 }, '亥': { x: 3, y: 3 }
};

const ChartViewer: React.FC<ChartViewerProps> = ({ chart }) => {
    return (
        <svg viewBox="0 0 800 800" style={{ width: '100%', height: 'auto', border: '2px solid #333', backgroundColor: '#f9f9f9' }}>
            <defs>
                <style>
                    {`
                        .palace-rect { fill: #fff; stroke: #ccc; stroke-width: 1; }
                        .title-text { font-family: sans-serif; font-weight: bold; font-size: 14px; fill: #333; }
                        .major-star { font-family: sans-serif; font-size: 14px; fill: #c00; font-weight: bold; }
                        .minor-star { font-family: sans-serif; font-size: 12px; fill: #666; }
                        .transformation { font-family: sans-serif; font-size: 12px; fill: #fff; font-weight: bold; }
                        .trans-bg-lu { fill: #2e8b57; }
                        .trans-bg-quan { fill: #4682b4; }
                        .trans-bg-ke { fill: #daa520; }
                        .trans-bg-ji { fill: #b22222; }
                    `}
                </style>
            </defs>

            {/* Render 12 Palaces */}
            {chart.palaces && Array.isArray(chart.palaces) && chart.palaces.map((p: any, idx) => {
                const isDict = typeof p === 'object' && p !== null;
                const name = isDict ? p.name : '未知';
                const earthlyBranch = isDict ? p.earthlyBranch || p.position : '未知';
                const majorStars = isDict ? (p.majorStars || p.stars || []) : [];
                const minorStars = isDict ? (p.minorStars || []) : [];

                const coords = BRANCH_GRID_MAP[earthlyBranch as string];
                if (!coords) return null;

                const cellWidth = 200;
                const cellHeight = 200;
                const x = coords.x * cellWidth;
                const y = coords.y * cellHeight;

                return (
                    <g key={idx} transform={`translate(${x}, ${y})`}>
                        <rect width={cellWidth} height={cellHeight} className="palace-rect" />

                        {/* Title and Earthly Branch */}
                        <text x={cellWidth - 10} y={cellHeight - 10} textAnchor="end" className="title-text">
                            {name}
                        </text>
                        <text x={10} y={cellHeight - 10} textAnchor="start" className="title-text" style={{fill: '#999'}}>
                            {earthlyBranch}
                        </text>

                        {/* Major Stars rendering */}
                        {majorStars.map((s: any, i: number) => {
                            const starName = typeof s === 'string' ? s : s.name;
                            const transformation = typeof s === 'object' && s.transformation ? s.transformation : null;
                            const yOffset = 25 + i * 20;

                            return (
                                <g key={`major-${i}`}>
                                    <text x={10} y={yOffset} className="major-star">{starName}</text>
                                    {transformation && (
                                        <g transform={`translate(${50}, ${yOffset - 12})`}>
                                            <rect width="18" height="16" rx="4" className={
                                                transformation === '祿' ? 'trans-bg-lu' :
                                                transformation === '權' ? 'trans-bg-quan' :
                                                transformation === '科' ? 'trans-bg-ke' :
                                                'trans-bg-ji'
                                            } />
                                            <text x="9" y="12" textAnchor="middle" className="transformation">{transformation}</text>
                                        </g>
                                    )}
                                </g>
                            );
                        })}

                        {/* Minor Stars rendering */}
                        {minorStars.map((s: any, i: number) => {
                            const starName = typeof s === 'string' ? s : s.name;
                            const yOffset = 25 + i * 16;
                            return (
                                <text key={`minor-${i}`} x={cellWidth - 10} y={yOffset} textAnchor="end" className="minor-star">{starName}</text>
                            );
                        })}
                    </g>
                );
            })}

            {/* Center Area */}
            <g transform="translate(200, 200)">
                <rect width="400" height="400" fill="#fdfdfd" stroke="#ccc" strokeDasharray="5,5" />
                <text x="200" y="200" textAnchor="middle" dominantBaseline="middle" style={{fontSize: '24px', fill: '#666'}}>
                    天盤可視化 (SVG)
                </text>
            </g>
        </svg>
    );
};

export default ChartViewer;
