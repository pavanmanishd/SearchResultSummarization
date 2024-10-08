import React from "react";
import './styles.css';

export const LlmSelectList = ({ options, selected, setSelected }) => {
    return (
        <div className="llm-select-list">
            <select onChange={(e) => setSelected(e.target.value)} value={selected}>
                {options.map((option, index) => (
                    <option key={index} value={option}>
                        {option}
                    </option>
                ))}
            </select>
        </div>
    );
}