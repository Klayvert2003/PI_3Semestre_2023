var senhaInput = document.getElementById('senha');
var confirmarSenhaInput = document.getElementById('confirma-senha');
var submitButton = document.getElementById('submit-button');

confirmarSenhaInput.addEventListener('input', function() {
  if (confirmarSenhaInput.value === senhaInput.value) {
    submitButton.disabled = false;
    senhaInput.style.color = 'green';
    confirmarSenhaInput.style.color = 'green';
  } else {
    submitButton.disabled = true;
    senhaInput.style.color = 'red';
    confirmarSenhaInput.style.color = 'red';
  }
});
