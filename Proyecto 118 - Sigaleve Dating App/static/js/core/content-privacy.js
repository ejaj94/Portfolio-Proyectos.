/**
 * Filtro anti-doxxing no cliente: bloqueia telefones, redes sociais, e-mails e links.
 */
'use strict';

// =========================================================================
// IMPLEMENTAÇÃO DOS 3 REQUISITOS NOVOS:
// 1. Álbum Privado / Cofre Oculto 🔒
// 2. Likes e Comentários em Fotos + Filtro Anti-Doxxing 🛡️
// 3. Momentos & Sentimentos / Feed Comunitário ✨
// =========================================================================

// --- 🛡️ FILTRO ANTI-DOXXING NO CLIENTE ---
function validateContentPrivacyClient(text) {
  if (!text) return { ok: true };
  const cleaned = text.trim();

  // Telefone / Sequência de dígitos
  const digitsOnly = cleaned.replace(/\D/g, '');
  if (digitsOnly.length >= 9) {
    return { ok: false, reason: 'Por segurança e privacidade, não é permitido partilhar números de telefone.' };
  }

  // Padrões de redes sociais e identificadores
  const forbiddenPatterns = [
    /@[\w_.-]+/i,
    /\b(ig|insta|instagram|snap|snapchat|tiktok|telegram|whats|whatsapp|facebook|fb|twitter|x)\b/i,
    /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/i,
    /(https?:\/\/|www\.)\S+/i,
    /\b[a-zA-Z0-9-]+\.(com|pt|net|org|es|br|io|app|co)\b/i
  ];

  for (const pat of forbiddenPatterns) {
    if (pat.test(cleaned)) {
      return {
        ok: false,
        reason: 'Por segurança e privacidade, não é permitido partilhar redes sociais, emails ou links externos.'
      };
    }
  }

  return { ok: true };
}
