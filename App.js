import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
    const [genre, setGenre] = useState('');
    const [theme, setTheme] = useState('');
    const [characters, setCharacters] = useState('');
    const [script, setScript] = useState('');
    const [templates, setTemplates] = useState([]);

    const generateScript = async () => {
        const response = await axios.post('/generate_script', {
            genre,
            theme,
            characters: characters.split(',').map(char => char.trim())
        });
        setScript(response.data.script);
    };

    const fetchTemplates = async () => {
        const response = await axios.get('/templates');
        setTemplates(response.data);
    };

    useEffect(() => {
        fetchTemplates();
    }, []);

    return (
        <div>
            <h1>Movie Script Generator</h1>
            <input type="text" placeholder="Genre" onChange={e =>
