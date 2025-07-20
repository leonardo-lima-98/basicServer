const form = document.getElementById("login-form");
form.addEventListener("submit", async (e) => {
    e.preventDefault();  // Impede o envio padrão

    const formData = new FormData(form);
    const data = new URLSearchParams(formData); // prepara como x-www-form-urlencoded

    const res = await fetch("/login", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: data
    });

    const result = await res.json();

    if (res.ok) {
    localStorage.setItem("token", result.access_token);
    alert("Login bem-sucedido!");
    // Redireciona, se quiser:
    window.location.href = "/logged";
    } else {
    alert("Falha no login: " + result.detail);
    }
});