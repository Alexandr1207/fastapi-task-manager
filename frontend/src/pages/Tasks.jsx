import React, { useEffect, useState } from 'react';
import { Container, Typography, TextField, Button, List, ListItem, ListItemText, IconButton, Paper, Box, Checkbox } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import API from '../api/axios';

export default function Tasks() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');

  const fetchTasks = async () => {
    try {
      const res = await API.get('/tasks/');
      setTasks(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    if (!title.trim()) return;
    await API.post('/tasks/', { title, description, is_completed: false });
    setTitle('');
    setDescription('');
    fetchTasks();
  };

  const handleDelete = async (id) => {
    await API.delete(`/tasks/${id}`);
    fetchTasks();
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom align="center">Список задач</Typography>
      <Paper sx={{ p: 3, mb: 4 }}>
        <Box component="form" onSubmit={handleCreate} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField label="Заголовок задачи" value={title} onChange={(e) => setTitle(e.target.value)} required />
          <TextField label="Описание" value={description} onChange={(e) => setDescription(e.target.value)} multiline rows={2} />
          <Button type="submit" variant="contained">Добавить задачу</Button>
        </Box>
      </Paper>
      <Paper>
        <List>
          {tasks.map((task) => (
            <ListItem key={task.id} secondaryAction={
              <IconButton edge="end" color="error" onClick={() => handleDelete(task.id)}>
                <DeleteIcon />
              </IconButton>
            }>
              <Checkbox checked={task.is_completed || false} />
              <ListItemText primary={task.title} secondary={task.description} />
            </ListItem>
          ))}
        </List>
      </Paper>
    </Container>
  );
}