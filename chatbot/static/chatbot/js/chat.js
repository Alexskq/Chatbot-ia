document.addEventListener("DOMContentLoaded", function () {
  const chatMessages = document.getElementById("chat-messages");
  const chatForm = document.getElementById("chat-form");
  const messageInput = document.getElementById("message-input");

  // Fonction pour faire défiler vers le dernier message
  function scrollToLastMessage() {
    const lastMessage = chatMessages.lastElementChild;
    if (lastMessage) {
      lastMessage.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  }

  // Faire défiler vers le dernier message au chargement
  scrollToLastMessage();

  // Gérer l'envoi du formulaire avec AJAX
  chatForm.addEventListener("submit", function (e) {
    e.preventDefault();

    const userMessage = messageInput.value.trim();
    if (!userMessage) return;

    // Ajouter immédiatement le message de l'utilisateur
    appendMessage(userMessage, "user");
    messageInput.value = "";

    // Envoyer le message via AJAX
    const formData = new FormData(chatForm);
    const xhr = new XMLHttpRequest();
    xhr.open("POST", window.location.href, true);
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    
    xhr.onload = function () {
      if (xhr.status === 200) {
        try {
          const response = JSON.parse(xhr.responseText);
          if (response.status === "success") {
            appendMessage(response.bot_response, "bot");
          }
        } catch (e) {
          console.error("Erreur de parsing JSON:", e);
        }
      } else {
        console.error("Erreur de requête:", xhr.status);
        appendMessage("Désolé, une erreur est survenue.", "bot");
      }
    };
    
    xhr.onerror = function () {
      console.error("Erreur réseau");
      appendMessage("Désolé, une erreur de connexion est survenue.", "bot");
    };
    
    xhr.send(formData);
  });

  // Fonction pour ajouter un message au chat
  function appendMessage(content, sender) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message mb-3 ${
      sender === "bot" ? "text-start" : "text-end"
    }`;

    const time = new Date().toLocaleTimeString("fr-FR", {
      hour: "2-digit",
      minute: "2-digit",
    });

    messageDiv.innerHTML = `
      <div class="message-content ${
        sender === "bot" ? "bg-light" : "bg-primary text-white"
      }" 
        style="display: inline-block; padding: 10px; border-radius: 10px; max-width: 70%;">
        ${content}
      </div>
      <small class="text-muted d-block">${time}</small>
    `;

    chatMessages.appendChild(messageDiv);
    scrollToLastMessage();
  }
});
