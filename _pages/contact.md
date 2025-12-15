---
layout: page
title: Contacte
permalink: /contact/
comments: false
---

<!-- 
  TO CONNECT TO GOOGLE SHEET:
  1. Follow instructions in GOOGLE_SHEETS_API_SETUP.md
  2. Set up Vercel environment variables:
     - GOOGLE_SHEET_ID
     - GOOGLE_SERVICE_ACCOUNT_KEY (entire JSON as string)
  3. Deploy to Vercel - the API route will handle submissions
-->
<form id="contact-form" method="POST">
<p class="mb-4">Ai ceva sugestii pentru scriucutolk? Părerea ta contează pentru noi! </p>
<div id="form-message" class="alert" style="display:none;"></div>
<div class="form-group row">
<div class="col-md-6">
<input class="form-control" type="text" name="name" placeholder="Nume*" required>
</div>
<div class="col-md-6">
<input class="form-control" type="email" name="_replyto" placeholder="E-mail*" required>
</div>
</div>
<textarea rows="12" class="form-control mb-3" name="message" placeholder="Mesajul tău*" required></textarea>    
<input class="btn btn-dark" type="submit" value="Send" id="submit-btn">
</form>

<script>
document.getElementById('contact-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    var form = this;
    var submitBtn = document.getElementById('submit-btn');
    var messageDiv = document.getElementById('form-message');
    
    // Disable submit button
    submitBtn.disabled = true;
    submitBtn.value = 'Se trimite...';
    
    // Get form data
    const formData = new FormData(form);
    const data = {
        name: formData.get('name'),
        _replyto: formData.get('_replyto'),
        message: formData.get('message')
    };
    
    try {
        // Submit to API route
        const response = await fetch('/api/submit-contact', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            // Success
            messageDiv.className = 'alert alert-success';
            messageDiv.textContent = 'Mulțumim! Mesajul tău a fost trimis cu succes.';
            messageDiv.style.display = 'block';
            form.reset();
        } else {
            // Error
            messageDiv.className = 'alert alert-danger';
            messageDiv.textContent = 'Eroare la trimitere. Te rugăm să încerci din nou.';
            messageDiv.style.display = 'block';
        }
    } catch (error) {
        // Network error
        messageDiv.className = 'alert alert-danger';
        messageDiv.textContent = 'Eroare la trimitere. Te rugăm să încerci din nou.';
        messageDiv.style.display = 'block';
    } finally {
        submitBtn.disabled = false;
        submitBtn.value = 'Send';
        
        // Hide message after 5 seconds
        setTimeout(function() {
            messageDiv.style.display = 'none';
        }, 5000);
    }
});
</script>