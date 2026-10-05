# Directives agents — portfolio-backend

Règles de collaboration pour les agents (Claude / Gemini) sur **portfolio-backend** (API Python).

---

## 📍 0. Contexte vivant (lire en premier)

L'état **dynamique** du projet (focus, en cours, décisions) est maintenu dans
**[`.ai/STATE.md`](.ai/STATE.md)** pour éviter de le re-dériver — et donc de rebrûler des %
de session — à chaque conversation. Il est importé ici :

@.ai/STATE.md

Convention complète dans [`.ai/README.md`](.ai/README.md). En fin de session, rafraîchir
l'état : `bash .ai/ctx.sh` (ou la commande `/handoff` sous Claude Code).

---

## 🧱 Stack
- API : **Python** (FastAPI probable), code dans `app/` (ex. `app/main.py`).
- Dépendances : `requirements.txt`.
- Déploiement : `Dockerfile` + `docker-compose.prod.yml`.

<!-- Ajoute ici les règles statiques du projet (workflow git, conventions, contraintes). -->
