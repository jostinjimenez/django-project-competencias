const alertPlaceholder = document.getElementById('liveAlertPlaceholder');
const appendAlert = (message, type) => {
    const wrapper = document.createElement('div');
    wrapper.innerHTML = [
        `<div class="alert alert-${type} alert-dismissible fade show" role="alert">`,
        `   <div>${message}</div>`,
        '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
        '</div>'
    ].join('');

    alertPlaceholder.appendChild(wrapper);

    // Agregamos la clase 'fade-out' después de agregar el mensaje de alerta
    wrapper.firstChild.classList.add('fade-out');

    // Después de 3 segundos, eliminamos la alerta del DOM
    setTimeout(() => {
        wrapper.remove();
    }, 3000);
};

const alertTrigger = document.getElementById('liveAlertBtn');
if (alertTrigger) {
    alertTrigger.addEventListener('click', () => {
        appendAlert('La competicion ha sido activada', 'success');
    });
}