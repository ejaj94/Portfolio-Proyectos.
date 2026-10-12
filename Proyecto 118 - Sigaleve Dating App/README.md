# Proyecto 118: Sigaleve — Progressive Web App (PWA) de Conexões Humanas & Dating Seguro

<p align="center">
  <img src="docs/sigaleve_showcase.jpg" alt="Sigaleve Platform Architecture & Showcase" width="850" style="border-radius: 12px; box-shadow: 0 8px 30px rgba(0,0,0,0.12);" />
</p>

<p align="center">
  <strong>Sigaleve</strong> é uma plataforma moderna e inclusiva de relacionamentos e comunidade focada em <strong>privacidade radical</strong>, <strong>segurança em tempo real</strong> e <strong>combate ao estigma social</strong>.
</p>

---

## 🌟 Visão Geral do Projeto

Desenvolvido como uma aplicação web progressiva (**PWA**) de alto desempenho, o **Sigaleve** foi desenhado para proporcionar um ambiente empático e livre de preconceitos, especialmente pensado para pessoas com condições crónicas de saúde e ISTs (Infeções Sexualmente Transmissíveis), permitindo ligações autênticas, transparentes e com total salvaguarda da identidade.

> **Status:** Showcase de Portfólio / Produção Sanitizada  
> **Arquitetura:** Python Flask (Eventlet) + Socket.IO + Tailwind CSS + Vanilla JS PWA + Nginx Reverse Proxy  
> **Segurança:** Privacy Shield, Botão de Pânico com Camuflagem Instantânea, Criptografia PBKDF2/Werkzeug, 2FA OTP & Rate Limiting.

---

## 🚀 Principais Funcionalidades

### 1. 🛡️ Privacy Shield & Discrição Total
- **Modo Incógnito:** Os utilizadores só ficam visíveis para os perfis a quem deram "Like".
- **Botão de Pânico (Quick Stealth Escape):**
  - Implementado em cabeçalhos e menus de navegação.
  - Ao ser clicado perante olhares indiscretos ou risco de exposição involuntária, redireciona instantaneamente a página para uma pesquisa benigna externa (ex.: *Receitas de Biscoitos de Chocolate no Google*), limpando visualizações sensíveis do ecrã de imediato.
  - Inclui tooltip explicativo (`i`) com linguagem simples e clara.

### 2. ⚡ Conexões em Tempo Real (WebSockets & Matches)
- Motor de deslize com gestos fluídos (Touch Swipes e cliques rápidos).
- Mensagens diretas e chat interativo com Socket.IO em baixa latência.
- Filtros inteligentes de compatibilidade por localização (Geolocalização / Raio em KM), idade, interesses e objetivos.

### 3. 💎 Níveis de Assinatura & Monetização (Plus, Gold & Platinum)
- **Plus:** Swipes e likes ilimitados, Modo Incógnito e Passaporte Global.
- **Gold:** Galeria de admiradores secretos (*Quem Gostou de Ti*), Top Picks diários e Rebobinar ilimitado.
- **Platinum:** Likes prioritários na fila de descoberta, mensagens diretas com Super Likes e Boosts periódicos.

### 4. 🔒 Segurança de Contas & Verificação
- Autenticação com requisitos estritos de complexidade de palavra-passe.
- Suporte a verificação de dois fatores (**2FA via TOTP / QR Code** com PyOTP).
- Integração OAuth configurável (Google Login & Meta/Facebook Login).
- Proteção CSRF, headers `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN` e sanitização estrita de inputs.

### 5. 🌐 Experiência PWA Nativa
- Totalmente responsivo para telemóvel, tablet e desktop.
- `manifest.json` com suporte a instalação como app nativa em iOS e Android.
- Alternância dinâmica entre tema claro e tema escuro respeitando preferências do utilizador ou do sistema operativo.

---

## 🛠️ Stack Tecnológica

| Camada | Tecnologias Utilizadas |
| :--- | :--- |
| **Backend** | Python 3.10+, Flask, Flask-SocketIO, Eventlet, Gunicorn, Werkzeug |
| **Frontend** | HTML5 Semântico, Tailwind CSS, FontAwesome 6, Vanilla JavaScript (ES6+), Touch Events |
| **Comunicação** | WebSockets (Socket.IO bi-direcional para chat e eventos de match) |
| **Segurança & Criptografia** | PyOTP, QRCode, Werkzeug Security (Hashes criptográficos), HTTPS/TLS |
| **Deploy & Servidor** | Nginx (Reverse Proxy + WebSocket upgrade), Systemd, Linux VPS |

---

## 📂 Estrutura de Diretórios Sanitizada

```text
Proyecto 118 - Sigaleve Dating App/
├── app.py                      # Servidor principal Flask + Socket.IO
├── requirements.txt            # Dependências Python
├── nginx_sigaleve.conf         # Configuração de produção Nginx
├── .env.example                # Modelo de variáveis de ambiente (sem credenciais reais)
├── .gitignore                  # Regras estritas de exclusão de dados e chaves
├── docs/
│   └── sigaleve_showcase.jpg   # Infográfico de arquitetura e funcionalidades
├── data/
│   ├── users_store.example.json # Base de dados mock/demo para testes locais
│   ├── moments_store.json
│   └── photo_interactions.json
├── static/                     # Assets estáticos (CSS, JS, ícones PWA, logos)
└── templates/                  # Templates Jinja2 (Landing, App, Políticas legais)
```

---

## ⚙️ Como Executar Localmente

### 1. Clonar o Repositório e Navegar para a Pasta
```bash
cd "Proyecto 118 - Sigaleve Dating App"
```

### 2. Criar e Ativar Ambiente Virtual
```bash
python -m venv venv
# No Windows:
.\venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente
Copie o ficheiro `.env.example` para `.env` e ajuste se desejar usar OAuth ou SMTP:
```bash
cp .env.example .env
```
*(Se não configurar SMTP ou OAuth, o servidor opera em modo local/demo com logs claros no terminal).*

### 5. Iniciar a Aplicação
```bash
python app.py
```
Acesse a aplicação no navegador em:
- **Landing Page:** `http://localhost:5001/`
- **Web App:** `http://localhost:5001/app`

---

## 🛡️ Nota de Privacidade e Conformidade (Senior Developer Note)

Este repositório foi **rigorosamente sanitizado**:
- ❌ **Sem dados sensíveis de utilizadores reais:** O diretório `data/` contém apenas utilizadores de demonstração fictícios (`users_store.example.json`). Ficheiros reais de produção são excluídos via `.gitignore`.
- ❌ **Sem credenciais ou segredos em texto limpo:** Chaves de API do Google, Meta, senhas de VPS e tokens SMTP foram substituídos por variáveis dinâmicas de ambiente.
- 🛡️ Total conformidade com as melhores práticas de segurança e privacidade do utilizador (RGPD / LGPD).

---
**Autor:** Emmanuel (EJAJ TECH)  
*Showcase de Engenharia de Software e Produto*
