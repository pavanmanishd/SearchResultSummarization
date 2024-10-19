import React from 'react';
import '../../index.css';


export const Metrics = ({metrics}) => {
    return (
        <div className="metrics">
            <h2>Metrics</h2>
            <div className="metric">
                <h3>Compression Ratio</h3>
                <p>{metrics.compression_ratio}</p>
            </div>
            <div className="metric">
                <h3>Precision</h3>
                <p>{metrics.precision}</p>
            </div>
            <div className="metric">
                <h3>Recall</h3>
                <p>{metrics.recall}</p>
            </div>
            <div className="metric">
                <h3>F1 Score</h3>
                <p>{metrics.f1_score}</p>
            </div>
            <div className="metric">
                <h3>Cosine Similarity</h3>
                <p>{metrics.cosine_similarity}</p>
            </div>
        </div>
    );
}