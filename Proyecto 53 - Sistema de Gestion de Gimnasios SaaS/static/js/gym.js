// EJAJ TECH - FitClub Gym SaaS Interactive JavaScript

// Open / Close Check-in Modal
function openCheckinModal() {
    const modal = document.getElementById('checkinModal');
    if (modal) modal.style.display = 'flex';
}

function closeCheckinModal() {
    const modal = document.getElementById('checkinModal');
    if (modal) modal.style.display = 'none';
}

// Record Member Check-in AJAX
async function submitCheckin(event) {
    event.preventDefault();
    const memberId = document.getElementById('checkinMemberSelect').value;
    const entryType = document.getElementById('checkinEntryType').value;

    if (!memberId) {
        alert('Por favor selecione um sócio.');
        return;
    }

    try {
        const res = await fetch('/api/attendance/checkin', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ member_id: parseInt(memberId), entry_type: entryType })
        });

        const data = await res.json();
        if (data.success) {
            alert(data.message);
            closeCheckinModal();
            window.location.reload();
        } else {
            alert('Acesso recusado: ' + data.message);
        }
    } catch (err) {
        alert('Erro de conexão: ' + err.message);
    }
}

// Register New Member AJAX
async function submitNewMemberForm(event) {
    event.preventDefault();
    const name = document.getElementById('full_name').value.trim();
    const email = document.getElementById('email').value.trim();
    const phone = document.getElementById('phone').value.trim();
    const nif = document.getElementById('nif').value.trim();
    const planId = document.getElementById('plan_id').value;

    try {
        const res = await fetch('/api/members/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                full_name: name,
                email: email,
                phone: phone,
                nif: nif,
                plan_id: parseInt(planId)
            })
        });

        const data = await res.json();
        if (data.success) {
            alert('Sócio inscrito com sucesso! Código: ' + data.code);
            window.location.href = '/members';
        } else {
            alert('Erro ao registar sócio: ' + data.message);
        }
    } catch (err) {
        alert('Erro de rede: ' + err.message);
    }
}

// Renew Member Membership Quota AJAX
async function renewMembership(memberId) {
    const method = prompt('Método de Pagamento para a Renovação (MBWay, Multibanco, Dinheiro, Cartão):', 'MBWay');
    if (!method) return;

    try {
        const res = await fetch('/api/members/renew', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ member_id: parseInt(memberId), payment_method: method })
        });

        const data = await res.json();
        if (data.success) {
            alert(data.message);
            window.location.reload();
        } else {
            alert('Erro ao renovar: ' + data.message);
        }
    } catch (err) {
        alert('Erro de rede: ' + err.message);
    }
}
