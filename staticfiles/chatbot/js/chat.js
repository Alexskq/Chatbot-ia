document.addEventListener("DOMContentLoaded", function () {
  const chatMessages = document.getElementById("chat-messages");
  const chatForm = document.getElementById("chat-form");
  const messageInput = document.getElementById("message-input");

  // Fonction pour faire défiler vers le dernier message
  function scrollToLastMessage() {
    const lastMessage = chatMessages.lastElementChild;
    if (lastMessage) {
      lastMessage.scrollIntoView({ behavior: "smooth" });
    }
  }

  // Observer les changements dans le conteneur de messages
  const observer = new MutationObserver(() => {
    scrollToLastMessage();
  });

  // Observer les changements dans le conteneur de messages
  observer.observe(chatMessages, { childList: true });

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
  }

  chatForm.addEventListener("submit", function (e) {
    e.preventDefault();

    const formData = new FormData(chatForm);
    const userMessage = formData.get("message");

    // Ajouter immédiatement le message de l'utilisateur
    appendMessage(userMessage, "user");
    messageInput.value = "";

    // Envoyer le message au serveur
    fetch(window.location.href, {
      method: "POST",
      body: formData,
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          appendMessage(data.bot_response, "bot");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        appendMessage("Désolé, une erreur est survenue.", "bot");
      });
  });

  chatMessages.addEventListener("DOMContentLoaded", scrollToLastMessage());
});
