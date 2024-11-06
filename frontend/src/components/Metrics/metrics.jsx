import React from 'react';
import './styles.css';

export const Metrics = ({ metrics }) => {
    if(metrics.precision) {
        return (
            <div>
                <div className="metrics">
                    <h2 className="metrics-title">Metrics</h2>
                    <table className="metrics-table">
                        <thead>
                            <tr className="metrics-table-header">
                                <th className="metrics-table-cell">Metric</th>
                                <th className="metrics-table-cell">Value</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr className="metrics-table-row">
                                <td className="metrics-table-cell">Compression Ratio</td>
                                <td className="metrics-table-cell">{metrics.compression_ratio*100}%</td>
                            </tr>
                            <tr className="metrics-table-row">
                                <td className="metrics-table-cell">Precision</td>
                                <td className="metrics-table-cell">{metrics.precision}</td>
                            </tr>
                            <tr className="metrics-table-row">
                                <td className="metrics-table-cell">Cosine Similarity</td>
                                <td className="metrics-table-cell">{metrics.cosine_similarity}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                    <p>* This is calculated by comparing the summary with data on the internet.</p>
            </div>
        );
    } else {
        return (
            <div></div>
        )
    }
}
