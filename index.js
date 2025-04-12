// index.js
const express = require('express');
const { exec } = require('child_process');

const app = express();
const PORT = 3000;

// Tu usuario local de la laptop (el que corres allá)
const USUARIO_LAPTOP = 'arthur';

app.get('/asistencia/:numero', (req, res) => {
  const numero = req.params.numero;

  // Comando SSH que se conecta a la laptop vía túnel inverso
  const comando = `ssh -p 2222 ${USUARIO_LAPTOP}@localhost "python3 ~/marcar_asistencia.py ${numero}"`;

  exec(comando, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error al ejecutar SSH: ${error.message}`);
      return res.status(500).send('Error al marcar asistencia.');
    }
    if (stderr) {
      console.error(`stderr: ${stderr}`);
    }

    console.log(`stdout: ${stdout}`);
    res.send(`Asistencia marcada para el número ${numero}`);
  });
});

app.listen(PORT, () => {
  console.log(`Servidor escuchando en http://0.0.0.0:${PORT}`);
});
