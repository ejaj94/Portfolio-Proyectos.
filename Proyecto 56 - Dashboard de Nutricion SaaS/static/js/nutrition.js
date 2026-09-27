// EJAJ TECH - NutriTracker Interactive JavaScript

document.addEventListener('DOMContentLoaded', () => {
    initFoodSelector();
});

// Auto calculate macros based on food selection and grams
function initFoodSelector() {
    const foodSelect = document.getElementById('foodSelectInput');
    const gramsInput = document.getElementById('gramsInput');

    if (foodSelect && gramsInput) {
        foodSelect.addEventListener('change', updateCalculatedMacros);
        gramsInput.addEventListener('input', updateCalculatedMacros);
    }
}

function updateCalculatedMacros() {
    const foodSelect = document.getElementById('foodSelectInput');
    const gramsInput = document.getElementById('gramsInput');
    const calcNotice = document.getElementById('calcMacroNotice');

    if (!foodSelect || !gramsInput || !calcNotice) return;

    const selectedOpt = foodSelect.options[foodSelect.selectedIndex];
    if (!selectedOpt || !selectedOpt.dataset.cal) {
        calcNotice.innerText = 'Selecione um alimento para ver a estimativa.';
        return;
    }

    const cal100 = parseFloat(selectedOpt.dataset.cal || 0);
    const prot100 = parseFloat(selectedOpt.dataset.prot || 0);
    const carbs100 = parseFloat(selectedOpt.dataset.carbs || 0);
    const fat100 = parseFloat(selectedOpt.dataset.fat || 0);

    const grams = parseFloat(gramsInput.value || 0);
    const mult = grams / 100.0;

    const estCal = (cal100 * mult).toFixed(1);
    const estProt = (prot100 * mult).toFixed(1);
    const estCarbs = (carbs100 * mult).toFixed(1);
    const estFat = (fat100 * mult).toFixed(1);

    calcNotice.innerHTML = `<strong>Estimativa para ${grams}g:</strong> ${estCal} kcal | Proteína: ${estProt}g | Hidratos: ${estCarbs}g | Gorduras: ${estFat}g`;
}

// Submit Meal Log AJAX
async function submitMealLog(event) {
    event.preventDefault();
    const logDate = document.getElementById('logDateInput').value;
    const mealType = document.getElementById('mealTypeInput').value;
    const foodName = document.getElementById('foodSelectInput').value;
    const quantityG = parseFloat(document.getElementById('gramsInput').value || 100);

    try {
        const res = await fetch('/api/log/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                log_date: logDate,
                meal_type: mealType,
                food_name: foodName,
                quantity_g: quantityG
            })
        });

        const data = await res.json();
        if (data.success) {
            alert('✅ ' + data.message);
            window.location.href = '/';
        } else {
            alert('❌ Erro: ' + data.message);
        }
    } catch (err) {
        alert('Erro de rede: ' + err.message);
    }
}

// Delete Log Entry AJAX
async function deleteMealLog(logId) {
    if (!confirm('Deseja eliminar este registo de refeição?')) return;

    try {
        const res = await fetch(`/api/log/delete/${logId}`, {
            method: 'POST'
        });

        const data = await res.json();
        if (data.success) {
            alert('🗑️ ' + data.message);
            window.location.reload();
        } else {
            alert('Erro: ' + data.message);
        }
    } catch (err) {
        alert('Erro de rede: ' + err.message);
    }
}

// Submit Custom Food AJAX
async function submitCustomFood(event) {
    event.preventDefault();
    const name = document.getElementById('foodNameInput').value.trim();
    const category = document.getElementById('foodCatInput').value;
    const calories = parseFloat(document.getElementById('foodCalInput').value || 0);
    const protein = parseFloat(document.getElementById('foodProtInput').value || 0);
    const carbs = parseFloat(document.getElementById('foodCarbsInput').value || 0);
    const fat = parseFloat(document.getElementById('foodFatInput').value || 0);
    const fiber = parseFloat(document.getElementById('foodFiberInput').value || 0);

    try {
        const res = await fetch('/api/food/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: name,
                category: category,
                calories_100g: calories,
                protein_g: protein,
                carbs_g: carbs,
                fat_g: fat,
                fiber_g: fiber
            })
        });

        const data = await res.json();
        if (data.success) {
            alert('🥗 ' + data.message);
            window.location.reload();
        } else {
            alert('Erro: ' + data.message);
        }
    } catch (err) {
        alert('Erro de rede: ' + err.message);
    }
}

// Update Goals AJAX
async function submitUpdateGoals(event) {
    event.preventDefault();
    const name = document.getElementById('userNameInput').value.trim();
    const cal = parseFloat(document.getElementById('targetCalInput').value || 2200);
    const prot = parseFloat(document.getElementById('targetProtInput').value || 160);
    const carbs = parseFloat(document.getElementById('targetCarbsInput').value || 220);
    const fat = parseFloat(document.getElementById('targetFatInput').value || 60);

    try {
        const res = await fetch('/api/goals/update', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_name: name,
                target_calories: cal,
                target_protein_g: prot,
                target_carbs_g: carbs,
                target_fat_g: fat
            })
        });

        const data = await res.json();
        if (data.success) {
            alert('🎯 ' + data.message);
            window.location.href = '/';
        } else {
            alert('Erro: ' + data.message);
        }
    } catch (err) {
        alert('Erro de rede: ' + err.message);
    }
}

// TDEE / Macro Calculator Helper
function calculateTDEE() {
    const weight = parseFloat(document.getElementById('calcWeight')?.value || 75);
    const goal = document.getElementById('calcGoal')?.value || 'maintenance';
    
    let baseCal = weight * 30; // Rough TDEE estimate
    if (goal === 'cut') baseCal -= 400;
    if (goal === 'bulk') baseCal += 400;

    const prot = Math.round(weight * 2.0); // 2g/kg
    const fat = Math.round(weight * 0.8); // 0.8g/kg
    const remCal = baseCal - (prot * 4 + fat * 9);
    const carbs = Math.max(50, Math.round(remCal / 4));

    document.getElementById('targetCalInput').value = Math.round(baseCal);
    document.getElementById('targetProtInput').value = prot;
    document.getElementById('targetCarbsInput').value = carbs;
    document.getElementById('targetFatInput').value = fat;
}
