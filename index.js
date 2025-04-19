const express = require('express');
const { exec } = require('child_process');
const path = require('path');
const bodyParser = require('body-parser');

const app = express();
const PORT = 3000;
const USUARIO_LAPTOP = 'arthur';

// Middleware para procesar formularios
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public')));

// Ruta principal - Landing Page
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'landing.html'));
});

// Ruta para la página de asistencia (adonde lleva el QR)
app.get('/asistencia', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'asistencia.html'));
});

// API para marcar asistencia
app.post('/api/marcar-asistencia', (req, res) => {
  const { nombre } = req.body;
  
  if (!nombre) {
    return res.status(400).json({ 
      success: false, 
      message: 'Nombre del alumno requerido' 
    });
  }

  // Aseguramos que el nombre esté correctamente escapado para la shell
  const nombreEscapado = `'${nombre.replace(/'/g, `'\\''`)}'`;
  const comando = `ssh -p 2222 ${USUARIO_LAPTOP}@localhost "python3 ~/marcar_asistencia.py marcar ${nombreEscapado}"`;
  
  exec(comando, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error al ejecutar SSH: ${error.message}`);
      return res.status(500).json({ 
        success: false, 
        message: 'Error al marcar asistencia' 
      });
    }
    
    if (stderr) {
      console.error(`stderr: ${stderr}`);
    }
    
    try {
      const resultado = JSON.parse(stdout);
      return res.json(resultado);
    } catch (e) {
      console.error(`Error al parsear la respuesta: ${e.message}`);
      return res.status(500).json({ 
        success: false, 
        message: 'Error al procesar la respuesta del servidor' 
      });
    }
  });
});


app.listen(PORT, '0.0.0.0',() => {
  console.log(`Servidor QRScan ejecutándose en puerto ${PORT}`);
});