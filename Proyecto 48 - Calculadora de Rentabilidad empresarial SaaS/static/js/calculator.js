/* 
  EJAJ TECH - Proyecto 48: Calculadora de Rentabilidade empresarial SaaS Engine
  Real-time calculation & Chart.js rendering
*/

let breakEvenChart = null;

document.addEventListener('DOMContentLoaded', () => {
  initCalculator();
});

function initCalculator() {
  const inputs = [
    'product_cost', 'labor_hours', 'labor_rate', 
    'overhead_cost', 'monthly_fixed_costs', 'vat_rate', 'selling_price'
  ];

  inputs.forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener('input', recalculate);
    }
  });

  // Init chart canvas if present
  const ctx = document.getElementById('breakevenChart');
  if (ctx) {
    initChart(ctx);
  }

  // Initial Calculation
  recalculate();
}

function recalculate() {
  const product_cost = parseFloat(document.getElementById('product_cost')?.value || 0);
  const labor_hours = parseFloat(document.getElementById('labor_hours')?.value || 0);
  const labor_rate = parseFloat(document.getElementById('labor_rate')?.value || 0);
  const overhead_cost = parseFloat(document.getElementById('overhead_cost')?.value || 0);
  const monthly_fixed_costs = parseFloat(document.getElementById('monthly_fixed_costs')?.value || 0);
  const vat_rate = parseFloat(document.getElementById('vat_rate')?.value || 23);
  const selling_price = parseFloat(document.getElementById('selling_price')?.value || 0);

  // Update slider label readouts
  updateLabel('val_product_cost', formatMoney(product_cost));
  updateLabel('val_labor_hours', labor_hours + ' hrs');
  updateLabel('val_labor_rate', formatMoney(labor_rate) + '/h');
  updateLabel('val_overhead_cost', formatMoney(overhead_cost));
  updateLabel('val_monthly_fixed', formatMoney(monthly_fixed_costs));
  updateLabel('val_vat_rate', vat_rate + '%');
  updateLabel('val_selling_price', formatMoney(selling_price));

  // Calculations
  const labor_total = labor_hours * labor_rate;
  const unit_cost = product_cost + labor_total + overhead_cost;
  const price_with_vat = selling_price * (1 + vat_rate / 100);
  const gross_margin = selling_price - unit_cost;
  const margin_pct = selling_price > 0 ? (gross_margin / selling_price) * 100 : 0;
  const net_profit = gross_margin;

  let breakeven_units = 0;
  if (gross_margin > 0) {
    breakeven_units = Math.ceil(monthly_fixed_costs / gross_margin);
  }
  const breakeven_revenue = breakeven_units * selling_price;

  // Update DOM Output Metrics
  setText('out_total_cost', formatMoney(unit_cost));
  setText('out_price_vat', formatMoney(price_with_vat));
  setText('out_gross_margin', formatMoney(gross_margin));
  setText('out_margin_pct', margin_pct.toFixed(1) + '%');
  setText('out_net_profit', formatMoney(net_profit));
  setText('out_breakeven_units', breakeven_units.toLocaleString('pt-PT') + ' un.');
  setText('out_breakeven_revenue', formatMoney(breakeven_revenue));

  // Status Badge Update
  const badge = document.getElementById('margin_status_badge');
  if (badge) {
    if (gross_margin <= 0) {
      badge.className = 'status-pill status-loss';
      badge.innerHTML = '<i class="fas fa-exclamation-triangle"></i> PREJUÍZO (Margem Negativa)';
    } else if (margin_pct < 25) {
      badge.className = 'status-pill status-warning';
      badge.innerHTML = '<i class="fas fa-exclamation-circle"></i> MARGEM BAIXA (< 25%)';
    } else {
      badge.className = 'status-pill status-profitable';
      badge.innerHTML = '<i class="fas fa-check-circle"></i> PRODUTO RENTÁVEL (' + margin_pct.toFixed(1) + '%)';
    }
  }

  // Update Break-Even Chart
  updateChartData(monthly_fixed_costs, unit_cost, selling_price, breakeven_units);
}

function updateLabel(id, text) {
  const el = document.getElementById(id);
  if (el) el.innerText = text;
}

function setText(id, text) {
  const el = document.getElementById(id);
  if (el) el.innerText = text;
}

function formatMoney(val) {
  return '€ ' + val.toFixed(2).replace('.', ',').replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
}

function initChart(ctx) {
  breakEvenChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [],
      datasets: [
        {
          label: 'Custos Totais (€)',
          borderColor: '#EF4444',
          backgroundColor: 'rgba(239, 68, 68, 0.1)',
          fill: true,
          data: [],
          tension: 0.1
        },
        {
          label: 'Faturação Total (€)',
          borderColor: '#10B981',
          backgroundColor: 'rgba(16, 185, 129, 0.1)',
          fill: true,
          data: [],
          tension: 0.1
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'bottom' },
        tooltip: {
          callbacks: {
            label: function(context) {
              return context.dataset.label + ': € ' + context.parsed.y.toLocaleString('pt-PT');
            }
          }
        }
      },
      scales: {
        x: { title: { display: true, text: 'Unidades Vendidas / Mês' } },
        y: { title: { display: true, text: 'Valor (€)' } }
      }
    }
  });
}

function updateChartData(fixedCosts, unitCost, price, breakevenUnits) {
  if (!breakEvenChart) return;

  const maxUnits = Math.max(breakevenUnits * 2, 40);
  const step = Math.max(1, Math.floor(maxUnits / 8));

  const labels = [];
  const costsData = [];
  const revData = [];

  for (let u = 0; u <= maxUnits + step; u += step) {
    labels.push(u + ' un');
    costsData.push(fixedCosts + (unitCost * u));
    revData.push(price * u);
  }

  breakEvenChart.data.labels = labels;
  breakEvenChart.data.datasets[0].data = costsData;
  breakEvenChart.data.datasets[1].data = revData;
  breakEvenChart.update();
}

function loadPreset(product_cost, labor_hours, labor_rate, overhead_cost, monthly_fixed_costs, vat_rate, selling_price) {
  document.getElementById('product_cost').value = product_cost;
  document.getElementById('labor_hours').value = labor_hours;
  document.getElementById('labor_rate').value = labor_rate;
  document.getElementById('overhead_cost').value = overhead_cost;
  document.getElementById('monthly_fixed_costs').value = monthly_fixed_costs;
  document.getElementById('vat_rate').value = vat_rate;
  document.getElementById('selling_price').value = selling_price;
  recalculate();
}

async function saveSimulation() {
  const nameInput = prompt('Por favor insira um nome para guardar esta simulação:', 'Nova Simulação ' + new Date().toLocaleDateString('pt-PT'));
  if (!nameInput) return;

  const categoryInput = prompt('Categoria (ex: Produto Físico, Serviço, Restauração):', 'Geral') || 'Geral';

  const payload = {
    name: nameInput,
    category: categoryInput,
    notes: 'Simulação interativa guardada via EJAJ TECH SaaS Engine.',
    product_cost: parseFloat(document.getElementById('product_cost')?.value || 0),
    labor_hours: parseFloat(document.getElementById('labor_hours')?.value || 0),
    labor_rate: parseFloat(document.getElementById('labor_rate')?.value || 0),
    overhead_cost: parseFloat(document.getElementById('overhead_cost')?.value || 0),
    monthly_fixed_costs: parseFloat(document.getElementById('monthly_fixed_costs')?.value || 0),
    vat_rate: parseFloat(document.getElementById('vat_rate')?.value || 23),
    selling_price: parseFloat(document.getElementById('selling_price')?.value || 0)
  };

  try {
    const res = await fetch('/api/simulations/save', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const result = await res.json();
    if (result.success) {
      alert('✅ ' + result.message);
      window.location.href = '/simulations';
    } else {
      alert('❌ Erro: ' + result.message);
    }
  } catch (err) {
    alert('❌ Erro de comunicação com o servidor.');
  }
}
