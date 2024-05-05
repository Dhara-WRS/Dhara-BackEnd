const express = require('express');
const multer = require('multer');
const { spawn } = require('child_process');
const fs = require('fs');

const app = express();
const upload = multer({ dest: 'uploads/' });

// Define the Python script path
const pythonScriptPath = './vision.py';

// Define the `/upload` endpoint to receive the image
app.post('/upload', upload.single('image'), async (req, res) => {
    // Print statement for debugging
    console.log('Received a request at /upload');

    // Check if an image file was uploaded
    if (!req.file) {
        console.log('No image file uploaded');
        return res.status(400).send('No image file uploaded');
    }

    // Get the image path
    const imagePath = req.file.path;
    console.log('Image file uploaded at:', imagePath);

    try {
        // Run the Python script with the image path as an argument
        console.log('Running Python script:', pythonScriptPath);
        const pythonProcess = spawn('python3', [pythonScriptPath, imagePath]);

        // Variable to hold the output from the Python script
        let pythonOutput = '';

        // Capture the output of the Python script
        pythonProcess.stdout.on('data', (data) => {
            pythonOutput += data.toString();
            console.log('Received data from Python script:', pythonOutput);
        });

        // Handle the Python script completion
        pythonProcess.on('close', (code) => {
            console.log('Python script exited with code:', code);

            if (code !== 0) {
                console.error('Python script encountered an error');
                // Delete the image file
                fs.unlink(imagePath, (err) => {
                    if (err) {
                        console.error('Error deleting image file:', err);
                    }
                });
                return res.status(500).send('Error processing image');
            }

            // Send the Python script's output back to the client
            console.log('Sending Python script output to the client:', pythonOutput);
            
            // Delete the image file
            fs.unlink(imagePath, (err) => {
                if (err) {
                    console.error('Error deleting image file:', err);
                } else {
                    console.log('Image file deleted:', imagePath);
                }
            });

            res.status(200).send(pythonOutput);
        });

    } catch (error) {
        console.error('Error running Python script:', error);
        // Delete the image file
        fs.unlink(imagePath, (err) => {
            if (err) {
                console.error('Error deleting image file:', err);
            }
        });
        res.status(500).send('Error processing image');
    }
});

// Start the server on port 5000
const PORT = 5000;
app.listen(PORT, () => {
    console.log(`Express server is running on http://localhost:${PORT}`);
});
