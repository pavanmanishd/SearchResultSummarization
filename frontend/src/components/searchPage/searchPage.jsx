import React, { useState } from 'react';
import { SearchResult } from '../searchResult/searchResult';
import './styles.css'; // Assuming you import the styles from an external file

export const SearchPage = () => {
    const [query, setQuery] = useState('');
    const [searchResponse, setSearchResponse] = useState('');
    const [loading, setLoading] = useState(false);

    const handleChange = (event) => {
        setQuery(event.target.value);
    }

    const handleSubmit = () => {
        setLoading(true);
        const api = 'http://localhost:8000/summarize';
        const body = {
            query: query 
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
            setSearchResponse(data.summary);
            setLoading(false);
        })
        .catch((error) => {
            console.error('Error:', error);
            setLoading(false);
        });
    }

    return (
        <div className="search-page">
            <div className="search-inputs">
                <input 
                    type="text" 
                    className="query-input"
                    placeholder="Enter your query" 
                    value={query} 
                    onChange={handleChange} 
                />
                <div className="button-group">
                    <button className="search-btn" onClick={handleSubmit}>Search</button>
                    <button className="clear-btn" onClick={() => setQuery('')}>Clear</button>
                    <button className="clear-result-btn" onClick={() => setSearchResponse('')}>Clear Result</button>
                </div>
            </div>
            {loading ? (
                <div className="loading-screen">Loading...</div>
            ) : (
                <SearchResult content={searchResponse} />
            )}
        </div>
    );
}