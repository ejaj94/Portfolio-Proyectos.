# ============================================================
# SIGALEVE — VOZES EM CÍRCULO (Roda Terapêutica Circular de 6 Lugares — 100% EFÉMERA)
# ============================================================
# Arquitetura Senior de Roda Terapêutica & Escuta Ativa (Máx. 6 Pessoas por Roda):
#   - 4 salas ao vivo (3 temáticas + 1 Sala Demo Interativa para demonstração ao vivo):
#     1. "Primeiros Passos & Aceitação"
#     2. "Coragem, Encontros & Recomeços"
#     3. "Noite de Desabafo & Escuta Livre"
#     4. "Roda Demo Interativa (6/6 ao Vivo)" — Simula uma roda completa com 5 membros
#        de demonstração + o utilizador, mostrando em tempo real a mesa circular de 6
#        lugares, avatares brancos (ouvintes) vs verde esmeralda (com o Bastão da Palavra),
#        check-ins emocionais, reações nos cantos dos avatares, "Abraço Coletivo",
#        passagem animada do Bastão e ritual de libertação antes do apagamento total.
#   - Capacidade Máxima Estrita: 6 lugares (cadeiras 0 a 5) por roda.
#   - Exclusividade de Sala: Cada utilizador só pode estar numa única roda de cada vez.
#   - Escrita Exclusiva por Turno: Apenas quem tem o Bastão da Palavra (avatar verde)
#     pode escrever e enviar mensagens no chat efémero.
#   - DESTRUIÇÃO AUTOMÁTICA TOTAL (Zero-Storage):
#     Ao concluir o turno ("Concluir Partilha", "Passar a Vez" ou fim dos 3 minutos),
#     é gerado um resumo breve do Ritual de Acolhimento (visível por 4 segundos) e
#     TODAS as mensagens e reações são apagadas da RAM sem deixar rasto.
#   - Anonimato 100% Obrigatório ("Membro Anónimo #XXXX").
# ============================================================
import time as _time
import uuid as _uuid
import hashlib as _hashlib
import threading as _threading
from flask import request as _request, jsonify as _jsonify

VOICES_LOCK = _threading.Lock()

MAX_SEATS_PER_ROOM = 6           # Máximo estrito de 6 pessoas por roda do círculo
TURN_DURATION_SECONDS = 180      # 3 minutos por turno / sessão de roda
EXTEND_BONUS_SECONDS = 60        # +1 minuto extra (máx. 1 vez por turno)
MAX_MESSAGES_PER_ROOM = 100      # Máximo em RAM apenas durante o turno ativo

ROOMS_CATALOG = [
    {
        "id": "aceitacao",
        "title": "Primeiros Passos & Aceitação",
        "subtitle": "Para quem recebeu um diagnóstico recentemente ou procura paz interior sem julgamentos.",
        "emoji": "🌱",
        "badge": "Acolhimento & Calma",
        "theme_color": "#10b981",
        "prompt_of_day": "O que mais te ajudou (ou o que mais precisas ouvir hoje) para respirar fundo e seguir leve?",
        "is_demo": False,
    },
    {
        "id": "recomecos",
        "title": "Coragem, Encontros & Recomeços",
        "subtitle": "Partilha vitórias, receios de voltar a namorar, conversas honestas e histórias de superação.",
        "emoji": "💜",
        "badge": "Progresso & Amor-Próprio",
        "theme_color": "#a855f7",
        "prompt_of_day": "Qual foi um pequeno progresso recente de que te orgulhas na tua jornada pessoal ou afetiva?",
        "is_demo": False,
    },
    {
        "id": "desabafo",
        "title": "Noite de Desabafo & Escuta Livre",
        "subtitle": "Como te sentes neste exato momento? O círculo de 6 pessoas escuta em silêncio e acolhe a tua voz.",
        "emoji": "🕯️",
        "badge": "Escuta Empática 24h",
        "theme_color": "#ec4899",
        "prompt_of_day": "Se pudesses deixar um peso fora dos ombros agora mesmo, o que dirias ao círculo?",
        "is_demo": False,
    },
    {
        "id": "demo_roda",
        "title": "Roda Demo ao Vivo (6 Lugares)",
        "subtitle": "Sala de demonstração interativa com 6 participantes em círculo, reações ao vivo, passagem do Bastão e ritual efémero.",
        "emoji": "✨",
        "badge": "Demo Interativa 6/6",
        "theme_color": "#10b981",
        "prompt_of_day": "Bem-vindo à Roda Demo! Experimenta receber o Bastão Verde, ativar o Abraço Coletivo ou ver o Bastão girar na roda.",
        "is_demo": True,
    },
]

REACTION_TYPES = {
    "contigo": {"emoji": "🤍", "label": "Estou contigo"},
    "forca": {"emoji": "🌱", "label": "Força & Progresso"},
    "abraco": {"emoji": "🫂", "label": "Abraço Silencioso"},
    "gratidao": {"emoji": "✨", "label": "Obrigado por partilhares"},
}

MOOD_TYPES = {
    "escuta": {"emoji": "🤍", "label": "Apenas a escutar"},
    "esperancoso": {"emoji": "🌱", "label": "Esperançoso/a"},
    "ansioso": {"emoji": "🌊", "label": "Ansioso/a"},
    "cansado": {"emoji": "🌧️", "label": "Cansado/a"},
    "empaz": {"emoji": "🕯️", "label": "Em paz"},
}

# Participantes simulados exclusivos para a sala `demo_roda` (ocupam até 5 cadeiras para deixar 1 lugar ao utilizador real)
DEMO_BOT_PROFILES = [
    {
        "user_id": "demo_bot_1",
        "alias": "Membro Anónimo #4821",
        "mood": "esperancoso",
        "default_reaction": "abraco",
        "sample_messages": [
            "Olá roda... durante meses tive receio de falar sobre o meu diagnóstico, mas estar aqui convosco faz-me sentir finalmente compreendido. 🌱",
            "Hoje consegui ter uma conversa honesta com alguém especial e correu muito melhor do que o meu medo dizia. Não desistam de vocês! 💚",
            "Obrigado a todos pelos abraços silenciosos que estou a ver nos vossos ícones da roda. Sabe mesmo bem não falar para o vazio. ✨",
        ],
    },
    {
        "user_id": "demo_bot_2",
        "alias": "Membro Anónimo #7390",
        "mood": "empaz",
        "default_reaction": "contigo",
        "sample_messages": [
            "Respirei fundo antes de começar... Queria partilhar que aprender a aceitar o meu tempo mudou a forma como me olho ao espelho. 🕯️",
            "Ver esta roda de 6 pessoas unida em silêncio e respeito dá-me uma paz enorme ao fim do dia.",
        ],
    },
    {
        "user_id": "demo_bot_3",
        "alias": "Membro Anónimo #2154",
        "mood": "ansioso",
        "default_reaction": "forca",
        "sample_messages": [
            "Hoje o coração estava um pouco apertado com receio do futuro, mas ouvir as vossas partilhas lembrou-me que passo a passo tudo acalma. 🌊🌱",
        ],
    },
    {
        "user_id": "demo_bot_4",
        "alias": "Membro Anónimo #9042",
        "mood": "escuta",
        "default_reaction": "gratidao",
        "sample_messages": [
            "Estou sobretudo em escuta ativa hoje, mas quis pegar no Bastão um instante para agradecer a coragem de cada um nesta roda. ✨",
        ],
    },
    {
        "user_id": "demo_bot_5",
        "alias": "Membro Anónimo #6188",
        "mood": "cansado",
        "default_reaction": "abraco",
        "sample_messages": [
            "Semana longa, mas sentar-me nesta roda convosco tira-me um peso enorme dos ombros. Obrigado pelo acolhimento sem julgamentos. 🫂",
        ],
    },
]


def _anon_alias_for(user_id: str) -> str:
    for b in DEMO_BOT_PROFILES:
        if b["user_id"] == user_id:
            return b["alias"]
    digest = _hashlib.sha256(f"sigaleve-circle-{user_id}".encode("utf-8")).hexdigest()
    num = int(digest[:6], 16) % 9000 + 1000
    return f"Membro Anónimo #{num}"


# Armazenamento 100% EFÉMERO em RAM (NUNCA gravado em disco)
_EPHEMERAL_STORE = {"rooms": {}}


def _create_empty_room_state(rid: str) -> dict:
    return {
        "id": rid,
        "active_speaker": None,       # {user_id, alias, avatar, is_anonymous, started_at, ends_at, extended}
        "queue": [],                  # [{user_id, alias, avatar, is_anonymous, requested_at}]
        "listeners": {},              # {user_id: {"alias": ..., "last_seen": ts, "mood": "escuta", "seat_idx": int}}
        "live_reactions": dict(contigo=0, forca=0, abraco=0, gratidao=0),
        "live_reactions_by_user": {}, # {user_id: "contigo" | "forca" | "abraco" | "gratidao"}
        "messages": [],               # 100% vazio no início e limpo ao terminar cada turno
        "last_wiped_at": None,
        "last_handoff": None,         # {"from_alias", "to_alias", "from_uid", "to_uid", "reason", "at"}
        "last_release_ritual": None,  # {"speaker_alias", "total_reactions", "breakdown", "reason", "at"}
    }


def _populate_demo_room(rm: dict, now: float):
    """Inicializa ou restaura a Sala Demo Interativa (`demo_roda`) com 5 participantes simulados,
    deixando sempre a 6.ª cadeira livre para o utilizador testar tudo em tempo real."""
    rm["listeners"] = {}
    for idx, bot in enumerate(DEMO_BOT_PROFILES):
        b_uid = bot["user_id"]
        rm["listeners"][b_uid] = {
            "alias": bot["alias"],
            "last_seen": now + 86400,  # Sempre presente na sala de demo
            "mood": bot["mood"],
            "seat_idx": idx,
            "is_demo_bot": True,
        }

    # Colocar o primeiro bot como orador inicial com o Bastão Verde e outros 2 na fila
    speaker_bot = DEMO_BOT_PROFILES[0]
    rm["active_speaker"] = {
        "user_id": speaker_bot["user_id"],
        "alias": speaker_bot["alias"],
        "avatar": "",
        "is_anonymous": True,
        "started_at": now - 12,
        "ends_at": now + TURN_DURATION_SECONDS - 12,
        "extended": False,
    }
    rm["queue"] = [
        {
            "user_id": DEMO_BOT_PROFILES[1]["user_id"],
            "alias": DEMO_BOT_PROFILES[1]["alias"],
            "avatar": "",
            "is_anonymous": True,
            "requested_at": now - 10,
        },
        {
            "user_id": DEMO_BOT_PROFILES[2]["user_id"],
            "alias": DEMO_BOT_PROFILES[2]["alias"],
            "avatar": "",
            "is_anonymous": True,
            "requested_at": now - 5,
        },
    ]

    # Ativar reações silenciosas nos cantos dos avatares brancos para demonstrar o "Abraço Coletivo"
    rm["live_reactions_by_user"] = {
        DEMO_BOT_PROFILES[1]["user_id"]: "contigo",
        DEMO_BOT_PROFILES[2]["user_id"]: "forca",
        DEMO_BOT_PROFILES[3]["user_id"]: "gratidao",
        DEMO_BOT_PROFILES[4]["user_id"]: "abraco",
    }
    rm["live_reactions"] = {"contigo": 1, "forca": 1, "abraco": 1, "gratidao": 1}

    # Mensagens de exemplo do turno atual do orador verde
    rm["messages"] = [
        {
            "id": f"vc_sys_{_uuid.uuid4().hex[:8]}",
            "speaker_id": "system",
            "speaker_alias": "Círculo Sigaleve",
            "speaker_avatar": "",
            "is_anonymous": True,
            "kind": "system",
            "text": f"🌿 {speaker_bot['alias']} recebeu o Bastão da Palavra (3 min). A roda escuta em silêncio e todas as mensagens serão libertadas no fim do turno.",
            "reactions": {"contigo": 0, "forca": 0, "abraco": 0, "gratidao": 0},
            "reacted_by": {},
            "created_at": now - 11,
        },
        {
            "id": f"vc_demo_{_uuid.uuid4().hex[:8]}",
            "speaker_id": speaker_bot["user_id"],
            "speaker_alias": speaker_bot["alias"],
            "speaker_avatar": "",
            "is_anonymous": True,
            "kind": "share",
            "text": speaker_bot["sample_messages"][0],
            "reactions": {"contigo": 2, "forca": 1, "abraco": 2, "gratidao": 1},
            "reacted_by": {},
            "created_at": now - 8,
        },
        {
            "id": f"vc_demo_{_uuid.uuid4().hex[:8]}",
            "speaker_id": speaker_bot["user_id"],
            "speaker_alias": speaker_bot["alias"],
            "speaker_avatar": "",
            "is_anonymous": True,
            "kind": "share",
            "text": speaker_bot["sample_messages"][1],
            "reactions": {"contigo": 1, "forca": 2, "abraco": 3, "gratidao": 1},
            "reacted_by": {},
            "created_at": now - 3,
        },
    ]


def _init_ephemeral_rooms():
    now = _time.time()
    for r in ROOMS_CATALOG:
        rid = r["id"]
        if rid not in _EPHEMERAL_STORE["rooms"]:
            rm = _create_empty_room_state(rid)
            if r.get("is_demo"):
                _populate_demo_room(rm, now)
            _EPHEMERAL_STORE["rooms"][rid] = rm


_init_ephemeral_rooms()


def init_voices_circle(
    app,
    socketio,
    session,
    load_json_store,
    save_json_store,
    load_users,
    validate_content_privacy_fn,
):
    """Inicializa as rotas HTTP e eventos Socket.IO do 'Vozes em Círculo' (Mesa Circular de 6 Lugares)."""
    lock = VOICES_LOCK

    # Remover qualquer ficheiro antigo em disco para garantir zero rasto histórico
    try:
        import os as _os
        old_file = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "data", "voices_circle_store.json")
        if _os.path.exists(old_file):
            _os.remove(old_file)
    except Exception:
        pass

    def _load():
        _init_ephemeral_rooms()
        return _EPHEMERAL_STORE

    def _resolve_member_identity(user_id: str, _is_anonymous: bool = True):
        """O anonimato em Vozes em Círculo é 100% obrigatório (sem opção de revelar perfil)."""
        return _anon_alias_for(user_id), ""

    def _recalculate_live_reactions(room_state: dict):
        counts = dict(contigo=0, forca=0, abraco=0, gratidao=0)
        by_user = room_state.get("live_reactions_by_user") or {}
        listeners = room_state.get("listeners") or {}
        active = room_state.get("active_speaker")
        active_uid = active.get("user_id") if active else None

        valid_by_user = {}
        for u, rx in list(by_user.items()):
            # Orador ativo tem o Bastão Verde; as reações silenciosas nos cantos pertencem aos ouvintes brancos
            if rx in counts and (u in listeners or u == active_uid):
                valid_by_user[u] = rx
                counts[rx] += 1
        room_state["live_reactions_by_user"] = valid_by_user
        room_state["live_reactions"] = counts

    def _record_release_ritual_and_wipe(room_state: dict, now: float, reason: str = "completed"):
        """Regista o resumo do Ritual de Libertação & Acolhimento (visível durante 4s) e apaga TODO o chat da RAM."""
        active = room_state.get("active_speaker")
        speaker_alias = active.get("alias", "Membro Anónimo") if active else "Membro Anónimo"

        # Somar apoios silenciosos recebidos na roda + nas mensagens do turno
        rx_totals = dict(contigo=0, forca=0, abraco=0, gratidao=0)
        live_rx = room_state.get("live_reactions") or {}
        for k in rx_totals:
            rx_totals[k] += int(live_rx.get(k, 0))
        for m in room_state.get("messages", []):
            m_rx = m.get("reactions") or {}
            for k in rx_totals:
                rx_totals[k] += int(m_rx.get(k, 0))

        total_support = sum(rx_totals.values())
        share_count = sum(1 for m in room_state.get("messages", []) if m.get("kind") == "share")

        room_state["last_release_ritual"] = {
            "id": f"ritual_{_uuid.uuid4().hex[:8]}",
            "speaker_alias": speaker_alias,
            "total_reactions": total_support,
            "share_count": share_count,
            "breakdown": rx_totals,
            "reason": reason,  # "completed" | "passed" | "timeout"
            "at": now,
        }

        # Destruição total das mensagens e reações (Zero-Storage)
        room_state["messages"] = []
        room_state["live_reactions"] = dict(contigo=0, forca=0, abraco=0, gratidao=0)
        room_state["live_reactions_by_user"] = {}
        room_state["last_wiped_at"] = now

    def _find_committed_room(data: dict, uid: str):
        """Verifica se o utilizador já tem o Bastão da Palavra ou está na fila noutra roda (ignorando a sala demo)."""
        for r in ROOMS_CATALOG:
            rid = r["id"]
            if r.get("is_demo"):
                continue
            rm = data["rooms"][rid]
            act = rm.get("active_speaker")
            if act and act.get("user_id") == uid:
                return rid, r["title"], "speaker"
            if any(q.get("user_id") == uid for q in rm.get("queue", [])):
                return rid, r["title"], "queue"
        return None, None, None

    def _assign_seat_index(rm_target: dict, uid: str) -> int:
        listeners = rm_target.get("listeners") or {}
        if uid in listeners and isinstance(listeners[uid].get("seat_idx"), int):
            return listeners[uid]["seat_idx"]
        used_seats = {
            info.get("seat_idx")
            for u, info in listeners.items()
            if u != uid and isinstance(info.get("seat_idx"), int)
        }
        for s_idx in range(MAX_SEATS_PER_ROOM):
            if s_idx not in used_seats:
                return s_idx
        return 0

    def _enforce_single_room_presence(data: dict, uid: str, target_room_id: str, now: float, force_switch: bool = False):
        """Regra de exclusividade: cada utilizador só pode estar numa única roda de cada vez,
        respeitando o limite máximo de 6 lugares (cadeiras) por roda."""
        for r in ROOMS_CATALOG:
            rid = r["id"]
            if rid == target_room_id:
                continue
            rm_other = data["rooms"][rid]
            if uid in (rm_other.get("listeners") or {}):
                rm_other["listeners"].pop(uid, None)
            if uid in (rm_other.get("live_reactions_by_user") or {}):
                rm_other["live_reactions_by_user"].pop(uid, None)
                _recalculate_live_reactions(rm_other)
            if force_switch or r.get("is_demo"):
                rm_other["queue"] = [q for q in rm_other.get("queue", []) if q.get("user_id") != uid]
                act = rm_other.get("active_speaker")
                if act and act.get("user_id") == uid:
                    _record_release_ritual_and_wipe(rm_other, now, reason="completed")
                    rm_other["active_speaker"] = None
                    _advance_turn_if_needed(rm_other, now)

        rm_target = data["rooms"][target_room_id]
        listeners = rm_target.setdefault("listeners", {})

        # Se a sala demo tiver 6 bots por algum motivo, garantir sempre 1 cadeira para o utilizador real
        if target_room_id == "demo_roda" and uid not in listeners and len(listeners) >= MAX_SEATS_PER_ROOM:
            # Libertar a cadeira 5 para o utilizador real
            for b_uid in list(listeners.keys()):
                if str(b_uid).startswith("demo_bot_") and listeners[b_uid].get("seat_idx") == 5:
                    listeners.pop(b_uid, None)
                    break

        if uid not in listeners and len(listeners) >= MAX_SEATS_PER_ROOM:
            return False  # Roda cheia (6/6 lugares ocupados)

        existing_info = listeners.get(uid) or {}
        seat_idx = _assign_seat_index(rm_target, uid)
        listeners[uid] = {
            "alias": _anon_alias_for(uid),
            "last_seen": now,
            "mood": existing_info.get("mood") or "escuta",
            "seat_idx": seat_idx,
            "is_demo_bot": False,
        }
        return True

    def _promote_next_speaker(room_state: dict, prev_speaker: dict, now: float, reason: str = "handoff"):
        """Promove o próximo membro na fila para receber o Bastão da Palavra (verde) e regista a animação do passe."""
        if not room_state.get("queue"):
            room_state["active_speaker"] = None
            return
        nxt = room_state["queue"].pop(0)
        room_state["active_speaker"] = {
            "user_id": nxt["user_id"],
            "alias": nxt["alias"],
            "avatar": "",
            "is_anonymous": True,
            "started_at": now,
            "ends_at": now + TURN_DURATION_SECONDS,
            "extended": False,
        }
        room_state["last_handoff"] = {
            "id": f"handoff_{_uuid.uuid4().hex[:8]}",
            "from_uid": prev_speaker.get("user_id") if prev_speaker else None,
            "from_alias": prev_speaker.get("alias") if prev_speaker else "Centro da Roda",
            "to_uid": nxt["user_id"],
            "to_alias": nxt["alias"],
            "reason": reason,
            "at": now,
        }
        room_state["messages"].append({
            "id": f"vc_sys_{_uuid.uuid4().hex[:8]}",
            "speaker_id": "system",
            "speaker_alias": "Círculo Sigaleve",
            "speaker_avatar": "",
            "is_anonymous": True,
            "kind": "system",
            "text": f"🌿 {nxt['alias']} recebeu o Bastão da Palavra. A roda escuta em silêncio — todas as mensagens serão libertadas e apagadas no fim do turno.",
            "reactions": {"contigo": 0, "forca": 0, "abraco": 0, "gratidao": 0},
            "reacted_by": {},
            "created_at": now,
        })

        # Se for na sala de demo e o novo orador for um bot, adicionar automaticamente uma partilha realista
        if room_state.get("id") == "demo_roda" and str(nxt["user_id"]).startswith("demo_bot_"):
            bot_prof = next((b for b in DEMO_BOT_PROFILES if b["user_id"] == nxt["user_id"]), None)
            if bot_prof and bot_prof.get("sample_messages"):
                room_state["messages"].append({
                    "id": f"vc_demo_{_uuid.uuid4().hex[:8]}",
                    "speaker_id": bot_prof["user_id"],
                    "speaker_alias": bot_prof["alias"],
                    "speaker_avatar": "",
                    "is_anonymous": True,
                    "kind": "share",
                    "text": bot_prof["sample_messages"][0],
                    "reactions": {"contigo": 2, "forca": 1, "abraco": 2, "gratidao": 1},
                    "reacted_by": {},
                    "created_at": now + 0.1,
                })
            # Manter a fila viva na sala demo
            if len(room_state["queue"]) < 2 and prev_speaker and str(prev_speaker.get("user_id", "")).startswith("demo_bot_"):
                room_state["queue"].append({
                    "user_id": prev_speaker["user_id"],
                    "alias": prev_speaker["alias"],
                    "avatar": "",
                    "is_anonymous": True,
                    "requested_at": now,
                })
            # Restaurar reações empáticas nos cantos dos bots ouvintes
            rx_cycle = ["contigo", "forca", "abraco", "gratidao"]
            room_state["live_reactions_by_user"] = {}
            for idx_b, b in enumerate(DEMO_BOT_PROFILES):
                if b["user_id"] != nxt["user_id"]:
                    room_state["live_reactions_by_user"][b["user_id"]] = rx_cycle[idx_b % len(rx_cycle)]
            _recalculate_live_reactions(room_state)

    def _advance_turn_if_needed(room_state: dict, now: float) -> bool:
        """Verifica se o turno atual expirou: apaga TODAS as mensagens da sessão e promove o próximo."""
        changed = False
        listeners = room_state.get("listeners") or {}
        stale_uids = [
            uid for uid, info in listeners.items()
            if not info.get("is_demo_bot") and (now - float(info.get("last_seen", 0)) > 120)
        ]
        for uid in stale_uids:
            listeners.pop(uid, None)
            if uid in (room_state.get("live_reactions_by_user") or {}):
                room_state["live_reactions_by_user"].pop(uid, None)
            changed = True
        if stale_uids:
            _recalculate_live_reactions(room_state)

        active = room_state.get("active_speaker")
        if active and now >= float(active.get("ends_at", 0)):
            prev_active = dict(active)
            _record_release_ritual_and_wipe(room_state, now, reason="timeout")
            room_state["active_speaker"] = None
            _promote_next_speaker(room_state, prev_active, now, reason="timeout")
            changed = True

        # Se não há orador ativo e não há ninguém na sala, garantir que mensagens estão vazias
        if room_state.get("active_speaker") is None and not listeners and room_state.get("messages"):
            _record_release_ritual_and_wipe(room_state, now, reason="empty")
            changed = True

        # Se não há orador ativo e há fila, promover o primeiro da fila
        if room_state.get("active_speaker") is None and room_state.get("queue"):
            _record_release_ritual_and_wipe(room_state, now, reason="handoff")
            _promote_next_speaker(room_state, None, now, reason="handoff")
            changed = True

        # Na sala demo, se o turno de um bot expirou e ficou sem ninguém, repor estado vivo da demo
        if room_state.get("id") == "demo_roda" and room_state.get("active_speaker") is None and not room_state.get("queue"):
            _populate_demo_room(room_state, now)
            changed = True

        return changed

    def _build_seats_payload(room_state: dict, current_uid: str, now: float) -> list:
        """Constrói as 6 cadeiras da mesa circular (0..5) com estado:
        - 'speaker' (verde esmeralda — com o Bastão da Palavra)
        - 'listener' (branco — em escuta ativa, com mood e reação no canto)
        - 'empty' (lugar livre na roda)"""
        listeners = room_state.get("listeners") or {}
        active = room_state.get("active_speaker")
        active_uid = active.get("user_id") if active else None
        queue_list = room_state.get("queue") or []
        queue_pos_by_uid = {q.get("user_id"): idx + 1 for idx, q in enumerate(queue_list)}
        live_by_user = room_state.get("live_reactions_by_user") or {}

        # Mapear utilizadores presentes para as 6 cadeiras
        seat_map = {}
        unassigned = []
        for uid_key, info in listeners.items():
            s_idx = info.get("seat_idx")
            if isinstance(s_idx, int) and 0 <= s_idx < MAX_SEATS_PER_ROOM and s_idx not in seat_map:
                seat_map[s_idx] = (uid_key, info)
            else:
                unassigned.append((uid_key, info))

        # Garantir que o orador ativo também tem cadeira atribuída
        if active_uid and active_uid not in listeners:
            unassigned.insert(0, (active_uid, {
                "alias": active.get("alias", _anon_alias_for(active_uid)),
                "mood": "esperancoso",
                "last_seen": now,
                "is_demo_bot": str(active_uid).startswith("demo_bot_"),
            }))

        for uid_key, info in unassigned:
            for s_idx in range(MAX_SEATS_PER_ROOM):
                if s_idx not in seat_map:
                    info["seat_idx"] = s_idx
                    seat_map[s_idx] = (uid_key, info)
                    break

        seats = []
        for s_idx in range(MAX_SEATS_PER_ROOM):
            if s_idx not in seat_map:
                seats.append({
                    "seat_index": s_idx,
                    "occupied": False,
                    "role": "empty",
                    "color_state": "empty",
                    "alias": "Lugar Livre",
                    "short_tag": f"Lugar #{s_idx + 1}",
                    "is_me": False,
                    "is_speaker": False,
                    "queue_position": None,
                    "mood_key": None,
                    "mood_emoji": None,
                    "mood_label": None,
                    "corner_reaction": None,
                    "corner_reaction_emoji": None,
                })
            else:
                u_id, info = seat_map[s_idx]
                alias = info.get("alias") or _anon_alias_for(u_id)
                short_tag = alias.split("#")[-1] if "#" in alias else f"0{s_idx + 1}"
                is_speaker = bool(active_uid and u_id == active_uid)
                is_me = bool(current_uid and u_id == current_uid)
                q_pos = queue_pos_by_uid.get(u_id)
                mood_key = info.get("mood") or "escuta"
                mood_meta = MOOD_TYPES.get(mood_key, MOOD_TYPES["escuta"])
                rx_key = live_by_user.get(u_id)
                rx_emoji = REACTION_TYPES[rx_key]["emoji"] if rx_key in REACTION_TYPES else None

                seats.append({
                    "seat_index": s_idx,
                    "occupied": True,
                    "role": "speaker" if is_speaker else ("queue" if q_pos else "listener"),
                    "color_state": "green" if is_speaker else "white",
                    "alias": alias,
                    "short_tag": f"#{short_tag}",
                    "is_me": is_me,
                    "is_speaker": is_speaker,
                    "is_demo_bot": bool(info.get("is_demo_bot", False)),
                    "queue_position": q_pos,
                    "mood_key": mood_key,
                    "mood_emoji": mood_meta["emoji"],
                    "mood_label": mood_meta["label"],
                    "corner_reaction": rx_key,
                    "corner_reaction_emoji": rx_emoji,
                })
        return seats

    def _serialize_room(room_meta: dict, room_state: dict, current_uid: str, now: float):
        _recalculate_live_reactions(room_state)
        active = room_state.get("active_speaker")
        active_payload = None
        if active:
            remaining = max(0, int(round(float(active.get("ends_at", now)) - now)))
            elapsed = max(0.0, now - float(active.get("started_at", now)))
            active_payload = {
                "alias": active.get("alias", "Membro Anónimo"),
                "avatar": "",
                "is_anonymous": True,
                "started_at": active.get("started_at", now),
                "ends_at": active.get("ends_at", now),
                "remaining_seconds": remaining,
                "elapsed_seconds": round(elapsed, 1),
                "in_grounding_pause": elapsed < 3.5,  # Pausa de respiração guiada de 3s ao receber o Bastão Verde
                "extended": bool(active.get("extended", False)),
                "is_me": bool(current_uid and active.get("user_id") == current_uid),
                "is_demo_bot": str(active.get("user_id", "")).startswith("demo_bot_"),
            }

        queue_payload = []
        my_queue_position = None
        for idx, q in enumerate(room_state.get("queue", [])):
            is_me = bool(current_uid and q.get("user_id") == current_uid)
            if is_me:
                my_queue_position = idx + 1
            queue_payload.append({
                "position": idx + 1,
                "alias": q.get("alias", "Membro Anónimo"),
                "avatar": "",
                "is_anonymous": True,
                "is_me": is_me,
            })

        seats_payload = _build_seats_payload(room_state, current_uid, now)
        occupied_count = sum(1 for s in seats_payload if s["occupied"])

        messages_payload = []
        latest_share_message = None
        for m in room_state.get("messages", [])[-MAX_MESSAGES_PER_ROOM:]:
            msg_reacted_by = m.get("reacted_by") or {}
            serialized_m = {
                "id": m.get("id"),
                "speaker_alias": m.get("speaker_alias", "Membro Anónimo"),
                "speaker_avatar": "",
                "is_anonymous": True,
                "kind": m.get("kind", "share"),
                "text": m.get("text", ""),
                "reactions": m.get("reactions") or {"contigo": 0, "forca": 0, "abraco": 0, "gratidao": 0},
                "my_reaction": msg_reacted_by.get(str(current_uid)) if current_uid else None,
                "created_at": m.get("created_at", now),
                "is_me": bool(current_uid and m.get("speaker_id") == current_uid),
            }
            messages_payload.append(serialized_m)
            if m.get("kind") == "share":
                latest_share_message = serialized_m

        live_by_user = room_state.get("live_reactions_by_user") or {}
        my_live_reaction = live_by_user.get(str(current_uid)) if current_uid else None

        listeners = room_state.get("listeners") or {}
        my_listener_info = listeners.get(str(current_uid)) or {}
        my_mood = my_listener_info.get("mood") or "escuta"

        # Verificar se 3 ou mais membros na roda estão a enviar uma reação silenciosa ("Abraço Coletivo da Roda")
        active_reactors_count = sum(1 for s in seats_payload if s["occupied"] and s.get("corner_reaction"))
        collective_hug_active = active_reactors_count >= 3

        # Ritual de libertação recente (visível durante 4.5 segundos após o fim de um turno)
        last_ritual = room_state.get("last_release_ritual")
        recent_ritual = None
        if last_ritual and (now - float(last_ritual.get("at", 0))) <= 5.0:
            recent_ritual = last_ritual

        # Passagem recente do Bastão da Palavra (visível durante 4 segundos para animar na roda)
        last_handoff = room_state.get("last_handoff")
        recent_handoff = None
        if last_handoff and (now - float(last_handoff.get("at", 0))) <= 4.5:
            recent_handoff = last_handoff

        return {
            "id": room_meta["id"],
            "title": room_meta["title"],
            "subtitle": room_meta["subtitle"],
            "emoji": room_meta["emoji"],
            "badge": room_meta["badge"],
            "theme_color": room_meta["theme_color"],
            "prompt_of_day": room_meta["prompt_of_day"],
            "is_demo": bool(room_meta.get("is_demo", False)),
            "max_seats": MAX_SEATS_PER_ROOM,
            "participants_count": occupied_count,
            "is_full": occupied_count >= MAX_SEATS_PER_ROOM and (str(current_uid) not in listeners),
            "seats": seats_payload,
            "my_mood": my_mood,
            "active_speaker": active_payload,
            "latest_share_message": latest_share_message,
            "queue": queue_payload,
            "my_queue_position": my_queue_position,
            "live_reactions": room_state.get("live_reactions") or {"contigo": 0, "forca": 0, "abraco": 0, "gratidao": 0},
            "my_live_reaction": my_live_reaction,
            "active_reactors_count": active_reactors_count,
            "collective_hug_active": collective_hug_active,
            "recent_release_ritual": recent_ritual,
            "recent_handoff": recent_handoff,
            "messages": messages_payload,
            "last_wiped_at": room_state.get("last_wiped_at"),
            "server_now": now,
        }

    def _broadcast_room_update(room_id: str, wiped: bool = False):
        """Notifica via Socket.IO todos os clientes na sala para atualizarem em tempo real."""
        try:
            payload = {"room_id": room_id, "wiped": wiped}
            socketio.emit("voices_circle_update", payload, room=f"voices_{room_id}")
            socketio.emit("voices_circle_update", payload)
        except Exception:
            pass

    @app.route("/api/v1/voices-circle", methods=["GET"])
    def api_voices_circle_state():
        uid = str(session.get("user_id") or session.get("user_email") or "guest_local")
        selected_room = (_request.args.get("room_id") or "aceitacao").strip().lower()
        force_switch = (_request.args.get("switch") or "") == "1"
        if selected_room not in {r["id"] for r in ROOMS_CATALOG}:
            selected_room = "aceitacao"

        now = _time.time()
        switched_from = None
        locked_in_other = None
        room_full_error = None

        with lock:
            data = _load()
            for r in ROOMS_CATALOG:
                rid = r["id"]
                _advance_turn_if_needed(data["rooms"][rid], now)

            committed_rid, committed_title, committed_role = _find_committed_room(data, uid)
            if committed_rid and committed_rid != selected_room:
                if force_switch:
                    switched_from = committed_title
                    joined = _enforce_single_room_presence(data, uid, selected_room, now, force_switch=True)
                    if not joined:
                        room_full_error = "Esta roda já atingiu o limite máximo de 6 pessoas."
                        selected_room = committed_rid
                        _enforce_single_room_presence(data, uid, selected_room, now, force_switch=False)
                else:
                    locked_in_other = {
                        "room_id": committed_rid,
                        "room_title": committed_title,
                        "role": committed_role,
                    }
                    selected_room = committed_rid
                    _enforce_single_room_presence(data, uid, selected_room, now, force_switch=False)
            else:
                joined = _enforce_single_room_presence(data, uid, selected_room, now, force_switch=False)
                if not joined:
                    room_full_error = "Esta roda já está completa (6/6 lugares ocupados)."

            rooms_summary = []
            current_room_detail = None
            for r in ROOMS_CATALOG:
                rid = r["id"]
                serialized = _serialize_room(r, data["rooms"][rid], uid, now)
                rooms_summary.append({
                    "id": serialized["id"],
                    "title": serialized["title"],
                    "subtitle": serialized["subtitle"],
                    "emoji": serialized["emoji"],
                    "badge": serialized["badge"],
                    "theme_color": serialized["theme_color"],
                    "prompt_of_day": serialized["prompt_of_day"],
                    "is_demo": serialized["is_demo"],
                    "max_seats": MAX_SEATS_PER_ROOM,
                    "participants_count": serialized["participants_count"],
                    "is_full": serialized["is_full"],
                    "has_active_speaker": serialized["active_speaker"] is not None,
                    "active_speaker_alias": serialized["active_speaker"]["alias"] if serialized["active_speaker"] else None,
                    "queue_count": len(serialized["queue"]),
                    "is_my_active_room": (rid == selected_room),
                })
                if rid == selected_room:
                    current_room_detail = serialized

        return _jsonify({
            "success": True,
            "my_anon_alias": _anon_alias_for(uid),
            "active_room_id": selected_room,
            "switched_from": switched_from,
            "locked_in_other": locked_in_other,
            "room_full_error": room_full_error,
            "rooms": rooms_summary,
            "current_room": current_room_detail,
            "reaction_types": REACTION_TYPES,
            "mood_types": MOOD_TYPES,
        })

    @app.route("/api/v1/voices-circle/mood", methods=["POST"])
    def api_voices_circle_mood():
        """Define o Check-in Emocional de 1 palavra do participante na roda (visível sob o seu avatar)."""
        uid = str(session.get("user_id") or session.get("user_email") or "guest_local")
        body = _request.get_json(silent=True) or {}
        room_id = (body.get("room_id") or "aceitacao").strip().lower()
        mood = (body.get("mood") or "escuta").strip().lower()

        if mood not in MOOD_TYPES:
            return _jsonify({"success": False, "error": "Estado emocional inválido."}), 400

        room_meta = next((r for r in ROOMS_CATALOG if r["id"] == room_id), None)
        if not room_meta:
            return _jsonify({"success": False, "error": "Sala inválida."}), 400

        now = _time.time()
        with lock:
            data = _load()
            _enforce_single_room_presence(data, uid, room_id, now, force_switch=False)
            rm = data["rooms"][room_id]
            if uid in rm.get("listeners", {}):
                rm["listeners"][uid]["mood"] = mood
                rm["listeners"][uid]["last_seen"] = now
            serialized = _serialize_room(room_meta, rm, uid, now)

        _broadcast_room_update(room_id)
        return _jsonify({
            "success": True,
            "mood": mood,
            "mood_meta": MOOD_TYPES[mood],
            "current_room": serialized,
        })

    @app.route("/api/v1/voices-circle/hand", methods=["POST"])
    def api_voices_circle_hand():
        """Gerir o Bastão da Palavra:
        - 'raise': pedir a palavra (ou assumir imediatamente na sala Demo)
        - 'lower': sair da fila
        - 'extend': +1 minuto extra (máx. 1 vez por turno)
        - 'pass': passar a vez sem pressão para o próximo na roda
        - 'finish': concluir partilha com Ritual de Libertação e apagar todo o chat"""
        uid = str(session.get("user_id") or session.get("user_email") or "guest_local")

        body = _request.get_json(silent=True) or {}
        room_id = (body.get("room_id") or "aceitacao").strip().lower()
        action = (body.get("action") or "raise").strip().lower()

        room_meta = next((r for r in ROOMS_CATALOG if r["id"] == room_id), None)
        if not room_meta:
            return _jsonify({"success": False, "error": "Sala inválida."}), 400

        now = _time.time()
        wiped = False
        with lock:
            data = _load()
            for r in ROOMS_CATALOG:
                _advance_turn_if_needed(data["rooms"][r["id"]], now)

            if action == "raise" and not room_meta.get("is_demo"):
                committed_rid, committed_title, committed_role = _find_committed_room(data, uid)
                if committed_rid and committed_rid != room_id:
                    role_txt = "com o Bastão da Palavra" if committed_role == "speaker" else "na fila da palavra"
                    return _jsonify({
                        "success": False,
                        "error": f"Só podes estar numa roda de cada vez! Já estás {role_txt} na roda «{committed_title}». Conclui ou sai dessa roda primeiro.",
                        "committed_room_id": committed_rid,
                    }), 409

            joined = _enforce_single_room_presence(data, uid, room_id, now, force_switch=False)
            if not joined:
                return _jsonify({
                    "success": False,
                    "error": "Esta roda já atingiu o limite máximo de 6 pessoas. Aguarda que um lugar fique livre.",
                }), 409

            rm = data["rooms"][room_id]
            alias, _ = _resolve_member_identity(uid, True)
            active = rm.get("active_speaker")

            if action == "raise":
                if active and active.get("user_id") == uid:
                    return _jsonify({
                        "success": True,
                        "message": "Já estás com o Bastão da Palavra!",
                        "current_room": _serialize_room(room_meta, rm, uid, now),
                    })

                # Na sala Demo (`demo_roda`), se quem tem a palavra é um bot, passar imediatamente o Bastão Verde ao utilizador
                # para que possa experimentar falar e ver o seu ícone em verde sem esperar 3 minutos!
                if room_meta.get("is_demo") and active and str(active.get("user_id", "")).startswith("demo_bot_"):
                    prev_bot = dict(active)
                    _record_release_ritual_and_wipe(rm, now, reason="handoff")
                    rm["queue"] = [q for q in rm["queue"] if q.get("user_id") != uid]
                    rm["queue"].insert(0, {
                        "user_id": uid,
                        "alias": alias,
                        "avatar": "",
                        "is_anonymous": True,
                        "requested_at": now,
                    })
                    # Recolocar o bot na fila para manter a roda viva
                    rm["queue"].append({
                        "user_id": prev_bot["user_id"],
                        "alias": prev_bot["alias"],
                        "avatar": "",
                        "is_anonymous": True,
                        "requested_at": now,
                    })
                    rm["active_speaker"] = None
                    _promote_next_speaker(rm, prev_bot, now, reason="handoff")
                    wiped = True
                else:
                    existing = next((q for q in rm["queue"] if q.get("user_id") == uid), None)
                    if existing:
                        existing["alias"] = alias
                        existing["avatar"] = ""
                        existing["is_anonymous"] = True
                    else:
                        rm["queue"].append({
                            "user_id": uid,
                            "alias": alias,
                            "avatar": "",
                            "is_anonymous": True,
                            "requested_at": now,
                        })
                    _advance_turn_if_needed(rm, now)
                serialized = _serialize_room(room_meta, rm, uid, now)

            elif action == "lower":
                rm["queue"] = [q for q in rm["queue"] if q.get("user_id") != uid]
                serialized = _serialize_room(room_meta, rm, uid, now)

            elif action == "extend":
                if not active or active.get("user_id") != uid:
                    return _jsonify({"success": False, "error": "Apenas o orador atual pode prolongar o turno."}), 403
                if active.get("extended"):
                    return _jsonify({"success": False, "error": "Já utilizaste a extensão de +1 minuto neste turno."}), 400
                active["ends_at"] = float(active.get("ends_at", now)) + EXTEND_BONUS_SECONDS
                active["extended"] = True
                serialized = _serialize_room(room_meta, rm, uid, now)

            elif action in ("finish", "pass"):
                # Permite terminar ou passar a vez (se for o orador atual, ou na sala demo para testar a rotação)
                if active and active.get("user_id") != uid and not room_meta.get("is_demo"):
                    return _jsonify({"success": False, "error": "Apenas quem tem o Bastão da Palavra pode concluir ou passar a vez."}), 403
                prev_active = dict(active) if active else None
                ritual_reason = "passed" if action == "pass" else "completed"
                _record_release_ritual_and_wipe(rm, now, reason=ritual_reason)
                rm["active_speaker"] = None
                wiped = True
                _promote_next_speaker(rm, prev_active, now, reason=ritual_reason)
                _advance_turn_if_needed(rm, now)
                serialized = _serialize_room(room_meta, rm, uid, now)
            else:
                return _jsonify({"success": False, "error": "Ação desconhecida."}), 400

        _broadcast_room_update(room_id, wiped=wiped)
        return _jsonify({"success": True, "wiped": wiped, "action": action, "current_room": serialized})

    @app.route("/api/v1/voices-circle/demo-action", methods=["POST"])
    def api_voices_circle_demo_action():
        """Controlos interativos exclusivos da Sala Demo (`demo_roda`) para demonstrar:
        - 'take_stick': O utilizador recebe imediatamente o Bastão Verde (com pausa de respiração de 3s).
        - 'next_turn': Passa o Bastão ao próximo membro da roda com animação e Ritual de Libertação.
        - 'collective_hug': Os 5 participantes da roda ativam reações nos seus cantos em simultâneo (Abraço Coletivo).
        - 'bot_share': O orador de demonstração envia uma nova mensagem ao vivo para a bolha central e chat.
        - 'reset_demo': Repõe o estado inicial completo da Roda Demo (6/6 lugares)."""
        uid = str(session.get("user_id") or session.get("user_email") or "guest_local")
        body = _request.get_json(silent=True) or {}
        demo_cmd = (body.get("command") or "next_turn").strip().lower()
        room_id = "demo_roda"
        room_meta = next((r for r in ROOMS_CATALOG if r["id"] == room_id), ROOMS_CATALOG[-1])

        now = _time.time()
        wiped = False
        with lock:
            data = _load()
            rm = data["rooms"][room_id]
            _enforce_single_room_presence(data, uid, room_id, now, force_switch=False)
            alias = _anon_alias_for(uid)

            if demo_cmd == "reset_demo":
                _populate_demo_room(rm, now)
                _enforce_single_room_presence(data, uid, room_id, now, force_switch=False)
                wiped = True

            elif demo_cmd == "take_stick":
                prev_active = dict(rm["active_speaker"]) if rm.get("active_speaker") else None
                _record_release_ritual_and_wipe(rm, now, reason="handoff")
                rm["queue"] = [q for q in rm.get("queue", []) if q.get("user_id") != uid]
                if prev_active and str(prev_active.get("user_id", "")).startswith("demo_bot_"):
                    rm["queue"].append({
                        "user_id": prev_active["user_id"],
                        "alias": prev_active["alias"],
                        "avatar": "",
                        "is_anonymous": True,
                        "requested_at": now,
                    })
                rm["queue"].insert(0, {
                    "user_id": uid,
                    "alias": alias,
                    "avatar": "",
                    "is_anonymous": True,
                    "requested_at": now,
                })
                rm["active_speaker"] = None
                _promote_next_speaker(rm, prev_active, now, reason="handoff")
                # Os 5 bots enviam apoio silencioso ao utilizador
                rx_keys = ["abraco", "contigo", "forca", "gratidao", "abraco"]
                rm["live_reactions_by_user"] = {
                    b["user_id"]: rx_keys[i % len(rx_keys)]
                    for i, b in enumerate(DEMO_BOT_PROFILES)
                }
                _recalculate_live_reactions(rm)
                wiped = True

            elif demo_cmd == "next_turn":
                prev_active = dict(rm["active_speaker"]) if rm.get("active_speaker") else None
                _record_release_ritual_and_wipe(rm, now, reason="completed")
                rm["active_speaker"] = None
                if not rm.get("queue"):
                    for b in DEMO_BOT_PROFILES[:3]:
                        rm["queue"].append({
                            "user_id": b["user_id"],
                            "alias": b["alias"],
                            "avatar": "",
                            "is_anonymous": True,
                            "requested_at": now,
                        })
                _promote_next_speaker(rm, prev_active, now, reason="handoff")
                wiped = True

            elif demo_cmd == "collective_hug":
                rx_keys = ["abraco", "contigo", "abraco", "gratidao", "forca"]
                active_uid = rm["active_speaker"]["user_id"] if rm.get("active_speaker") else None
                for i, b in enumerate(DEMO_BOT_PROFILES):
                    if b["user_id"] != active_uid:
                        rm.setdefault("live_reactions_by_user", {})[b["user_id"]] = rx_keys[i % len(rx_keys)]
                _recalculate_live_reactions(rm)

            elif demo_cmd == "bot_share":
                active = rm.get("active_speaker")
                if not active or not str(active.get("user_id", "")).startswith("demo_bot_"):
                    # Se o utilizador tinha a palavra, um bot assume ou envia exemplo
                    bot_prof = DEMO_BOT_PROFILES[0]
                    sp_uid = active["user_id"] if active else bot_prof["user_id"]
                    sp_alias = active["alias"] if active else bot_prof["alias"]
                else:
                    sp_uid = active["user_id"]
                    sp_alias = active["alias"]
                    bot_prof = next((b for b in DEMO_BOT_PROFILES if b["user_id"] == sp_uid), DEMO_BOT_PROFILES[0])

                existing_shares = [m for m in rm.get("messages", []) if m.get("kind") == "share"]
                samples = bot_prof.get("sample_messages") or DEMO_BOT_PROFILES[0]["sample_messages"]
                next_text = samples[len(existing_shares) % len(samples)]
                rm["messages"].append({
                    "id": f"vc_demo_{_uuid.uuid4().hex[:8]}",
                    "speaker_id": sp_uid,
                    "speaker_alias": sp_alias,
                    "speaker_avatar": "",
                    "is_anonymous": True,
                    "kind": "share",
                    "text": next_text,
                    "reactions": {"contigo": 2, "forca": 2, "abraco": 3, "gratidao": 1},
                    "reacted_by": {},
                    "created_at": now,
                })

            serialized = _serialize_room(room_meta, rm, uid, now)

        _broadcast_room_update(room_id, wiped=wiped)
        return _jsonify({"success": True, "command": demo_cmd, "wiped": wiped, "current_room": serialized})

    @app.route("/api/v1/voices-circle/speak", methods=["POST"])
    def api_voices_circle_speak():
        """Envia uma mensagem para a bolha central e para o chat ao vivo da roda.
        Regra estrita: apenas quem tem o Bastão da Palavra (ícone verde) pode escrever e enviar mensagens."""
        uid = str(session.get("user_id") or session.get("user_email") or "guest_local")

        body = _request.get_json(silent=True) or {}
        room_id = (body.get("room_id") or "aceitacao").strip().lower()
        text = (body.get("text") or "").strip()

        room_meta = next((r for r in ROOMS_CATALOG if r["id"] == room_id), None)
        if not room_meta:
            return _jsonify({"success": False, "error": "Sala inválida."}), 400

        if len(text) < 1 or len(text) > 1000:
            return _jsonify({"success": False, "error": "Escreve uma mensagem (máx. 1000 caracteres)."}), 400

        ok, why = validate_content_privacy_fn(text)
        if not ok:
            return _jsonify({"success": False, "error": why, "code": "PRIVACY_BLOCK"}), 400

        now = _time.time()
        with lock:
            data = _load()
            for r in ROOMS_CATALOG:
                _advance_turn_if_needed(data["rooms"][r["id"]], now)

            if not room_meta.get("is_demo"):
                committed_rid, committed_title, committed_role = _find_committed_room(data, uid)
                if committed_rid and committed_rid != room_id:
                    role_txt = "com o Bastão da Palavra" if committed_role == "speaker" else "na fila da palavra"
                    return _jsonify({
                        "success": False,
                        "error": f"Só podes estar numa roda de cada vez! Já estás {role_txt} na roda «{committed_title}».",
                        "committed_room_id": committed_rid,
                    }), 409

            joined = _enforce_single_room_presence(data, uid, room_id, now, force_switch=False)
            if not joined:
                return _jsonify({"success": False, "error": "Esta roda já atingiu o limite de 6 participantes."}), 409

            rm = data["rooms"][room_id]
            active = rm.get("active_speaker")
            alias, _ = _resolve_member_identity(uid, True)

            if active is None:
                return _jsonify({
                    "success": False,
                    "error": "Para poderes escrever e enviar mensagens no chat da roda, clica primeiro em «Pedir a Palavra (3 min)» para receberes o Bastão Verde!",
                }), 403
            elif active.get("user_id") != uid:
                return _jsonify({
                    "success": False,
                    "error": f"Só podes enviar mensagens quando o teu ícone estiver em VERDE (com o Bastão da Palavra)! Neste momento {active.get('alias')} tem a palavra.",
                }), 403

            msg = {
                "id": f"vc_msg_{_uuid.uuid4().hex[:10]}",
                "speaker_id": uid,
                "speaker_alias": alias,
                "speaker_avatar": "",
                "is_anonymous": True,
                "kind": "share",
                "text": text,
                "reactions": {"contigo": 0, "forca": 0, "abraco": 0, "gratidao": 0},
                "reacted_by": {},
                "created_at": now,
            }
            rm["messages"].append(msg)
            if len(rm["messages"]) > MAX_MESSAGES_PER_ROOM:
                rm["messages"] = rm["messages"][-MAX_MESSAGES_PER_ROOM:]

            serialized = _serialize_room(room_meta, rm, uid, now)

        _broadcast_room_update(room_id)
        return _jsonify({"success": True, "message": msg, "current_room": serialized})

    @app.route("/api/v1/voices-circle/react", methods=["POST"])
    def api_voices_circle_react():
        """Envia ou alterna uma única reação silenciosa de empatia:
        - Se clicar na mesma reação que já tinha selecionado, ela é desmarcada (-1).
        - Se clicar noutra reação diferente, a anterior é desmarcada (-1) e a nova aparece no canto do seu ícone (+1).
        """
        uid = str(session.get("user_id") or session.get("user_email") or "guest_local")
        body = _request.get_json(silent=True) or {}
        room_id = (body.get("room_id") or "aceitacao").strip().lower()
        reaction = (body.get("reaction") or "contigo").strip().lower()
        message_id = (body.get("message_id") or "").strip()

        if reaction not in REACTION_TYPES:
            return _jsonify({"success": False, "error": "Reação inválida."}), 400

        room_meta = next((r for r in ROOMS_CATALOG if r["id"] == room_id), None)
        if not room_meta:
            return _jsonify({"success": False, "error": "Sala inválida."}), 400

        now = _time.time()
        selected_now = None
        with lock:
            data = _load()
            if not room_meta.get("is_demo"):
                committed_rid, committed_title, _ = _find_committed_room(data, uid)
                if committed_rid and committed_rid != room_id:
                    return _jsonify({
                        "success": False,
                        "error": f"Só podes estar numa roda de cada vez (estás ativo em «{committed_title}»).",
                    }), 409

            _enforce_single_room_presence(data, uid, room_id, now, force_switch=False)
            rm = data["rooms"][room_id]
            _advance_turn_if_needed(rm, now)

            if message_id:
                target_msg = next((m for m in rm.get("messages", []) if m.get("id") == message_id), None)
                if target_msg is not None:
                    rx_map = target_msg.setdefault("reactions", {"contigo": 0, "forca": 0, "abraco": 0, "gratidao": 0})
                    reacted_by = target_msg.setdefault("reacted_by", {})
                    prev_rx = reacted_by.get(uid)
                    if prev_rx == reaction:
                        rx_map[reaction] = max(0, int(rx_map.get(reaction, 0)) - 1)
                        reacted_by.pop(uid, None)
                        selected_now = None
                    else:
                        if prev_rx and prev_rx in rx_map:
                            rx_map[prev_rx] = max(0, int(rx_map.get(prev_rx, 0)) - 1)
                        rx_map[reaction] = int(rx_map.get(reaction, 0)) + 1
                        reacted_by[uid] = reaction
                        selected_now = reaction
            else:
                live_by_user = rm.setdefault("live_reactions_by_user", {})
                prev_rx = live_by_user.get(uid)
                if prev_rx == reaction:
                    live_by_user.pop(uid, None)
                    selected_now = None
                else:
                    live_by_user[uid] = reaction
                    selected_now = reaction
                _recalculate_live_reactions(rm)

            serialized = _serialize_room(room_meta, rm, uid, now)

        try:
            if selected_now:
                socketio.emit(
                    "voices_circle_reaction",
                    {
                        "room_id": room_id,
                        "reaction": selected_now,
                        "emoji": REACTION_TYPES[selected_now]["emoji"],
                        "message_id": message_id or None,
                    },
                )
            else:
                _broadcast_room_update(room_id)
        except Exception:
            pass

        return _jsonify({
            "success": True,
            "reaction": selected_now,
            "emoji": REACTION_TYPES[selected_now]["emoji"] if selected_now else None,
            "current_room": serialized,
        })
