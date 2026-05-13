document.addEventListener("DOMContentLoaded", () => {

    const messageInput = document.getElementById("messageInput");
    const sendBtn = document.getElementById("sendMessageBtn");
    const chatMessages = document.getElementById("chatMessages");
    const emojiBtn = document.getElementById("emojiBtn");
    const emojiPicker = document.getElementById("emojiPicker");
    const closeEmojiPicker = document.getElementById("closeEmojiPicker");
    const clearChatBtn = document.getElementById("clearChatBtn");
    const helpBtn = document.getElementById("helpBtn");
    const logoutBtn = document.getElementById("logoutBtn");

    const USER_EMAIL = localStorage.getItem("jamieParentEmail") || sessionStorage.getItem("jamieParentEmail") || "parent@example.com";
    const USER_AGE = 10;

    let selectedVoice = null;

    function setFemaleVoice() {
        const voices = window.speechSynthesis.getVoices();
        selectedVoice = voices.find(v => /female|zira|susan|amy|alloy/i.test(v.name)) || voices[0];
    }
    window.speechSynthesis.onvoiceschanged = setFemaleVoice;
    setFemaleVoice();

    /* ================= SEND MESSAGE ================= */
    async function sendMessage() {
        const msg = messageInput.value.trim();
        if (!msg) return;
        addMessage(msg, "user", "You");
        messageInput.value = "";
        showTyping();

        try {
            const response = await fetch("http://127.0.0.1:8000/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: msg, age: USER_AGE, email: USER_EMAIL })
            });
            const data = await response.json();
            removeTyping();
            addMessage(data.reply, "jamie", "Jamie");

            if (data.reply) {
                const utterance = new SpeechSynthesisUtterance(data.reply);
                utterance.lang = 'en-US';
                utterance.voice = selectedVoice;
                utterance.pitch = 1.5;
                utterance.rate = 0.9;
                utterance.onend = () => { if(data.video_link) window.open(data.video_link, "_blank"); };
                window.speechSynthesis.cancel();
                window.speechSynthesis.speak(utterance);
            }
        } catch (err) {
            removeTyping();
            addMessage("Sorry! Jamie is having trouble connecting right now 😢", "jamie", "Jamie");
            console.error(err);
        }
    }

    /* ================= ADD MESSAGE ================= */
    function addMessage(text, sender, name) {
        const div = document.createElement("div");
        div.className = `message ${sender}-message`;

        const icon = sender === "user" ? "fas fa-user" : "fas fa-robot";
        const time = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

        div.innerHTML = `
            <div class="message-avatar"><i class="${icon}"></i></div>
            <div class="message-content">
                <div class="message-sender">${name}</div>
                <div class="message-text">${escapeHtml(text)}</div>
                <div class="message-time">${time}</div>
            </div>
        `;
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function showTyping() {
        const div = document.createElement("div");
        div.className = "message jamie-message";
        div.id = "typing";
        div.innerHTML = `<div class="message-avatar"><i class="fas fa-robot"></i></div>
                         <div class="message-content"><div class="message-sender">Jamie</div><div class="message-text">Typing...</div></div>`;
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function removeTyping() {
        const t = document.getElementById("typing");
        if (t) t.remove();
    }

    // ------------------ Apple popup logic ------------------
function showApplePopup(count) {
    const appleTree = document.getElementById('appleTree');
    const totalApples = document.getElementById('totalApples');
    appleTree.innerHTML = "";
    totalApples.innerText = "";

    for (let i = 0; i < count; i++) {
        const apple = document.createElement('div');
        apple.classList.add('apple');
        apple.style.left = (20 + Math.random() * 60) + '%';
        apple.style.animationDelay = (i * 0.3) + 's';
        apple.innerText = '🍎';
        appleTree.appendChild(apple);
    }

    setTimeout(() => {
        totalApples.innerText = `Total apples collected: ${count}`;
    }, count * 300 + 2000);

    const appleModal = new bootstrap.Modal(document.getElementById('applePopup'));
    appleModal.show();
}


    /* ================= EMOJI PICKER ================= */
    emojiBtn?.addEventListener("click", () => {
        emojiPicker.style.display = emojiPicker.style.display === "block" ? "none" : "block";
    });
    closeEmojiPicker?.addEventListener("click", () => emojiPicker.style.display = "none");
    document.querySelectorAll(".emoji").forEach(e => {
        e.addEventListener("click", () => {
            messageInput.value += e.textContent;
            messageInput.focus();
            emojiPicker.style.display = "none";
        });
    });

    function escapeHtml(text) {
        const div = document.createElement("div");
        div.textContent = text;
        return div.innerHTML;
    }

    /* ================= CLEAR CHAT ================= */
    clearChatBtn.addEventListener("click", () => {
        chatMessages.querySelectorAll(".message").forEach((msg, index) => {
            if(index !== 0) msg.remove();
        });
        chatMessages.scrollTop = 0;
    });

    /* ================= LOGOUT ================= */
    logoutBtn.addEventListener("click", () => window.location.href = "/logout");

    /* ================= HELP MODAL ================= */
    const helpModalHTML = `
        <div class="modal fade" id="helpModal" tabindex="-1" aria-labelledby="helpModalLabel" aria-hidden="true">
          <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title" id="helpModalLabel">Need Help?</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div class="modal-body">
                <p>Contact our support team:</p>
                <h6>support@jamie.com</h6>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
              </div>
            </div>
          </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', helpModalHTML);
    const helpModal = new bootstrap.Modal(document.getElementById('helpModal'));
    helpBtn.addEventListener("click", () => helpModal.show());

    /* ================= FEATURE MODAL ================= */
    const featureModalHTML = `
        <div class="modal fade" id="featureModal" tabindex="-1" aria-labelledby="featureModalLabel" aria-hidden="true">
          <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title" id="featureModalLabel">Jamie’s Cool New Features</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div class="modal-body">
                <ul>
                    <li>📖 Engages your kids with interactive stories</li>
                    <li>🕌 Focuses on Islamic content & values</li>
                    <li>💪 Motivates children to learn daily</li>
                    <li>🎮 Includes fun educational games</li>
                    <li>📝 Helps with homework & learning tasks</li>
                    <li>🌟 Teaches good manners and social skills</li>
                    <li>🗣️ Talks to your kids with friendly voice interactions</li>
                </ul>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
              </div>
            </div>
          </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', featureModalHTML);
    const featureModal = new bootstrap.Modal(document.getElementById('featureModal'));

    // Trigger feature modal on heading click
    const newFeatureHeading = document.querySelector(".jamie-features h5");
    if(newFeatureHeading) {
        newFeatureHeading.style.cursor = "pointer";
        newFeatureHeading.addEventListener("click", () => featureModal.show());
    }

    /* ================= JAMIE FEATURES EXPAND ================= */
    const featuresSection = document.querySelector(".jamie-features");
    if (featuresSection) {
        const title = featuresSection.querySelector("h5");
        const content = featuresSection.querySelector(".features-content");

        title.addEventListener("click", () => {
            featuresSection.classList.toggle("expanded");
            if(featuresSection.classList.contains("expanded")) {
                content.style.maxHeight = content.scrollHeight + "px";
            } else {
                content.style.maxHeight = "0";
            }
        });

        window.addEventListener("resize", () => {
            if(featuresSection.classList.contains("expanded")) {
                content.style.maxHeight = content.scrollHeight + "px";
            }
        });
    }

    /* ================= EVENTS ================= */
    sendBtn.addEventListener("click", sendMessage);
    messageInput.addEventListener("keypress", e => { if(e.key === "Enter") sendMessage(); });

});




