// Update app.js
let debateState = {
    currentRound: 0,
    maxRounds: 3,
    currentSpeaker: null,
    isDebateActive: false
};
let socket = null; 

function startDebate() {
    const motion = document.getElementById('motion').value;
    document.getElementById('startButton').disabled = true;
    
    if (socket) {
        socket.close();
    }

    socket = new WebSocket(`ws://localhost:8000/api/v1/debate/live`);
    
    socket.onopen = () => {
        console.log("WebSocket connected!");
        debateState.isDebateActive = true;
        debateState.currentRound = 1;
        updateInterface();
        
        // Clear previous debate logs
        document.getElementById('proponentLog').innerHTML = '';
        document.getElementById('opponentLog').innerHTML = '';
        
        socket.send(JSON.stringify({
            type: "start_debate",
            motion: motion,
            round: debateState.currentRound
        }));
    };
    
    socket.onerror = (error) => {
        console.error("WebSocket error:", error);
        alert("Connection error occurred");
    };
    
    socket.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            console.log("Message received:", data);
            
            if (data.type === "error") {
                console.error("Server error:", data.content);
                alert("Error: " + data.content);
                return;
            }
            
            handleDebateMessage(data);
        } catch (error) {
            console.error("Error processing message:", error);
        }
    };
}

function handleDebateMessage(data) {
    if (!data || !data.type) {
        console.error("Invalid message format:", data);
        return;
    }
    
    console.log("Processing message:", data);
    switch(data.type) {
        case 'argument':
            if (data.content && data.role) {
                addArgument(data);
                updateTurnIndicator(data.role);
                if (data.role === 'opponent') {
                    showNextRoundButton();
                }
            } else {
                console.error("Invalid argument data:", data);
            }
            break;
            
        case 'fact_check':
            const factCheckDiv = document.getElementById('factCheckResults');
            factCheckDiv.innerHTML += `<div class="fact-check">${data.content}</div>`;
            break;
            
        case 'round_complete':
            debateState.currentRound++;
            if (debateState.currentRound > debateState.maxRounds) {
                endDebate();
            }
            updateInterface();
            break;
    }
}

function sanitizeResponse(text) {
    //many time comments were added
    return text.replace(/``````/g, '').replace(/#.*/g, '').trim();
}

function addArgument(data) {
    const logElement = data.role === 'proponent' ? 
        document.getElementById('proponentLog') : 
        document.getElementById('opponentLog');
    
    const argumentDiv = document.createElement('div');
    argumentDiv.className = `argument ${data.role}`;
    argumentDiv.innerHTML = `
        <div class="argument-header">Round ${debateState.currentRound}</div>
        <div class="argument-content">${sanitizeResponse(data.content)}</div>
    `;
    
    logElement.appendChild(argumentDiv);
    logElement.scrollTop = logElement.scrollHeight;
}

function updateInterface() {
    try {
        document.getElementById('currentRound').textContent = debateState.currentRound;
        document.getElementById('startButton').disabled = debateState.isDebateActive;
        updateProgressBar();
        document.getElementById('nextRoundButton').style.display = debateState.isDebateActive && debateState.currentRound < debateState.maxRounds ? 'inline-block' : 'none';
    } catch (error) {
        console.error('Error updating interface:', error);
    }
}


function updateTurnIndicator(speaker) {
    document.getElementById('currentSpeaker').textContent = speaker.toUpperCase();
}

function endDebate() {
    debateState.isDebateActive = false;
    document.getElementById('startButton').disabled = false;
    alert('Debate completed!');
}
function startNextRound() {
    if (debateState.currentRound < debateState.maxRounds) {
        debateState.currentRound++;
        updateInterface();
        
        socket.send(JSON.stringify({
            type: "next_round",
            round: debateState.currentRound
        }));
        
        document.getElementById('nextRoundButton').style.display = 'none';
    } else {
        endDebate();
    }
}

function showNextRoundButton() {
    if (debateState.currentRound < debateState.maxRounds) {
        document.getElementById('nextRoundButton').style.display = 'inline-block';
    }
}

function updateProgressBar() {
    const progress = (debateState.currentRound / debateState.maxRounds) * 100;
    document.getElementById('debateProgress').style.width = `${progress}%`;
}