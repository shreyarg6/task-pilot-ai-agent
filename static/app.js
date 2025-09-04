const items = [];

function renderList(){
  const box = document.getElementById('tasklist');
  if(!items.length){ box.innerHTML = ''; return; }
  box.innerHTML = '';
  items.forEach((t, i)=>{
    const chip = document.createElement('div');
    chip.className = 'task-chip';
    const meta = [];
    if(t.minutes) meta.push(`${t.minutes}m`);
    if(t.importance) meta.push(t.importance);
    chip.innerHTML = `<strong>${t.title}</strong> ${meta.length? '· '+meta.join(' · ') : ''}
      <button title="remove" aria-label="remove" onclick="removeItem(${i})">✕</button>`;
    box.appendChild(chip);
  });
}

function removeItem(i){
  items.splice(i,1);
  renderList();
}

document.getElementById('createForm').addEventListener('submit', (e)=>{
  e.preventDefault();
  const title = document.getElementById('task_text').value.trim();
  const minutes = document.getElementById('length').value ? parseInt(document.getElementById('length').value,10) : null;
  const importance = document.getElementById('importance').value || null;
  if(!title) return;

  items.push({ title, minutes, importance });
  document.getElementById('task_text').value = '';
  document.getElementById('length').value = '';
  document.getElementById('importance').value = '';
  renderList();
});

document.getElementById('planBtn').addEventListener('click', async ()=>{
  if(!items.length) return;

  const res = await fetch('/ask', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({ items })
  });
  const data = await res.json();
  renderConversation(data);
});

function renderConversation(data){
  const chat = document.getElementById('chat');
  chat.innerHTML = '';
  // echo user tasks
  const u = document.createElement('div');
  u.className='msg user';
  u.textContent = items.map(t=>t.title).join(', ');
  chat.appendChild(u);

  // bot reply
  const b = document.createElement('div');
  b.className='msg bot';
  b.innerHTML = `<div>${data.reply_html}</div>`;
  chat.appendChild(b);

  if(data.tasks && data.tasks.length){
    const table = document.createElement('table');
    table.innerHTML = `<thead><tr><th>Task</th><th>Due</th><th>Importance</th><th>Est. mins</th><th>Score rank</th></tr></thead>`;
    const tbody = document.createElement('tbody');
    data.tasks.forEach((t, idx)=>{
      const tr = document.createElement('tr');
      tr.innerHTML = `<td>${t.title}</td><td>${t.due_date||''}</td><td>${t.importance||''}</td><td>${t.estimated_minutes||''}</td><td>${idx+1}</td>`;
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    const plan = document.createElement('div');
    plan.className='plan';
    plan.appendChild(table);
    b.appendChild(plan);
  }
}
