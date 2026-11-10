# P2 – Étape 4 : notes d'exploration de l'application de budget

Support pour la discussion avec le mentor. Tout ce qui est écrit ici a été observé en lisant le code et en le testant.

## 1. Organisation du projet

| Fichier | Rôle |
|---|---|
| `expenses.py` | Le vrai programme : classe `Expense`, lecture/écriture du CSV, affichage, menu et boucle principale |
| `main.py` | Simple script de vérification de l'installation (affiche un message et l'heure). Il ne lance **pas** l'application |
| `emma_expenses.csv` | Données de départ : 213 dépenses sur l'année 2025 |
| `personnal_expenses.csv` | Fichier vide, ne contient que la ligne d'en-tête |
| `.gitignore` | Exclut notamment `.venv/`, `__pycache__/` et `.idea/` |

**Point d'entrée réel** : `python expenses.py`, lancé depuis le dossier `p2-budget`.

**Données** : colonnes `date,category,description,amount`, dates au format `jj/mm/aaaa`, montants avec 2 décimales (ex. loyer mensuel de 780.00).

## 2. Le code de `expenses.py`

- **Constantes** : `FILENAME` est un simple **texte** (le nom du fichier, sans chemin). `COLUMNS` est la liste des 4 noms de colonnes ; elle ne sert qu'à écrire l'en-tête quand le fichier est créé.
- **`class Expense`** : représente une dépense. Le constructeur convertit le montant avec `float()` car un CSV ne contient que du texte. `to_row()` renvoie la dépense sous forme de liste de textes prête à être écrite (montant avec `:.2f`).
- **`read_expenses()`** : renvoie `[]` si le fichier n'existe pas. Sinon, lit le CSV avec `csv.DictReader` (chaque ligne devient un dictionnaire dont les clés viennent de l'en-tête) et construit une liste d'objets `Expense`.
- **`save_expense(expense)`** : ajoute une ligne à la fin du fichier (mode `"a"`). Elle écrit d'abord l'en-tête si le fichier est nouveau.
- **`show_history()`** : affiche le tableau de toutes les dépenses, calcule le total et le nombre de dépenses. Si la liste est vide, affiche un message et s'arrête avec `return`.
- **`add_expense()`** : demande catégorie, description et montant. Remplace la virgule par un point, convertit en nombre dans un `try/except`, ajoute la date du jour, puis appelle `save_expense`.
- **`show_menu()`** et **`main()`** : le menu à 3 choix dans une boucle `while True`, qui s'arrête avec `break` au choix 3.

## 3. Mécanismes importants

- **`if __name__ == "__main__":`** : `__name__` vaut `"__main__"` quand le fichier est lancé directement, et le nom du module (ici `"expenses"`) quand il est importé. Un `import` exécute le fichier une fois, de haut en bas : les fonctions et la classe sont **définies**, mais `main()` n'est pas **appelé**. Sans ce garde-fou, le menu se lancerait dès l'import.
- **Deux façons de lancer l'app** (en théorie) : `python expenses.py`, ou depuis `main.py` avec `import expenses` puis `expenses.main()`. Aujourd'hui, seule la première fonctionne, car `main.py` n'est pas relié.
- **`file_exists` calculé avant `open(..., "a")`** : le mode `"a"` crée le fichier s'il est absent. Calculé après, il vaudrait toujours `True` et l'en-tête ne serait jamais écrit.
- **Le CSV est cherché dans le dossier du terminal**, pas dans celui du script. Lancé ailleurs, le programme ne trouve pas `emma_expenses.csv` : l'historique est vide, et un ajout crée un **nouveau** fichier dans le dossier courant.

## 4. Comportements testés

Tests faits depuis un dossier **hors du dépôt**, avec `python C:\dev\p2-budget\expenses.py`, pour ne jamais modifier les données d'origine.

| Cas | Résultat observé |
|---|---|
| Historique sans fichier | « No expense saved yet, add one first. » ; aucun fichier créé |
| Ajout valide (12.5) | `Expense of 12.50 EUR saved.` ; fichier créé avec en-tête + `09/11/2026,leisure,leisure test,12.50` |
| Historique après ajout | ligne de la dépense et `Total: 12.50 EUR over 1 expense(s).` |
| Montant avec virgule | accepté (virgule remplacée par un point) |
| Montant avec lettres (`abc`) | « Invalid amount, the expense was not saved. » ; rien d'écrit ; retour au menu |
| Montant vide | même comportement que les lettres |
| Choix de menu invalide | « Invalid choice, please enter a number between 1 and 3. » |
| Choix avec espaces (` 1 `) | fonctionne grâce à `.strip()` |

## 5. Limites et comportements surprenants constatés

- **Catégorie ou description vides** : acceptées, la ligne CSV devient `date,,,12.00`. Une saisie faite d'espaces seuls donne le même résultat que du vide (`.strip()`), donc un seul groupe « sans catégorie » pour de futures statistiques.
- **Montant négatif (`-20`) ou nul (`0`)** : acceptés. Un montant négatif réduit le total : incohérent pour une dépense, sauf à l'assumer comme un remboursement.
- **`nan` et `inf`** : acceptés, car `float("nan")` ne lève pas d'erreur. Le total devient `nan EUR`, et la ligne reste dans le CSV, donc elle **contamine toutes les lectures suivantes**. Piste pour l'étape 5 : tester `math.isfinite(amount)` après la conversion et refuser la valeur si le résultat est `False`.
- **Pas de détection de doublons** : saisir deux fois la même dépense crée deux lignes.
- **Ordre des saisies** : catégorie et description sont demandées avant le montant. Si le montant est invalide, tout est perdu. Piste : valider le montant en premier.
- **Le `try/except` ne couvre que `float()`** : une autre erreur fait planter le programme. Exemple rencontré : `PermissionError` parce que le CSV était ouvert dans Excel.
- **Le nombre de mois n'existe pas dans les données** : il faudra le déduire du texte de la date, conservée telle quelle dans `Expense`. À garder en tête pour les moyennes mensuelles de l'étape 5.

## 6. Git : où j'en suis

- Starter cloné dans `C:\dev\p2-budget`, hors de mon dépôt de formation (pas de dépôt imbriqué).
- Dépôt privé `Papynacho/p2-budget` créé ; remote `origin` redirigé avec `git remote set-url`, puis `main` et `develop` poussées avec `git push -u`.
- Je travaille sur `develop`. Mentor invité comme collaborateur.
- Les tests ont été faits hors du dépôt : `emma_expenses.csv` d'origine n'a pas été modifié.
