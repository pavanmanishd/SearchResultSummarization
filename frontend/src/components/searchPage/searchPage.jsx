import React, { useState } from 'react';
import { SearchResult } from '../searchResult/searchResult';
import { LlmSelectList } from '../llmSelectList/llmSelectList';
import { llmOptions } from '../../constants';
import { Metrics } from '../Metrics/metrics';
import './styles.css';

export const SearchPage = () => {
    const [query, setQuery] = useState('');
    const [searchResponse, setSearchResponse] = useState('');
    const [loading, setLoading] = useState(false);
    const [selectedLlm, setSelectedLlm] = useState(llmOptions[0]);
    const [errorMessage, setErrorMessage] = useState('');
    const [metrics, setMetrics] = useState({});

    const handleChange = (event) => {
        setQuery(event.target.value);
        if (event.target.value.trim() !== '') {
            setErrorMessage('');
        }
    }

    const handleSubmit = () => {
        if (query.trim() === '') {
            setErrorMessage('Please enter a query');
            return;
        }
        setLoading(true);
        const api = 'http://localhost:8000/summarize';
        const body = {
            query: query,
            llm: selectedLlm
        };
        fetch(api, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body)
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            setSearchResponse(data.summary);
            setMetrics(data.metrics);
            setLoading(false);
        })
        .catch((error) => {
            console.error('Error:', error);
            setLoading(false);
        });
    }

    return (
        <div className='search-results-and-metrics'>
            <div className="search-page">
                <div className="search-inputs">
                    <input
                        type="text"
                        className="query-input"
                        placeholder="Enter your query"
                        value={query}
                        onChange={handleChange}
                    />
                    <p id="errorMessage" className='error-message'>{errorMessage}</p>
                    <div className="button-group">
                        <button className="search-btn" onClick={handleSubmit}>Search</button>
                        <button className="clear-btn" onClick={() => setQuery('')}>Clear</button>
                        <button className="clear-result-btn" onClick={() => setSearchResponse('')}>Clear Result</button>
                        <LlmSelectList selected={selectedLlm} setSelected={setSelectedLlm} options={llmOptions}/>
                    </div>
                </div>
                {loading ? (
                    <div className="loading-screen">Loading...</div>
                ) : (
                    <SearchResult content={searchResponse} />
                )}
            </div>
            <div>
                <Metrics metrics={metrics} />
            </div>
        </div>
    );
}