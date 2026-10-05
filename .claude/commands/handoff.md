---
description: Met à jour .ai/STATE.md (contexte vivant) puis régénère le snapshot auto
allowed-tools: Bash(bash .ai/ctx.sh), Read(.ai/STATE.md), Edit(.ai/STATE.md)
---

Prépare la passation de contexte pour la prochaine session (objectif : zéro re-exploration).

1. Lis `.ai/STATE.md`.
2. Mets à jour **uniquement la partie haute** (au-dessus du marqueur `CTX:AUTO:START`) à partir
   de ce qui s'est réellement passé dans CETTE conversation :
   - **🎯 Focus actuel** : la tâche en cours maintenant.
   - **✅ Fait récemment** : ce qui a été terminé/mergé (garde ~5 points max, élague l'ancien).
   - **🔧 En cours / à faire** : les prochaines étapes concrètes.
   - **🧠 Décisions clés** : ajoute toute décision prise ici qu'il ne faudra pas re-débattre.
   Reste **compact** (~40-50 lignes total). Ne touche pas au bloc entre les marqueurs `CTX:AUTO`.
3. Lance `bash .ai/ctx.sh` pour régénérer le snapshot git/issues.
4. Résume en 2-3 lignes ce qui a changé dans l'état.

Ne commite rien sauf si on te le demande explicitement.
