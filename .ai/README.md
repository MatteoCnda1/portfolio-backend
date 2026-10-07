# `.ai/` — Kit de contexte vivant

But : **économiser les % de session** Claude/Gemini en évitant de re-dériver l'état du
projet à chaque conversation. Les règles **statiques** vivent dans `AGENTS.md` ; ici on ne
garde que l'**état dynamique**, sous une forme compacte et auto-chargée.

## Contenu
- **`STATE.md`** — le contexte optimal (focus, fait / en cours, décisions, où regarder).
  Auto-chargé en début de session via un import dans `AGENTS.md` (`@.ai/STATE.md`).
  - Partie **haute** : maintenue à la main (ou via la commande `/handoff` sous Claude).
  - Partie **basse** (entre les marqueurs `CTX:AUTO`) : régénérée par `ctx.sh`, à ne pas éditer.
- **`SKILLS.md`** — quelles skills utiliser selon la tâche (communes + spécifiques au projet).
  Auto-chargé via `@.ai/SKILLS.md` dans `AGENTS.md`. Les skills embarquées vivent dans
  `.claude/skills/<nom>/` (ex. `grill-me`).
- **`ctx.sh`** — régénère le bloc dynamique (branche, 5 derniers commits, issues `gh` ouvertes,
  nb de fichiers modifiés). Déterministe, aucun appel LLM.

## Discipline (le cœur du gain)
1. **Début de session** : `STATE.md` est déjà dans le contexte → pas d'exploration à l'aveugle.
2. **Pendant** : si tu changes de focus ou prends une décision, mets à jour la partie haute.
3. **Fin de session** : rafraîchis l'état pour la prochaine fois :
   ```bash
   bash .ai/ctx.sh        # met à jour le snapshot git/issues
   ```
   Sous Claude Code tu peux aussi lancer `/handoff` (met à jour la partie haute + lance `ctx.sh`).

## Règle d'or
`STATE.md` doit rester **court** (~40-50 lignes). S'il gonfle, c'est que du statique s'y est
glissé → le déplacer dans `AGENTS.md`. Un contexte court rechargé = quelques centaines de tokens,
contre une exploration complète du repo à chaque fois.

## Portage vers un autre repo
```bash
cp -r .ai/ /chemin/autre-repo/
mkdir -p /chemin/autre-repo/.claude/skills && cp -r .claude/skills/grill-me /chemin/autre-repo/.claude/skills/
# puis ajouter en tête de son AGENTS.md (ou CLAUDE.md) : @.ai/STATE.md et @.ai/SKILLS.md
# et adapter la partie haute de .ai/STATE.md + la section « Spécifiques » de .ai/SKILLS.md.
```
