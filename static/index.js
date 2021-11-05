function openModal(modal) {
    bootstrap.Modal.getOrCreateInstance(document.getElementById(modal == "connexionModal" ? "inscriptionModal" : "connexionModal")).hide();
    bootstrap.Modal.getOrCreateInstance(document.getElementById(modal)).show()
}
