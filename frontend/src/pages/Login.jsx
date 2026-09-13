import React, { useState } from 'react';
import { Container, Paper, TextField, Button, Typography, Box } from '@mui/material';
import API from '../api/axios';
import { useNavigate } from 'react-router-dom';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      // Вариант 2: отправка чистого JSON
      const res = await API.post('/auth/token', {
        username: username,
        password: password,
      });

      localStorage.setItem('token', res.data.access_token);
      navigate('/tasks');
    } catch (err) {
      console.error('Детали ошибки:', err.response?.data);
      alert(`Ошибка: ${JSON.stringify(err.response?.data?.detail || 'Неверный логин или пароль')}`);
    }
  };

  return (
    <Container maxWidth="xs" sx={{ mt: 8 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h5" align="center" gutterBottom>
          Вход в Task Manager
        </Typography>
        <Box component="form" onSubmit={handleLogin} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField 
            label="Логин" 
            value={username} 
            onChange={(e) => setUsername(e.target.value)} 
            required 
          />
          <TextField 
            label="Пароль" 
            type="password" 
            value={password} 
            onChange={(e) => setPassword(e.target.value)} 
            required 
          />
          <Button type="submit" variant="contained" size="large">
            Войти
          </Button>
        </Box>
      </Paper>
    </Container>
  );
}