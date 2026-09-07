/* 
  EJAJ TECH - Proyecto 50: Sistema de Controlo de Frota SaaS Engine
  AJAX handlers & Dynamic Fleet Calculations
*/

document.addEventListener('DOMContentLoaded', () => {
  initFleetEngine();
});

function initFleetEngine() {
  // Add listeners if forms exist
  const fuelForm = document.getElementById('fuelForm');
  if (fuelForm) {
    fuelForm.addEventListener('submit', handleFuelSubmit);
  }

  const maintForm = document.getElementById('maintForm');
  if (maintForm) {
    maintForm.addEventListener('submit', handleMaintSubmit);
  }

  const vehicleForm = document.getElementById('vehicleForm');
  if (vehicleForm) {
    vehicleForm.addEventListener('submit', handleVehicleSubmit);
  }
}

async function handleVehicleSubmit(e) {
  e.preventDefault();
  const plate = document.getElementById('plate')?.value.trim();
  const brand = document.getElementById('brand')?.value.trim();
  const model = document.getElementById('model')?.value.trim();
  const category = document.getElementById('category')?.value.trim();
  const year = parseInt(document.getElementById('year')?.value || 2024);
  const fuel_type = document.getElementById('fuel_type')?.value.trim();
  const current_km = parseInt(document.getElementById('current_km')?.value || 0);
  const driver_name = document.getElementById('driver_name')?.value.trim();
  const insurance_expiry = document.getElementById('insurance_expiry')?.value.trim();
  const itv_expiry = document.getElementById('itv_expiry')?.value.trim();

  if (!plate || !brand || !model) {
    alert('Por favor preencha os campos obrigatórios (Matrícula, Marca e Modelo).');
    return;
  }

  const payload = { plate, brand, model, category, year, fuel_type, current_km, driver_name, insurance_expiry, itv_expiry };

  try {
    const res = await fetch('/api/vehicles/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const result = await res.json();
    if (result.success) {
      alert('✅ ' + result.message);
      location.reload();
    } else {
      alert('❌ Erro: ' + result.message);
    }
  } catch (err) {
    alert('❌ Erro ao comunicação com o servidor.');
  }
}

async function handleFuelSubmit(e) {
  e.preventDefault();
  const vehicle_id = parseInt(document.getElementById('vehicle_id')?.value || 0);
  const fill_date = document.getElementById('fill_date')?.value.trim();
  const liters = parseFloat(document.getElementById('liters')?.value || 0);
  const total_cost = parseFloat(document.getElementById('total_cost')?.value || 0);
  const km_at_fill = int(document.getElementById('km_at_fill')?.value || 0);

  if (!vehicle_id || liters <= 0 || total_cost <= 0 || km_at_fill <= 0) {
    alert('Por favor preencha todos os campos do abastecimento.');
    return;
  }

  const payload = { vehicle_id, fill_date, liters, total_cost, km_at_fill };

  try {
    const res = await fetch('/api/fuel/log', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const result = await res.json();
    if (result.success) {
      alert('⛽ ' + result.message);
      location.reload();
    } else {
      alert('❌ Erro: ' + result.message);
    }
  } catch (err) {
    alert('❌ Erro de comunicação.');
  }
}

async function handleMaintSubmit(e) {
  e.preventDefault();
  const vehicle_id = parseInt(document.getElementById('maint_vehicle_id')?.value || 0);
  const maint_type = document.getElementById('maint_type')?.value.trim();
  const description = document.getElementById('maint_description')?.value.trim();
  const maint_date = document.getElementById('maint_date')?.value.trim();
  const km_at_maint = parseInt(document.getElementById('km_at_maint')?.value || 0);
  const cost = parseFloat(document.getElementById('maint_cost')?.value || 0);
  const next_due_date = document.getElementById('next_due_date')?.value.trim();

  if (!vehicle_id || !maint_type || !maint_date || cost <= 0) {
    alert('Por favor preencha os dados da manutenção.');
    return;
  }

  const payload = { vehicle_id, maint_type, description, maint_date, km_at_maint, cost, next_due_date };

  try {
    const res = await fetch('/api/maintenance/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const result = await res.json();
    if (result.success) {
      alert('🛠️ ' + result.message);
      location.reload();
    } else {
      alert('❌ Erro: ' + result.message);
    }
  } catch (err) {
    alert('❌ Erro de ligação.');
  }
}

async function resolveAlert(alertId) {
  try {
    const res = await fetch('/api/alerts/resolve/' + alertId, { method: 'POST' });
    const result = await res.json();
    if (result.success) {
      location.reload();
    }
  } catch (err) {
    alert('Erro ao resolver alerta.');
  }
}
