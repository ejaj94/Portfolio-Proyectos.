# Arquitetura do Backend Sigaleve (Flask + Blueprints)

Este documento descreve a estrutura de backend refatorizada segundo os mais altos padrões de engenharia de software (Senior Software Architecture, SOC - Separation of Concerns).

---

## 🏛️ Estrutura de Diretórios

```
├── app.py                      # Ponto de entrada central, configuração WSGI e ProxyFix
├── services/
│   ├── __init__.py
│   └── common.py               # Helpers centrais (criptografia, persistência atómica, emails, presença)
├── routes/
│   ├── __init__.py
│   ├── auth.py                 # Registo, Login, 2FA (TOTP/Email), OAuth (Google/FB/IG), Reset de Senha
│   ├── profile.py              # Visualização de perfil, upload seguro de fotos (8MB máx) e verificação facial
│   ├── discovery.py            # Descoberta de perfis, likes mútuos e skips
│   ├── chat.py                 # Histórico de chat 24h efêmero e eventos Socket.IO em tempo real
│   ├── moments.py              # Histórias efêmeras de 24h com purga contínua em thread daemon
│   ├── vault.py                # Álbum Privado / Cofre Oculto com autorização mútua
│   ├── subscription.py         # Planos Sigaleve Plus e gestão de assinaturas
│   ├── push.py                 # Notificações WebPush (VAPID)
│   └── qa_health.py            # Comunidade Q&A anónima sobre saúde e ISTs
```

---

## 🔒 Princípios de Segurança e Qualidade Implementados

1. **Separação de Responsabilidades (SoC):**
   - O ficheiro monolítico original de ~3.850 linhas foi decomposto em 9 módulos independentes e focados.
   - O `app.py` foi reduzido para ~460 linhas, atuando puramente como orquestrador.

2. **Segurança de Autenticação e Dados:**
   - Remoção de fugas de `otp_code` ou `debug_code` em respostas HTTP.
   - Eliminação de fallbacks inseguros que pudessem permitir IDOR em atualização de perfis.
   - Criptografia simétrica com Fernet para campos de saúde (Artigo 9 do RGPD).
   - Bloqueio contra força bruta em memória no login (`_LOGIN_ATTEMPTS`).

3. **Confiabilidade de Dados (ACID / Atómico):**
   - Todas as gravações de JSON em disco usam ficheiros temporários (`.tmp`) e `os.replace` para prevenir corrupção em caso de queda de energia ou reinicialização.
