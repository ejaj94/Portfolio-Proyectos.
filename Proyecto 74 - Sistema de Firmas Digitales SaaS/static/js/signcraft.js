document.addEventListener('DOMContentLoaded', () => {
    // Canvas Signature Drawing Studio
    const canvas = document.getElementById('signature-canvas');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        let isDrawing = false;
        ctx.strokeStyle = '#065F46';
        ctx.lineWidth = 3;
        ctx.lineCap = 'round';

        function getPos(e) {
            const rect = canvas.getBoundingClientRect();
            return {
                x: (e.clientX || (e.touches && e.touches[0].clientX)) - rect.left,
                y: (e.clientY || (e.touches && e.touches[0].clientY)) - rect.top
            };
        }

        canvas.addEventListener('mousedown', (e) => {
            isDrawing = true;
            const pos = getPos(e);
            ctx.beginPath();
            ctx.moveTo(pos.x, pos.y);
        });

        canvas.addEventListener('mousemove', (e) => {
            if (!isDrawing) return;
            const pos = getPos(e);
            ctx.lineTo(pos.x, pos.y);
            ctx.stroke();
        });

        canvas.addEventListener('mouseup', () => isDrawing = false);
        canvas.addEventListener('mouseleave', () => isDrawing = false);

        // Touch support for mobiles/tablets
        canvas.addEventListener('touchstart', (e) => {
            e.preventDefault();
            isDrawing = true;
            const pos = getPos(e);
            ctx.beginPath();
            ctx.moveTo(pos.x, pos.y);
        });

        canvas.addEventListener('touchmove', (e) => {
            e.preventDefault();
            if (!isDrawing) return;
            const pos = getPos(e);
            ctx.lineTo(pos.x, pos.y);
            ctx.stroke();
        });

        canvas.addEventListener('touchend', () => isDrawing = false);

        // Clear Canvas Button
        const clearBtn = document.getElementById('clear-canvas-btn');
        if (clearBtn) {
            clearBtn.addEventListener('click', () => {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
            });
        }
    }

    // Submit Signature Form
    const signForm = document.getElementById('sign-submit-form');
    if (signForm) {
        signForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const docId = document.getElementById('sign-doc-id').value;
            const signerId = document.getElementById('sign-signer-id').value;

            fetch('/api/sign/submit', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ doc_id: docId, signer_id: signerId, signature_data: 'SIG_DRAW_CANVAS_OK' })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    alert('✅ ' + data.message);
                    window.location.reload();
                } else {
                    alert('⚠️ ' + data.message);
                }
            })
            .catch(err => alert('❌ Erro ao registar assinatura.'));
        });
    }

    // Create New Signature Request Form
    const docForm = document.getElementById('create-doc-form');
    if (docForm) {
        docForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const payload = {
                title: document.getElementById('doc-title-input').value,
                category: document.getElementById('doc-category-input').value,
                created_by: document.getElementById('doc-author-input').value,
                signer_name: document.getElementById('signer-name-input').value,
                signer_email: document.getElementById('signer-email-input').value,
                signer_role: document.getElementById('signer-role-input').value
            };

            fetch('/api/document/create', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    alert('✅ ' + data.message);
                    window.location.href = `/sign/${data.doc_id}`;
                } else {
                    alert('⚠️ ' + data.message);
                }
            })
            .catch(err => alert('❌ Erro ao emitir pedido de assinatura.'));
        });
    }
});
