import React from 'react';
export const SearchResult = (props) => {
    return (
        <div>
            <div dangerouslySetInnerHTML={{ __html: props.content }} />
        </div>
    );
}