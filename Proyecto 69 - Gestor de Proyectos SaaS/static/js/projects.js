document.addEventListener('DOMContentLoaded', () => {
    // Project Form Submit
    const projectForm = document.getElementById('project-form');
    if (projectForm) {
        projectForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const payload = {
                id: document.getElementById('proj-id').value || null,
                name: document.getElementById('proj-name').value,
                client_name: document.getElementById('proj-client').value,
                team_id: document.getElementById('proj-team').value,
                budget: parseFloat(document.getElementById('proj-budget').value || 0),
                start_date: document.getElementById('proj-start-date').value,
                due_date: document.getElementById('proj-due-date').value,
                status: document.getElementById('proj-status').value,
                description: document.getElementById('proj-desc').value
            };

            fetch('/api/project/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
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
            .catch(err => alert('❌ Erro na ligação ao servidor.'));
        });
    }

    // Task Form Submit
    const taskForm = document.getElementById('task-form');
    if (taskForm) {
        taskForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const payload = {
                project_id: document.getElementById('task-project-id').value,
                title: document.getElementById('task-title').value,
                assigned_to: document.getElementById('task-assigned').value,
                priority: document.getElementById('task-priority').value,
                status: document.getElementById('task-status').value,
                due_date: document.getElementById('task-due-date').value
            };

            fetch('/api/task/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
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
            .catch(err => alert('❌ Erro ao guardar tarefa.'));
        });
    }

    // Comment Form Submit
    const commentForm = document.getElementById('comment-form');
    if (commentForm) {
        commentForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const payload = {
                project_id: document.getElementById('comment-project-id').value,
                author: document.getElementById('comment-author').value || 'Gestor de Projeto',
                comment_text: document.getElementById('comment-text').value
            };

            fetch('/api/comment/add', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    window.location.reload();
                } else {
                    alert('⚠️ ' + data.message);
                }
            })
            .catch(err => alert('❌ Erro ao submeter comentário.'));
        });
    }

    // File Attach Form Submit
    const fileForm = document.getElementById('file-form');
    if (fileForm) {
        fileForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const payload = {
                project_id: document.getElementById('file-project-id').value,
                file_name: document.getElementById('file-name').value,
                file_size: document.getElementById('file-size').value || '2.5 MB',
                category: document.getElementById('file-category').value
            };

            fetch('/api/file/add', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
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
            .catch(err => alert('❌ Erro ao anexar ficheiro.'));
        });
    }
});

// Update Task Status AJAX
function toggleTaskStatus(taskId, newStatus) {
    fetch(`/api/task/status/${taskId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            window.location.reload();
        } else {
            alert('⚠️ ' + data.message);
        }
    })
    .catch(err => alert('❌ Erro ao atualizar tarefa.'));
}
