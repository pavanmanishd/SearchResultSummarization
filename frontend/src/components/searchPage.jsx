import React from 'react';
import { SearchResult } from './searchResult';
import { useState } from 'react';

export const SearchPage = () => {
    const [query, setQuery] = useState('');
    const [searchResposnse, setSearchResponse] = useState('');

    const handleChange = (event) => {
        setQuery(event.target.value);
    }

    const handleSubmit = (event) => {
        const api = 'http://localhost:8000/summarize';
        const body = {
            query: query 
        }
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
        })
        .catch((error) => {
            console.error('Error:', error);
        }
        );
    }

    return (
        <div>
        <input type="text" placeholder="enter your query" value={query} onChange={handleChange}/>
        <button onClick={handleSubmit}>Search</button>
        <SearchResult 
            content={searchResposnse}
        />
        </div>
    );
    }