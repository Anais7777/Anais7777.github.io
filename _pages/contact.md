---
layout: page
title: Contacte
permalink: /contact
comments: false
---

<form action="https://formspree.io/{{site.email}}" method="POST">    
<p class="mb-4">Ai ceva sugestii pentru scriucutolk? Părerea ta contează pentru noi! </p>
<div class="form-group row">
<div class="col-md-6">
<input class="form-control" type="text" name="name" placeholder="Nume*" required>
</div>
<div class="col-md-6">
<input class="form-control" type="email" name="_replyto" placeholder="E-mail*" required>
</div>
</div>
<textarea rows="8" class="form-control mb-3" name="message" placeholder="Mesajul tău*" required></textarea>    
<input class="btn btn-dark" type="submit" value="Send">
</form>