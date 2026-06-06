// Extract text and images from the page
async function scanPage() {
  const text = document.body.innerText.substring(0, 5000);
  const images = Array.from(document.images).map(img => img.src);
  
  const response = await fetch('http://localhost:8765/filter', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'x-api-key': 'secret-parent-key' },
    body: JSON.stringify({
      profile_id: 1,
      url: window.location.href,
      content_type: 'text',
      payload: text
    })
  });
  
  const data = await response.json();
  if (data.decision === 'BLOCK') {
    document.body.innerHTML = '<div style="background:black;color:white;text-align:center;padding:100px;font-family:sans-serif;"><h1>?? Blocked by Parent</h1><p>This content is not suitable for your age.</p></div>';
  } else if (data.decision === 'WARN') {
    alert('?? Warning: This page contains sensitive content.');
  }
}

scanPage();
