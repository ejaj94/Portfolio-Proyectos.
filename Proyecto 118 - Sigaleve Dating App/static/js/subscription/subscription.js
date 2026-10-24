/**
 * Subscrições e pagamentos: planos Plus/Gold/Platinum, cartão, MB Way e gestão da subscrição.
 */
// ═══════════════════════════════════════════════════
// ═══════════════════════════════════════════════════
// GESTIÓN DE SUBSCRIÇÃO E PAGAMENTOS (PLATINUM, GOLD, PLUS, SETTINGS)
// ═══════════════════════════════════════════════════
let currentProductTab = 'plus';
let selectedPlanId = 'plan_12m';
let selectedPlanPrice = '83.88';
let selectedPlanTitle = '12 Meses';

const PRODUCT_DATA_I18N = {
  es: {
    dur1m: '1 Mes', dur6m: '6 Meses', dur12m: '12 Meses',
    perMonth: '/mes', monthlyPay: 'pago mensual',
    badgeVip: 'VIP', badgePopular: 'Popular', badgeStandard: 'Estándar', badgeBest: 'Mejor valor',
    save40: 'Ahorra 40%', save37: 'Ahorra 37%', save33: 'Ahorra 33%',
    platTitle: 'Consigue el nivel más alto de Sigaleve',
    platDesc: 'Mira a quién le gustas, Likes prioritarios en la fila y mensajes directos antes de hacer match.',
    platBenefitsTitle: '<i class="fa-solid fa-gem text-zinc-300"></i> Ventajas Exclusivas Platinum',
    platBenefits: [
      '<strong>Likes prioritarios:</strong> los perfiles a los que des Like te verán antes que los demás.',
      '<strong>Mensajes antes de hacer match:</strong> adjunta una nota en cada Super Like.',
      '<strong>Mira a quién le gustas:</strong> visualiza todos los perfiles al instante sin esperas.',
      '<strong>Swipes y Likes ilimitados</strong> en todo el mundo.',
      '<strong>Pasaporte global:</strong> haz match y habla en cualquier ciudad sin moverte.',
      '<strong>5 Super Likes gratis por semana</strong> y 1 Boost gratis al mes.'
    ],
    goldTitle: 'Mira a quién le gustas & más',
    goldDesc: 'Descubre quién te ha dado Like antes de deslizar y desbloquea el Descubrimiento Premium.',
    goldBenefitsTitle: '<i class="fa-solid fa-crown text-amber-400"></i> Ventajas Incluidas en Gold',
    goldBenefits: [
      '<strong>Mira a quién le gustas:</strong> mira la galería completa de tus admiradores secretos.',
      '<strong>Top Picks diarios:</strong> selecciones premium basadas en tu vibra y compatibilidad.',
      '<strong>Swipes y Likes ilimitados:</strong> sin límite de perfiles por día.',
      '<strong>Rebobinar (Undo) ilimitado:</strong> deshaz tu último swipe tantas veces como quieras.',
      '<strong>5 Super Likes semanales</strong> y 1 Boost gratis mensual.'
    ],
    plusTitle: 'Swipes ilimitados y Modo Incógnito',
    plusDesc: 'Controla a quién ves, activa el modo incógnito y conecta sin límites.',
    plusBenefitsTitle: '<i class="fa-solid fa-bolt text-red-500"></i> Ventajas Incluidas en Plus',
    plusBenefits: [
      '<strong>Modo Incógnito:</strong> solo serás visible para las personas a las que les diste Like.',
      '<strong>Likes ilimitados:</strong> desliza a la derecha todo lo que desees.',
      '<strong>Rebobinar ilimitado:</strong> vuelve atrás si cometiste un error deslizando.',
      '<strong>Pasaporte:</strong> cambia tu ubicación a cualquier parte del mundo.',
      '<strong>Sin anuncios ni interrupciones:</strong> experiencia 100% fluida.'
    ],
    btnConfirm: 'Confirmar y Obtener Sigaleve'

  },
  pt: {
    dur1m: '1 Mês', dur6m: '6 Meses', dur12m: '12 Meses',
    perMonth: '/mês', monthlyPay: 'pagamento mensal',
    badgeVip: 'VIP', badgePopular: 'Popular', badgeStandard: 'Padrão', badgeBest: 'Melhor valor',
    save40: 'Poupa 40%', save37: 'Poupa 37%', save33: 'Poupa 33%',
    platTitle: 'Alcança o nível mais exclusivo do Sigaleve',
    platDesc: 'Vê quem gostou de ti, Gostos prioritários e mensagens diretas antes de fazer match.',
    platBenefitsTitle: '<i class="fa-solid fa-gem text-zinc-300"></i> Vantagens Exclusivas Platinum',
    platBenefits: [
      '<strong>Gostos prioritários:</strong> os teus likes aparecem primeiro a toda a gente.',
      '<strong>Mensagens antes de fazer match:</strong> envia uma nota em cada Super Like.',
      '<strong>Vê quem gostou de ti:</strong> descobre imediatamente os teus admiradores.',
      '<strong>Swipes e Likes ilimitados</strong> em todo o mundo.',
      '<strong>Passaporte global:</strong> conversa em qualquer cidade do planeta.',
      '<strong>5 Super Likes gratuitos por semana</strong> e 1 Boost por mês.'
    ],
    goldTitle: 'Vê quem gostou de ti e muito mais',
    goldDesc: 'Descobre quem te deu Like antes de deslizar e desbloqueia a Descoberta Premium.',
    goldBenefitsTitle: '<i class="fa-solid fa-crown text-amber-400"></i> Vantagens Incluídas no Gold',
    goldBenefits: [
      '<strong>Vê quem gostou de ti:</strong> galeria completa de todos os teus likes.',
      '<strong>Top Picks diários:</strong> seleções baseadas na tua sintonia e compatibilidade.',
      '<strong>Swipes e Likes ilimitados:</strong> sem limites de cartões diários.',
      '<strong>Rebobinar (Undo) ilimitado:</strong> volta atrás sempre que quiseres.',
      '<strong>5 Super Likes semanais</strong> e 1 Boost mensal gratuito.'
    ],
    plusTitle: 'Swipes ilimitados e Modo Incógnito',
    plusDesc: 'Controla quem te vê, ativa o modo incógnito e conecta-te sem barreiras.',
    plusBenefitsTitle: '<i class="fa-solid fa-bolt text-red-500"></i> Vantagens Incluídas no Plus',
    plusBenefits: [
      '<strong>Modo Incógnito:</strong> só ficas visível para as pessoas a quem deres Like.',
      '<strong>Likes ilimitados:</strong> desliza à direita sem restrições.',
      '<strong>Rebobinar ilimitado:</strong> desfaz o teu último deslize se mudares de ideias.',
      '<strong>Passaporte:</strong> muda a tua localização para onde quiseres.',
      '<strong>Sem anúncios nem interrupções:</strong> experiência rápida e discreta.'
    ],
    btnConfirm: 'Confirmar e Obter Sigaleve'

  },
  br: {
    dur1m: '1 Mês', dur6m: '6 Meses', dur12m: '12 Meses',
    perMonth: '/mês', monthlyPay: 'pagamento mensal',
    badgeVip: 'VIP', badgePopular: 'Popular', badgeStandard: 'Padrão', badgeBest: 'Melhor valor',
    save40: 'Economize 40%', save37: 'Economize 37%', save33: 'Economize 33%',
    platTitle: 'Alcance o nível mais exclusivo do Sigaleve',
    platDesc: 'Veja quem curtiu você, Likes prioritários e mensagens diretas antes do match.',
    platBenefitsTitle: '<i class="fa-solid fa-gem text-zinc-300"></i> Vantagens Exclusivas Platinum',
    platBenefits: [
      '<strong>Likes prioritários:</strong> os seus likes aparecem primeiro para todos.',
      '<strong>Mensagens antes do match:</strong> envie uma nota em cada Super Like.',
      '<strong>Veja quem curtiu você:</strong> descubra imediatamente seus admiradores.',
      '<strong>Swipes e Likes ilimitados</strong> no mundo todo.',
      '<strong>Passaporte global:</strong> converse em qualquer cidade do planeta.',
      '<strong>5 Super Likes grátis por semana</strong> e 1 Boost por mês.'
    ],
    goldTitle: 'Veja quem curtiu você e muito mais',
    goldDesc: 'Descubra quem deu Like em você antes de deslizar e desbloqueie a Descoberta Premium.',
    goldBenefitsTitle: '<i class="fa-solid fa-crown text-amber-400"></i> Vantagens Incluídas no Gold',
    goldBenefits: [
      '<strong>Veja quem curtiu você:</strong> galeria completa de todos os seus likes.',
      '<strong>Top Picks diários:</strong> seleções baseadas na sua sintonia e compatibilidade.',
      '<strong>Swipes e Likes ilimitados:</strong> sem limites de cards diários.',
      '<strong>Voltar Atrás ilimitado:</strong> desfaça o swipe sempre que quiser.',
      '<strong>5 Super Likes semanais</strong> e 1 Boost mensal grátis.'
    ],
    plusTitle: 'Swipes ilimitados e Modo Anônimo',
    plusDesc: 'Controle quem vê você, ative o modo anônimo e conecte-se sem barreiras.',
    plusBenefitsTitle: '<i class="fa-solid fa-bolt text-red-500"></i> Vantagens Incluídas no Plus',
    plusBenefits: [
      '<strong>Modo Anônimo:</strong> você só fica visível para quem der Like.',
      '<strong>Likes ilimitados:</strong> deslize para a direita sem restrições.',
      '<strong>Voltar Atrás ilimitado:</strong> desfaça seu último swipe se mudar de ideia.',
      '<strong>Passaporte:</strong> mude sua localização para onde quiser.',
      '<strong>Sem anúncios nem interrupções:</strong> experiência rápida e discreta.'
    ],
    btnConfirm: 'Confirmar e Obter Sigaleve'

  },
  en: {
    dur1m: '1 Month', dur6m: '6 Months', dur12m: '12 Months',
    perMonth: '/mo', monthlyPay: 'monthly payment',
    badgeVip: 'VIP', badgePopular: 'Popular', badgeStandard: 'Standard', badgeBest: 'Best value',
    save40: 'Save 40%', save37: 'Save 37%', save33: 'Save 33%',
    platTitle: 'Unlock the most exclusive level of Sigaleve',
    platDesc: 'See who liked you, Priority likes, and direct notes before matching.',
    platBenefitsTitle: '<i class="fa-solid fa-gem text-zinc-300"></i> Platinum Exclusive Perks',
    platBenefits: [
      '<strong>Priority likes:</strong> your profile is seen first by everyone you like.',
      '<strong>Message before matching:</strong> add a note to every Super Like.',
      '<strong>See who liked you:</strong> reveal all secret admirers immediately.',
      '<strong>Unlimited swipes & likes</strong> worldwide.',
      '<strong>Global passport:</strong> connect and chat in any city on Earth.',
      '<strong>5 free Super Likes per week</strong> and 1 free monthly Boost.'
    ],
    goldTitle: 'See who liked you & more',
    goldDesc: 'Discover who liked you before swiping and unlock Premium Discovery.',
    goldBenefitsTitle: '<i class="fa-solid fa-crown text-amber-400"></i> Perks Included in Gold',
    goldBenefits: [
      '<strong>See who liked you:</strong> full gallery of your admirers.',
      '<strong>Daily Top Picks:</strong> curated picks matching your vibe & compatibility.',
      '<strong>Unlimited swipes and likes:</strong> no daily card limits.',
      '<strong>Unlimited rewind (Undo):</strong> step back whenever you wish.',
      '<strong>5 weekly Super Likes</strong> and 1 monthly Boost.'
    ],
    plusTitle: 'Unlimited Swipes & Incognito Mode',
    plusDesc: 'Control who sees you, turn on incognito and connect without limits.',
    plusBenefitsTitle: '<i class="fa-solid fa-bolt text-red-500"></i> Perks Included in Plus',
    plusBenefits: [
      '<strong>Incognito mode:</strong> only visible to people you have liked.',
      '<strong>Unlimited likes:</strong> swipe right freely.',
      '<strong>Unlimited rewind:</strong> undo your last swipe anytime.',
      '<strong>Passport:</strong> teleport anywhere on the map.',
      '<strong>Ad-free & uninterrupted:</strong> smooth and discrete experience.'
    ],
    btnConfirm: 'Confirm and Get Sigaleve'

  },
  it: {
    dur1m: '1 Mese', dur6m: '6 Mesi', dur12m: '12 Mesi',
    perMonth: '/mese', monthlyPay: 'pagamento mensile',
    badgeVip: 'VIP', badgePopular: 'Popolare', badgeStandard: 'Standard', badgeBest: 'Miglior valore',
    save40: 'Risparmia il 40%', save37: 'Risparmia il 37%', save33: 'Risparmia il 33%',
    platTitle: 'Raggiungi il livello più esclusivo di Sigaleve',
    platDesc: 'Guarda a chi piaci, Mi Piace prioritari e note dirette prima di fare match.',
    platBenefitsTitle: '<i class="fa-solid fa-gem text-zinc-300"></i> Vantaggi Esclusivi Platinum',
    platBenefits: [
      '<strong>Mi Piace prioritari:</strong> il tuo profilo viene visualizzato per primo dalle persone a cui piaci.',
      '<strong>Messaggi prima del match:</strong> aggiungi una nota a ogni Super Like.',
      '<strong>Guarda a chi piaci:</strong> scopri subito tutti i tuoi ammiratori segreti.',
      '<strong>Swipe e Mi Piace illimitati</strong> in tutto il mondo.',
      '<strong>Passaporto globale:</strong> connettiti e chatta in qualunque città del mondo.',
      '<strong>5 Super Like gratuiti a settimana</strong> e 1 Boost gratuito al mese.'
    ],
    goldTitle: 'Guarda a chi piaci e molto altro',
    goldDesc: 'Scopri chi ti ha messo Mi Piace prima di scorrere e sblocca la Scoperta Premium.',
    goldBenefitsTitle: '<i class="fa-solid fa-crown text-amber-400"></i> Vantaggi Inclusi in Gold',
    goldBenefits: [
      '<strong>Guarda a chi piaci:</strong> galleria completa di tutti i tuoi ammiratori.',
      '<strong>Top Picks giornalieri:</strong> selezioni su misura per la tua sintonia e affinità.',
      '<strong>Swipe e Mi Piace illimitati:</strong> nessun limite giornaliero di profili.',
      '<strong>Annulla (Undo) illimitato:</strong> torna indietro ogni volta che desideri.',
      '<strong>5 Super Like settimanali</strong> e 1 Boost mensile gratuito.'
    ],
    plusTitle: 'Swipe Illimitati e Modalità Incognito',
    plusDesc: 'Controlla chi ti vede, attiva la modalità incognito e connettiti senza limiti.',
    plusBenefitsTitle: '<i class="fa-solid fa-bolt text-red-500"></i> Vantaggi Inclusi in Plus',
    plusBenefits: [
      '<strong>Modalità Incognito:</strong> visibile solo per le persone a cui hai messo Mi Piace.',
      '<strong>Mi Piace illimitati:</strong> scorri a destra senza alcuna restrizione.',
      '<strong>Annulla illimitato:</strong> annulla il tuo ultimo swipe se cambi idea.',
      '<strong>Passaporto:</strong> cambia la tua posizione ovunque nel mondo.',
      '<strong>Senza pubblicità né interruzioni:</strong> esperienza fluida e riservata.'
    ],
    btnConfirm: 'Conferma e Ottieni Sigaleve'

  },
  fr: {
    dur1m: '1 Mois', dur6m: '6 Mois', dur12m: '12 Mois',
    perMonth: '/mois', monthlyPay: 'paiement mensuel',
    badgeVip: 'VIP', badgePopular: 'Populaire', badgeStandard: 'Standard', badgeBest: 'Meilleure offre',
    save40: 'Économisez 40%', save37: 'Économisez 37%', save33: 'Économisez 33%',
    platTitle: 'Accédez au niveau le plus exclusif de Sigaleve',
    platDesc: 'Voyez qui vous a aimé, likes prioritaires et messages avant de matcher.',
    platBenefitsTitle: '<i class="fa-solid fa-gem text-zinc-300"></i> Avantages Exclusifs Platinum',
    platBenefits: [
      '<strong>Likes prioritaires:</strong> apparaissez en premier auprès de vos coups de cœur.',
      '<strong>Messages avant de matcher:</strong> joignez un mot à vos Super Likes.',
      '<strong>Voyez qui vous aime:</strong> accédez immédiatement à votre galerie secrète.',
      '<strong>Swipes et likes illimités</strong> dans le monde entier.',
      '<strong>Passeport mondial:</strong> discutez dans toutes les villes sans bouger.',
      '<strong>5 Super Likes offerts par semaine</strong> et 1 Boost par mois.'
    ],
    goldTitle: 'Voyez qui vous aime et bien plus',
    goldDesc: 'Découvrez qui a liké votre profil avant de swiper et profitez de la découverte premium.',
    goldBenefitsTitle: '<i class="fa-solid fa-crown text-amber-400"></i> Avantages Inclus dans Gold',
    goldBenefits: [
      '<strong>Voyez qui vous aime:</strong> galerie complète de vos admirateurs.',
      '<strong>Top Picks quotidiens:</strong> sélections selon vos affinités et compatibilité.',
      '<strong>Swipes et likes illimités:</strong> aucune limite quotidienne de profils.',
      '<strong>Retour en arrière illimité (Undo):</strong> revenez en arrière à volonté.',
      '<strong>5 Super Likes par semaine</strong> et 1 Boost mensuel gratuit.'
    ],
    plusTitle: 'Swipes illimités et Mode Incognito',
    plusDesc: 'Contrôlez votre visibilité, activez le mode incognito et connectez-vous librement.',
    plusBenefitsTitle: '<i class="fa-solid fa-bolt text-red-500"></i> Avantages Inclus dans Plus',
    plusBenefits: [
      '<strong>Mode Incognito:</strong> visible uniquement par les personnes que vous aimez.',
      '<strong>Likes illimités:</strong> swipez à droite sans restriction.',
      '<strong>Retour en arrière illimité:</strong> annulez votre dernier swipe.',
      '<strong>Passeport:</strong> changez de localisation où vous voulez.',
      '<strong>Sans publicité ni interruption:</strong> navigation fluide et discrète.'
    ],
    btnConfirm: 'Confirmer et Obtenir Sigaleve'
  }
};

function getProductData(tab) {
  const curLang = (typeof window !== 'undefined' && window.LANG && PRODUCT_DATA_I18N[window.LANG]) ? window.LANG : ((typeof LANG !== 'undefined' && PRODUCT_DATA_I18N[LANG]) ? LANG : (localStorage.getItem('sigaleve_lang') || 'pt'));
  const L = PRODUCT_DATA_I18N[curLang] || PRODUCT_DATA_I18N.pt || PRODUCT_DATA_I18N.es;

  return {
    badge: '<i class="fa-solid fa-bolt text-red-400"></i> SIGALEVE PLUS',
    badgeClass: 'bg-gradient-to-r from-red-600 via-pink-600 to-red-700 text-white font-black',
    title: L.plusTitle,
    desc: L.plusDesc,
    plans: [
      { id: 'plus_1m', duration: L.dur1m, price: '14.99', perMonth: '', total: '14,99€', badge: L.badgeStandard },
      { id: 'plus_6m', duration: L.dur6m, price: '9.99', perMonth: L.perMonth, total: '59,94€', badge: L.save33 },
      { id: 'plus_12m', duration: L.dur12m, price: '6.99', perMonth: L.perMonth, total: '83,88€', badge: L.badgeBest }
    ],
    benefitsTitle: L.plusBenefitsTitle,
    benefits: L.plusBenefits,
    btnConfirm: L.btnConfirm,
    btnGrad: 'bg-gradient-to-r from-red-500 via-pink-600 to-purple-600 text-white font-black shadow-lg shadow-pink-600/30'
  };
}

const PRODUCT_DATA = new Proxy({}, {
  get: function(target, prop) {
    return getProductData(prop);
  }
});

function openSubscriptionModal(type) {
  openProductSubscription(type || 'plus');
}

function openProductSubscription(tab) {
  try {
    const modal = document.getElementById('modal-subscription');
    if (!modal) return;
    modal.classList.remove('hidden');
    modal.style.display = 'flex';
    if (typeof hideSubAlert === 'function') hideSubAlert();
    if (typeof closeDrawer === 'function') {
      try { closeDrawer(); } catch (e) {}
    }

  // Actualizar clases de pestañas
  ['plus', 'settings'].forEach(t => {
    const btn = document.getElementById('sub-tab-' + t);
    if (!btn) return;
    if (t === tab) {
      btn.className = 'px-3 py-1.5 rounded-lg text-xs font-black uppercase tracking-wider transition-all bg-zinc-800 text-white shadow-sm flex items-center gap-1';
    } else {
      btn.className = 'px-3 py-1.5 rounded-lg text-xs font-black uppercase tracking-wider transition-all text-zinc-400 hover:text-white flex items-center gap-1';
    }
  });

  const headerSec = document.getElementById('sub-header-section');
  const viewSettings = document.getElementById('sub-view-settings');
  const viewPurchase = document.getElementById('sub-view-purchase');

  if (tab === 'settings') {
    if (headerSec) headerSec.classList.add('hidden');
    if (viewSettings) viewSettings.classList.remove('hidden');
    if (viewPurchase) viewPurchase.classList.add('hidden');
    currentProductTab = 'settings';
    renderSubscriptionSettingsUI();
    return;
  }

  // Pestañas de Compra: platinum, gold, plus
  if (headerSec) headerSec.classList.remove('hidden');
  if (viewSettings) viewSettings.classList.add('hidden');
  if (viewPurchase) viewPurchase.classList.remove('hidden');
  currentProductTab = tab;

  const data = PRODUCT_DATA['plus'];
  
  // Header
  const badgeEl = document.getElementById('sub-product-badge');
  if (badgeEl) {
    badgeEl.className = 'inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-black uppercase tracking-widest mb-2 shadow-md ' + data.badgeClass;
    badgeEl.innerHTML = data.badge;
  }
  const titleEl = document.getElementById('sub-product-title');
  if (titleEl) titleEl.textContent = data.title;
  const descEl = document.getElementById('sub-product-desc');
  if (descEl) descEl.textContent = data.desc;

  // Beneficios
  const bTitle = document.getElementById('sub-benefits-title');
  if (bTitle) bTitle.innerHTML = data.benefitsTitle;
  const bList = document.getElementById('sub-benefits-list');
  if (bList) {
    bList.innerHTML = data.benefits.map(b => `<li class="flex items-start gap-2"><i class="fa-solid fa-check text-emerald-400 text-sm mt-0.5"></i> <span>${b}</span></li>`).join('');
  }

  // Tarjetas de duración
  const grid = document.getElementById('subscription-plans-grid');
  if (grid) {
    grid.innerHTML = data.plans.map((p, idx) => {
      const isAct = idx === 2; // Por defecto 12 meses
      if (isAct) {
        selectedPlanId = p.id;
        selectedPlanPrice = p.total.replace('€', '').trim();
        selectedPlanTitle = p.duration;
      }
      return `
        <div onclick="selectPlan('${p.id}', '${p.price}', '${p.duration}', '${p.total}')" id="plan-card-${p.id}" class="plan-card ${isAct ? 'active' : ''} p-3 rounded-2xl border-2 text-center cursor-pointer transition-all relative flex flex-col justify-between bg-zinc-900 ${isAct ? 'border-purple-500 shadow-sm' : 'border-zinc-800 hover:border-zinc-700'}">
          <span class="absolute -top-2.5 left-1/2 -translate-x-1/2 text-[9px] font-black uppercase ${isAct ? 'bg-amber-400 text-black font-extrabold' : 'bg-zinc-700 text-white'} px-2 py-0.5 rounded-full shadow">${p.badge}</span>
          <p class="text-xs font-black mt-1 text-white">${p.duration}</p>
          <div class="my-2">
            <span class="text-lg font-black text-white">${p.price.replace('.', ',')}€</span>
            ${p.perMonth ? `<span class="text-[10px] block text-zinc-400">${p.perMonth}</span>` : ''}
          </div>
          <p class="text-[10px] text-zinc-400">total ${p.total}</p>
        </div>
      `;
    }).join('');
  }

  // Actualizar resumen y botón de submit
  const defaultTotal = data.plans[2] ? data.plans[2].total : (data.plans[0] ? data.plans[0].total : '0,00€');
  const defaultDuration = data.plans[2] ? data.plans[2].duration : (data.plans[0] ? data.plans[0].duration : '');
  const sumEl = document.getElementById('pay-summary-amount');
  if (sumEl) sumEl.textContent = defaultTotal;
  const btn = document.getElementById('btn-pay-submit');
  if (btn) {
    btn.className = 'w-full py-4 rounded-2xl text-xs font-black tracking-wider uppercase shadow-xl flex items-center justify-center gap-2 hover:opacity-95 active:scale-[0.99] transition-all ' + data.btnGrad;
    const baseAction = data.btnConfirm || 'Confirmar e Obter Sigaleve';
    const btnTextEl = document.getElementById('btn-pay-text');
    if (btnTextEl) {
      btnTextEl.textContent = `${baseAction} (${defaultDuration} • ${defaultTotal})`;
    }
  }
} catch (err) {
  console.error('Error in openProductSubscription:', err);
}
}

function openSubscriptionSettings() {
  openProductSubscription('settings');
}

function closeSubscriptionModal() {
  const modal = document.getElementById('modal-subscription');
  if (modal) {
    modal.classList.add('hidden');
    modal.style.display = 'none';
  }
}

function selectPlan(planId, price, title, total) {
  selectedPlanId = planId;
  const totalDisplay = total || (price ? price.replace('.', ',') + '€' : '');
  selectedPlanPrice = totalDisplay.replace('€', '').trim();
  selectedPlanTitle = title;

  document.querySelectorAll('#subscription-plans-grid .plan-card').forEach(card => {
    if (card.id === 'plan-card-' + planId) {
      card.classList.add('active');
      card.classList.remove('border-zinc-800');
      card.classList.add('border-purple-500');
    } else {
      card.classList.remove('active');
      card.classList.add('border-zinc-800');
      card.classList.remove('border-purple-500');
    }
  });

  const sumEl = document.getElementById('pay-summary-amount');
  if (sumEl) sumEl.textContent = totalDisplay;

  const btnText = document.getElementById('btn-pay-text');
  if (btnText) {
    const data = PRODUCT_DATA['plus'];
    const baseAction = data.btnConfirm || 'Confirmar e Obter Sigaleve';
    btnText.textContent = `${baseAction} (${title} • ${totalDisplay})`;
  }
}

function formatCardNumber(input) {
  let v = input.value.replace(/\D/g, '');
  if (v.length > 16) v = v.substring(0, 16);
  const parts = [];
  for (let i = 0; i < v.length; i += 4) {
    parts.push(v.substring(i, i + 4));
  }
  input.value = parts.join(' ');
}

function formatCardExp(input) {
  let v = input.value.replace(/\D/g, '');
  if (v.length > 4) v = v.substring(0, 4);
  if (v.length >= 3) {
    input.value = v.substring(0, 2) + '/' + v.substring(2);
  } else {
    input.value = v;
  }
}

function showSubAlert(msg, isSuccess = false) {
  const el = document.getElementById('sub-pay-alert');
  if (!el) return;
  el.className = isSuccess
    ? 'p-3 rounded-xl text-xs font-bold text-center bg-emerald-500/20 text-emerald-400 border border-emerald-500/40'
    : 'p-3 rounded-xl text-xs font-bold text-center bg-red-500/20 text-red-400 border border-red-500/40';
  el.innerHTML = isSuccess ? `<i class="fa-solid fa-circle-check mr-1.5"></i> ${msg}` : `<i class="fa-solid fa-triangle-exclamation mr-1.5"></i> ${msg}`;
  el.classList.remove('hidden');
}

function hideSubAlert() {
  const el = document.getElementById('sub-pay-alert');
  if (el) el.classList.add('hidden');
}

function renderSubscriptionSettingsUI() {
  const user = STATE.currentUser || {};
  const sub = user.subscription;
  const isSubActive = !!(user.is_plus && sub && sub.active);

  const freeBox = document.getElementById('sub-state-free');
  const activeBox = document.getElementById('sub-state-active');

  if (!isSubActive) {
    if (freeBox) freeBox.classList.remove('hidden');
    if (activeBox) activeBox.classList.add('hidden');
  } else {
    if (freeBox) freeBox.classList.add('hidden');
    if (activeBox) activeBox.classList.remove('hidden');

    const planTitle = document.getElementById('sub-current-plan-title');
    if (planTitle) planTitle.textContent = sub.plan_name || 'Sigaleve Plus';

    const nextBilling = document.getElementById('sub-current-next-billing');
    if (nextBilling) nextBilling.textContent = sub.next_billing || '28 de Outubro, 2026';

    const cardSummary = document.getElementById('sub-card-summary');
    if (cardSummary) cardSummary.textContent = `${sub.card_brand || 'Cartão'} terminado em ${sub.card_last4 || '0000'}`;

    const cardExp = document.getElementById('sub-card-exp-summary');
    if (cardExp) cardExp.textContent = `Expira ${sub.card_exp || 'MM/AA'}`;
  }
}

async function cancelSubscriptionPrompt() {
  showAppConfirm(
    'Cancelar Subscrição',
    'Tens a certeza de que desejas cancelar a tua subscrição? Perderás o acesso aos Likes ilimitados e prioridade.',
    async () => {
      try {
        const res = await fetch('/api/v1/subscription/cancel', { method: 'POST' });
        const data = await res.json();
        if (res.ok && data.success) {
          if (STATE.currentUser) {
            STATE.currentUser.is_plus = false;
            STATE.currentUser.subscription = null;
          }
          renderSubscriptionSettingsUI();
          showAppToast('Subscrição cancelada com sucesso. O teu perfil está agora no plano gratuito.', 'info');
        } else {
          showAppToast(data.error || 'Erro ao cancelar subscrição.', 'error');
        }
      } catch (err) {
        showAppToast('Erro de comunicação com o servidor.', 'error');
      }
    }
  );
}

async function handleSubscriptionPayment(e) {
  e.preventDefault();
  hideSubAlert();

  // 💳 MB WAY MANUAL: gera referência e mostra instruções. O usuário paga
  // no telemóvel; o dono confirma no painel /admin/payments e a subscrição
  // ativa sozinha (o modal faz polling do estado).
  const btn = document.getElementById('btn-pay-submit');
  btn.disabled = true;
  const originalHtml = btn.innerHTML;
  btn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> A gerar referência...';

  try {
    const res = await fetch('/api/v1/subscription/mbway-request', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ plan_id: selectedPlanId })
    });
    const data = await res.json();
    if (res.ok && data.success) {
      showMbwayInstructions(data);
    } else {
      showSubAlert(data.error || 'Não foi possível gerar a referência de pagamento.');
    }
  } catch (err) {
    showSubAlert('Erro de ligação com o servidor.');
  } finally {
    btn.disabled = false;
    btn.innerHTML = originalHtml;
  }
}

// ── MB WAY: instruções + polling do estado da referência ──
let mbwayPollTimer = null;

function showMbwayInstructions(data) {
  const form = document.getElementById('payment-form') || document.getElementById('pay-card-holder')?.closest('form');
  if (!form) return;
  const passos = (data.instructions || []).map(p => `<li style="margin-bottom:6px">${p}</li>`).join('');
  form.innerHTML = `
    <div style="text-align:center;padding:8px 4px">
      <i class="fa-solid fa-mobile-screen-button" style="font-size:34px;color:#22c55e"></i>
      <h3 style="font-weight:800;font-size:15px;margin:10px 0 4px">Paga com MB Way</h3>
      <p style="font-size:12px;color:#a1a1aa;margin-bottom:12px">Plano: <b>${data.plan_name}</b> • Valor: <b style="color:#22c55e">${data.price}</b></p>
      <div style="background:#052e16;border:1px solid #22c55e44;border-radius:14px;padding:14px;margin-bottom:14px">
        <p style="font-size:10px;letter-spacing:2px;color:#86efac;font-weight:800;margin-bottom:4px">REFERÊNCIA</p>
        <p id="mbway-ref-display" style="font-size:22px;font-weight:900;letter-spacing:3px;color:#fff;font-family:monospace">${data.reference}</p>
      </div>
      <ol style="text-align:left;font-size:12px;color:#d4d4d8;padding-left:18px;margin-bottom:14px">${passos}</ol>
      <div id="mbway-waiting" style="display:flex;align-items:center;justify-content:center;gap:8px;font-size:12px;color:#a1a1aa">
        <i class="fa-solid fa-circle-notch fa-spin"></i> À espera do pagamento... ativa automaticamente quando confirmares.
      </div>
    </div>`;
  // polling a cada 6s; ao confirmar, recarrega o estado do usuário
  clearInterval(mbwayPollTimer);
  mbwayPollTimer = setInterval(async () => {
    try {
      const r = await fetch(`/api/v1/subscription/mbway-status?ref=${encodeURIComponent(data.reference)}`, { credentials: 'include' });
      const d = await r.json();
      if (d.success && d.status === 'paid') {
        clearInterval(mbwayPollTimer);
        const me = await fetch('/api/v1/auth/me', { credentials: 'include' }).then(x => x.json()).catch(() => null);
        if (me && me.user) {
          STATE.currentUser = me.user;
          updateProfileUI(me.user);
        }
        showSubAlert('Pagamento confirmado! A tua subscrição já está ativa. 🎉', true);
        setTimeout(() => { closeSubscriptionModal(); showAppToast('🎉 Subscrição Sigaleve ativa!', 'success'); }, 1400);
      }
    } catch (_) {}
  }, 6000);
}
