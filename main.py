# main.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Template

# Definir mapeo de dominios de forma estática
domain_mapping = {
    "dti.eduqas.cl": "7edu-survey-unach.educadventista.org",
    "unach.eduqas.cl": "7edu-survey-unach.educadventista.org",
    "femvo.eduqas.cl": "7edu-survey-femvo.educadventista.org",
    "fejo.eduqas.cl": "7edu-survey-fejo.educadventista.org",
    "fejt.eduqas.cl": "7edu-survey-fejt.educadventista.org",
    "fefw.eduqas.cl": "7edu-survey-fefw.educadventista.org",
    "fegc.eduqas.cl": "7edu-survey-fegc.educadventista.org",
    "fas.eduqas.cl": "7edu-survey-fasc.educadventista.org",
    "fesg.eduqas.cl": "7edu-survey-fesg.educadventista.org",
    "ecuador.eduqas.cl": "7edu-survey-ue.educadventista.org",
    "unionecuatoriana.eduqas.cl": "7edu-survey-ue.educadventista.org",
    "ubs.eduqas.cl": "7edu-survey-usb.educadventista.org",
    "peru.eduqas.cl": "7edu-survey-upn.educadventista.org",
    "unionperuana.eduqas.cl": "7edu-survey-upn.educadventista.org",
    "useb.eduqas.cl": "7edu-survey-useb.educadventista.org",
    "uar.eduqas.cl": "7edu-survey-ua.educadventista.org",
    "ubol.eduqas.cl": "7edu-survey-ub.educadventista.org",
    "upar.eduqas.cl": "7edu-survey-up.educadventista.org",
    "ucob.eduqas.cl": "7edu-survey-ucob.educadventista.org",
    "ulb.eduqas.cl": "7edu-survey-ulb.educadventista.org",
    "unb.eduqas.cl": "7edu-survey-unb.educadventista.org",
    "uneb.eduqas.cl": "7edu-survey-uneb.educadventista.org",
    "unob.eduqas.cl": "7edu-survey-unob.educadventista.org",
    "dsa.eduqas.cl": "7edu-survey.educadventista.org",
    "uru.eduqas.cl": "7edu-survey-uu.educadventista.org",
    "genesis-chile.unach.cl": "7edu-survey-uch.educadventista.org",
    "unionchilena.cl": "7edu-survey-uch.educadventista.org",
    "unionchilena.eduqas.cl": "7edu-survey-uch.educadventista.org",
    "ups.eduqas.cl": "7edu-survey-ups.educadventista.org",
    "ucb.eduqas.cl": "7edu-survey-ucb.educadventista.org"
}

# Definir mensajes traducidos
translations = {
    "es": {
        "title": "Sistema Migrado",
        "migrated_from": "El sistema ha sido migrado del dominio:",
        "migrated_to": "al nuevo dominio:",
        "redirect_available": "Esta redirección estará disponible por un tiempo limitado (hasta 1 mes).",
        "update_references": "Por favor, actualice sus marcadores o referencias en el navegador para usar el nuevo dominio.",
        "redirecting": "Redirigiendo automáticamente en {seconds} segundos..."
    },
    "en": {
        "title": "System Migrated",
        "migrated_from": "The system has been migrated from the domain:",
        "migrated_to": "to the new domain:",
        "redirect_available": "This redirection will be available for a limited time (up to 1 month).",
        "update_references": "Please update your bookmarks or references in the browser to use the new domain.",
        "redirecting": "Automatically redirecting in {seconds} seconds..."
    },
    "pt": {
        "title": "Sistema Migrado",
        "migrated_from": "O sistema foi migrado do domínio:",
        "migrated_to": "para o novo domínio:",
        "redirect_available": "Este redirecionamento estará disponível por tempo limitado (até 1 mês).",
        "update_references": "Por favor, atualize seus favoritos ou referências no navegador para usar o novo domínio.",
        "redirecting": "Redirecionando automaticamente em {seconds} segundos..."
    }
}

app = FastAPI()

template = Template(
    """
    <!DOCTYPE html>
    <html lang="{{ lang }}" class="h-full">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
        <title>{{ messages['title'] }}</title>
    </head>
    <body class="h-full bg-gray-100 flex items-center justify-center">
        <div class="w-full max-w-5xl bg-white shadow-lg rounded-lg overflow-hidden">
            <div class="md:flex">
                <!-- Información de migración -->
                <div class="md:w-1/2 bg-gradient-to-br from-blue-600 to-purple-600 p-8 text-white">
                    <h1 class="text-3xl font-bold mb-4">{{ messages['title'] }}</h1>
                    <p class="text-lg mb-4">{{ messages['migrated_from'] }}</p>
                    <p class="text-xl font-semibold">{{ current_domain }}</p>
                    <p class="text-lg mt-4">{{ messages['migrated_to'] }}</p>
                    <a href="https://{{ new_domain }}" class="text-xl font-bold underline">
                        {{ new_domain }}
                    </a>
                    <p class="mt-4 text-sm">
                        {{ messages['redirect_available'] }}
                        <br>
                        {{ messages['update_references'] }}
                    </p>
                </div>
                <!-- Representación visual -->
                <div class="md:w-1/2 bg-gray-50 p-8 flex items-center justify-center">
                    <div class="text-center">
                        <img src="/static/logo.png" alt="Logo Educación Adventista" class="mx-auto mb-4 w-32">
                        <p class="text-gray-700">SURVEY - Educación Adventista</p>
                        <div id="countdown" class="mt-4 text-red-500 font-bold"></div>
                    </div>
                </div>
            </div>
        </div>
        <script>
            let countdown = 30; // Tiempo en segundos
            const countdownElement = document.getElementById('countdown');
            const interval = setInterval(() => {
                countdownElement.textContent = "{{ messages['redirecting'] }}".replace("{seconds}", countdown);
                if (countdown <= 0) {
                    clearInterval(interval);
                    window.location.href = 'https://{{ new_domain }}';
                }
                countdown--;
            }, 1000);
        </script>
    </body>
    </html>
    """
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def redirect_page(request: Request):
    current_domain = request.headers.get("host", "unknown").split(":")[0]
    new_domain = domain_mapping.get(current_domain, "7edu-survey.educadventista.org")
    
    # Obtener el idioma preferido del cliente
    accept_language = request.headers.get("accept-language", "es").split(",")[0]
    lang = accept_language.split("-")[0]
    messages = translations.get(lang, translations["es"])  # Por defecto a español
    
    return HTMLResponse(template.render(current_domain=current_domain, new_domain=new_domain, messages=messages, lang=lang))