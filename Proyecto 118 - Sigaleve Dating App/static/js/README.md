# Frontend JavaScript — guia de estrutura

O JavaScript da aplicação está dividido **por funcionalidade**. Cada ficheiro tem um comentário de
cabeçalho a explicar o que contém. Não há bundler: são *scripts clássicos* carregados por
`templates/sigaleve_app.html` com `<script src=...>`.

## Estrutura

```text
static/js/
├── core/                    Base partilhada por toda a app
│   ├── early-init.js        (<head>) tema escuro e idioma antes da 1ª pintura
│   ├── ui-feedback.js       toasts, confirmação e prompt personalizados
│   ├── i18n-data.js         dicionários de tradução (LANGS) e lista de línguas
│   ├── i18n.js              motor de tradução: T(), setLang(), translateAppUI()
│   ├── ui-state.js          tema escuro (toggle) e objeto STATE global
│   ├── navigation.js        showSection() — navegação entre secções
│   ├── bootstrap.js         arranque (DOMContentLoaded): sessão, idioma, atalhos
│   └── content-privacy.js   filtro anti-doxxing (telefones, redes, links)
├── features/                Uma funcionalidade por ficheiro
│   ├── auth.js              login, registo, 2FA, recuperar palavra-passe, login social
│   ├── onboarding.js        passos de criação de perfil e câmara
│   ├── profile.js           logout, perfil e edição de perfil
│   ├── community.js         Q&A de saúde, encontros em grupo, histórias de sucesso
│   ├── discover.js          baralho, swipe, detalhe de perfil
│   ├── matches.js           matches e lista de conversas
│   ├── chat.js              chat em tempo real (Socket.IO), fundo, anti-captura
│   ├── moments.js           feed "Momentos & Sentimentos"
│   ├── private-vault.js     cofre privado (álbum secreto)
│   ├── comments.js          comentários/gostos em fotos e momentos
│   ├── settings-drawer.js   gaveta lateral e cookies
│   └── layout.js            sidebar redimensionável, lightbox da foto
├── settings/                Modais da página de Definições
│   ├── theme-and-quick-exit.js   tema + botão de pânico (Saída Rápida)
│   ├── preferences.js            distância e faixa etária
│   ├── selection-options.js      modais de seleção (género, objetivos...)
│   ├── location-and-phone.js     países/cidades e indicativos
│   ├── blocked-contacts.js       contactos bloqueados
│   ├── settings-modals.js        notificações, privacidade, eliminar conta
│   └── selfie-verification.js    verificação por selfie
├── subscription/
│   └── subscription.js      planos, pagamento (cartão / MB Way) e gestão
└── tailwind-config.js       configuração do Tailwind (CDN)
```

CSS: `static/css/app.css`.

## Regras importantes

1. **A ordem dos `<script>` importa.** Os módulos partilham o âmbito global (como no ficheiro
   único original). Alguns estendem funções de módulos anteriores — por exemplo
   `moments.js` envolve `showSection` (definida em `navigation.js`) e `private-vault.js`
   envolve `openProfileDetail` (definida em `discover.js`).
2. Os ficheiros em `features/`, `core/` (exceto `early-init.js`) usam `'use strict'`; os de
   `settings/` e `subscription/` não (herdado do código original).
3. As funções chamadas por `onclick="..."` no HTML têm de continuar a ser globais
   (declaradas com `function nome()` ao nível do topo).
4. Ao acrescentar um módulo novo: criar o ficheiro, registar o `<script>` no template na
   posição certa e subir o parâmetro `?v=` para forçar a atualização da cache.
