// EJAJ TECH - FitTracker Workout Interactive JavaScript

document.addEventListener('DOMContentLoaded', () => {
    initRestTimer();
    initSetRows();
});

// Live Rest Timer Stopwatch
let timerInterval = null;
let timerSeconds = 0;

function initRestTimer() {
    const display = document.getElementById('restTimerDisplay');
    if (!display) return;

    window.startRestTimer = function(seconds) {
        clearInterval(timerInterval);
        timerSeconds = seconds;
        updateTimerDisplay();

        timerInterval = setInterval(() => {
            timerSeconds--;
            updateTimerDisplay();
            if (timerSeconds <= 0) {
                clearInterval(timerInterval);
                alert('⏱️ Tempo de descanso concluído! Hora da próxima série.');
            }
        }, 1000);
    };

    window.pauseRestTimer = function() {
        clearInterval(timerInterval);
    };

    window.resetRestTimer = function() {
        clearInterval(timerInterval);
        timerSeconds = 0;
        updateTimerDisplay();
    };

    function updateTimerDisplay() {
        const mins = Math.floor(timerSeconds / 60);
        const secs = timerSeconds % 60;
        display.innerText = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
}

// 1RM Brzycki Calculator
function calculate1RM() {
    const weight = parseFloat(document.getElementById('calcWeight')?.value || 0);
    const reps = parseInt(document.getElementById('calcReps')?.value || 0);
    const resultEl = document.getElementById('calc1RMResult');

    if (!resultEl) return;

    if (weight <= 0 || reps <= 0) {
        resultEl.innerText = '0.0 kg';
        return;
    }

    if (reps === 1) {
        resultEl.innerText = weight.toFixed(1) + ' kg';
        return;
    }

    // Brzycki formula: W * (36 / (37 - R))
    const oneRM = weight * (36 / (37 - reps));
    resultEl.innerText = oneRM.toFixed(1) + ' kg';
}

// Set Rows Builder
function initSetRows() {
    const addSetBtn = document.getElementById('btnAddSetRow');
    const tbody = document.getElementById('setRowsTableBody');

    if (addSetBtn && tbody) {
        addSetBtn.addEventListener('click', () => {
            const rowCount = tbody.querySelectorAll('tr').length + 1;
            const tr = document.createElement('tr');
            tr.className = 'set-log-row';
            tr.innerHTML = `
                <td>
                    <select class="form-control set-ex-name" required>
                        <option value="Supino Reto com Barra">Supino Reto com Barra (Peito)</option>
                        <option value="Supino Inclinado com Halteres">Supino Inclinado com Halteres (Peito)</option>
                        <option value="Agachamento Livre com Barra">Agachamento Livre com Barra (Pernas)</option>
                        <option value="Prensa de Pernas (Leg Press 45º)">Prensa de Pernas (Pernas)</option>
                        <option value="Levantamento Terra (Deadlift)">Levantamento Terra (Costas)</option>
                        <option value="Puxada à Frente na Polia (Lat Pulldown)">Puxada à Frente (Costas)</option>
                        <option value="Press Militar de Ombros">Press Militar (Ombros)</option>
                        <option value="Elevação Lateral com Halteres">Elevação Lateral (Ombros)</option>
                        <option value="Curl de Bíceps com Barra Z">Curl de Bíceps (Braços)</option>
                        <option value="Tríceps na Polia Alta com Corda">Tríceps Corda (Braços)</option>
                    </select>
                </td>
                <td><input type="number" class="form-control set-num" value="${rowCount}" min="1"></td>
                <td>
                    <select class="form-control set-type">
                        <option value="Trabalho">Trabalho</option>
                        <option value="Aquecimento">Aquecimento</option>
                        <option value="Até à Falha">Até à Falha</option>
                    </select>
                </td>
                <td><input type="number" class="form-control set-reps" value="10" min="1" onchange="recalcSessionVolume()"></td>
                <td><input type="number" class="form-control set-weight" value="60.0" step="2.5" min="0" onchange="recalcSessionVolume()"></td>
                <td style="text-align: center;"><input type="checkbox" class="set-pr" style="width: 18px; height: 18px;"></td>
                <td><button type="button" class="btn btn-danger btn-sm" onclick="removeSetRow(this)">✕</button></td>
            `;
            tbody.appendChild(tr);
            recalcSessionVolume();
        });
    }
}

function removeSetRow(btn) {
    const row = btn.closest('tr');
    row.remove();
    recalcSessionVolume();
}

function recalcSessionVolume() {
    let totalVol = 0;
    const rows = document.querySelectorAll('.set-log-row');

    rows.forEach(r => {
        const reps = parseFloat(r.querySelector('.set-reps')?.value || 0);
        const weight = parseFloat(r.querySelector('.set-weight')?.value || 0);
        totalVol += reps * weight;
    });

    const display = document.getElementById('sessionVolumeDisplay');
    if (display) {
        display.innerText = totalVol.toFixed(1) + ' kg';
    }
}

// Submit Workout Session AJAX
async function submitWorkoutLog(event) {
    event.preventDefault();
    const routineName = document.getElementById('routineNameInput').value.trim() || 'Treino Livre';
    const duration = parseInt(document.getElementById('durationInput').value || 60);
    const notes = document.getElementById('workoutNotesInput').value.trim();

    const sets = [];
    const rows = document.querySelectorAll('.set-log-row');

    rows.forEach(r => {
        const exName = r.querySelector('.set-ex-name').value;
        const setNum = parseInt(r.querySelector('.set-num').value || 1);
        const setType = r.querySelector('.set-type').value;
        const reps = parseInt(r.querySelector('.set-reps').value || 0);
        const weight = parseFloat(r.querySelector('.set-weight').value || 0);
        const isPr = r.querySelector('.set-pr').checked;

        if (exName && reps > 0) {
            sets.push({
                exercise_name: exName,
                set_number: setNum,
                set_type: setType,
                reps: reps,
                weight_kg: weight,
                is_pr: isPr
            });
        }
    });

    if (sets.length === 0) {
        alert('Por favor introduza pelo menos uma série efetuada.');
        return;
    }

    try {
        const res = await fetch('/api/workout/log', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                routine_name: routineName,
                duration_minutes: duration,
                notes: notes,
                sets: sets
            })
        });

        const data = await res.json();
        if (data.success) {
            alert(data.message);
            window.location.href = '/history';
        } else {
            alert('Erro ao registar treino: ' + data.message);
        }
    } catch (err) {
        alert('Erro de rede: ' + err.message);
    }
}

// Submit Custom Exercise AJAX
async function submitCustomExercise(event) {
    event.preventDefault();
    const name = document.getElementById('newExName').value.trim();
    const muscle = document.getElementById('newExMuscle').value;
    const equipment = document.getElementById('newExEquipment').value;
    const instructions = document.getElementById('newExInstructions').value.trim();

    try {
        const res = await fetch('/api/exercise/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: name,
                muscle_group: muscle,
                equipment: equipment,
                instructions: instructions
            })
        });

        const data = await res.json();
        if (data.success) {
            alert('Exercício adicionado!');
            window.location.reload();
        } else {
            alert('Erro: ' + data.message);
        }
    } catch (err) {
        alert('Erro: ' + err.message);
    }
}
