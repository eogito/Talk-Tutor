let record;
let audioChunks = [];
const startButton = document.getElementById('start');
const stopButton = document.getElementById('stop1');

async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    record = new MediaRecorder(stream);

    record.ondataavailable = (event) => {
        if (event.data.size > 0) {
            audioChunks.push(event.data);
        }
    };

    record.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const audioUrl = URL.createObjectURL(audioBlob);

        const downloadLink = document.createElement('a');
        downloadLink.href = audioUrl;
        downloadLink.download = 'recording.wav';
        downloadLink.style.display = 'none';
        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
        runPythonScript();
    };

    record.start();
}

function stopRecording() {
    record.stop();
}
async function runPythonScript() {
    try {
        const response = await fetch('/run', {
            method: 'POST',
        });

        if (response.ok) {
            const data = await response.json();
            console.log(data.output);
        } else {
            console.error('Error:', response.statusText);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

start.addEventListener('click', startRecording);
stop1.addEventListener('click', stopRecording);
