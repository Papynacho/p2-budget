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
| `requirements.txt` | Dépendances Python du projet (`numpy-financial`). À installer dans le `.venv` avec `pip install -r requirements.txt` |

**Point d'entrée réel** : `python expenses.py`, lancé depuis le dossier `p2-budget`.

**Données** : colonnes `date,category,description,amount`, dates au format `jj/mm/aaaa`, montants avec 2 décimales (ex. loyer mensuel de 780.00).

## 2. Le code de `expenses.py` (version fournie, avant mes modifications)

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

## 4. Comportements testés (sur la version fournie)

Le menu avait alors 3 choix ; il en compte 6 aujourd'hui (1 historique, 2 ajout, 3 statistiques, 4 simulation voiture, 5 simulation prêt immobilier, 6 quitter). Tests faits depuis un dossier **hors du dépôt**, avec `python C:\dev\p2-budget\expenses.py`, pour ne jamais modifier les données d'origine.

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
- Fonctionnalité 1 développée par petites fonctions, un commit par fonction, poussés sur `develop` :

| Commit | Contenu |
|---|---|
| `ca1d4de` | menu (« Statistics » en 3, « Quit » en 4), squelette de `show_stats`, `total_expenses` |
| `9c77ee4` | `months_covered` |
| `3ddde61` | `totals_by_category` |
| `8083a5a` | `monthly_averages` et renommage de `cat` en `total_category` |
| `7be88aa` | affichage complet dans `show_stats` |
| `ee364e8` | mise à jour de `NOTES.md` (fonctionnalité 1) |
| `308a3b3` | fonctionnalité 2 : menu « Car Purchase Simulator » (4) et « Quit » (5), `average_expenses_monthly`, `month_savings`, `months_to_buy`, `show_month_for_car`, et mise à jour de `NOTES.md` |
| `f307cc1` | fonctionnalité 3 (début) : constantes `ANNUAL_RATE`, `LOAN_YEARS`, `MAX_DEBT_RATIO`, menu « Mortgage Simulator » (5) et « Quit » (6), `monthly_max_capacity`, affichage provisoire ; `requirements.txt` encore vide |
| `e0cf80b` | ajout de `numpy-financial` à `requirements.txt` |
| `ec3c4b6` | `loan_capacity` et affichage du tableau des montants empruntables (fonctionnalité 3 terminée) |

Historique complet : `git log --oneline` (il contient aussi les commits du starter et d'éventuels commits intermédiaires non listés ici).

La fonctionnalité 2 a été validée par tous les tests de la section 8 avant d'être commitée en une seule fois, puis poussée sur `develop`. La fonctionnalité 3 a été commitée en trois étapes (calcul de la capacité, dépendance, calcul du capital et affichage), toutes testées (section 9) avant le push.

**Enseignements Git de la fonctionnalité 3**
- `git commit -am` prend **tous les fichiers suivis modifiés**, pas seulement celui dont parle le message. Un premier commit « Add requirements.txt » embarquait aussi du code inachevé de `expenses.py` ; il a été annulé avec `git reset --soft HEAD~1` (avant tout push), puis refait avec le seul `requirements.txt` (`e0cf80b`).
- `git commit --amend` n'est utilisable que **tant que rien n'est poussé** : il a corrigé une faute de frappe dans le message de `f307cc1` avant le push.
- Le message de `ec3c4b6` contient une faute de frappe (« fucntion »). Il a été poussé : je ne l'ai pas corrigé, car cela obligerait à réécrire un commit publié (`--amend` puis `push --force-with-lease`) alors que le mentor a accès au dépôt.
- `git --no-pager diff` avant chaque commit a permis de repérer que `FILENAME` avait été modifié pour un test (`emma_expense.csv`, sans le « s ») et pas remis en place. Corrigé avant le commit.

## 7. Étape 5 – Fonctionnalité 1 : statistiques par catégorie

**Organisation du code** : `show_stats()` ne fait que lire les dépenses et **afficher**. Les calculs sont dans quatre fonctions qui ne font aucun `print` et renvoient une valeur (`return`) :

| Fonction | Reçoit | Renvoie |
|---|---|---|
| `total_expenses(expenses)` | la liste des dépenses | le total général (nombre) |
| `months_covered(expenses)` | la liste des dépenses | le nombre de mois distincts (nombre) |
| `totals_by_category(expenses)` | la liste des dépenses | un dictionnaire catégorie → total |
| `monthly_averages(months_cov, total_category)` | le nombre de mois et les totaux | un dictionnaire catégorie → moyenne mensuelle |

`monthly_averages` reçoit les résultats des deux fonctions précédentes, pas la liste complète : elle ne refait donc aucun calcul.

**Choix de conception**
- **Mois couverts** : la date reste du texte (`"05/03/2025"`). Je la découpe avec `.split("/")` et j'ajoute `"mois/année"` (ex. `"03/2025"`) dans un `set`, qui ne garde chaque valeur qu'une fois. `len(set)` donne le nombre de mois. Garder l'année évite de confondre mars 2025 et mars 2026.
- **Totaux par catégorie** : un dictionnaire. À la première apparition d'une catégorie je pose la valeur avec `=`, ensuite j'ajoute avec `+=` (un `+=` sur une clé absente provoquerait une `KeyError`).
- **Historique vide** : le garde-fou `if not expenses` est placé **avant** les calculs, ce qui évite une division par zéro dans les moyennes.
- **Affichage** : alignement avec `:<20`, `:>10.2f`, `:>20.2f`, comme `show_history`. Singulier/pluriel : `1 month` / `13 months`.

**Vérifications faites** (CSV d'Emma, 213 dépenses, tests depuis un dossier hors dépôt)

| Catégorie | Total | Moyenne mensuelle |
|---|---|---|
| groceries | 2462.87 | 205.24 |
| transport | 1013.91 | 84.49 |
| subscription | 520.72 | 43.39 |
| leisure | 406.50 | 33.88 |
| housing | 9360.00 | 780.00 |
| restaurant | 961.92 | 80.16 |
| clothing | 1220.69 | 101.72 |
| utilities | 1456.13 | 121.34 |
| health | 603.61 | 50.30 |
| **Total** | **18006.35** | **12 mois** |

- La somme des totaux par catégorie est égale au total général.
- Sans fichier CSV : message « No expense saved yet, add one first. », pas de plantage.
- Une seule dépense : « over 1 month ». Avec le CSV d'Emma : « over 12 months ».

**Limites constatées**
- **Définition des « mois couverts »** : ma fonction compte les mois qui ont au moins une dépense. En ajoutant une dépense en novembre 2026 à l'année 2025, l'application indique 13 mois (et non 23) et les moyennes baissent. À valider avec le mentor : mois distincts, ou durée entre la première et la dernière dépense ?
- **Décimales parasites** : l'ordinateur représente mal certains décimaux (`1456.1299999999999`). C'est corrigé à l'affichage avec `:.2f`, pas dans les données.
- **Catégorie vide** : `""` apparaîtrait comme une catégorie à part dans le tableau (non géré).
- **Pas de tri** : les catégories apparaissent dans l'ordre d'arrivée dans le CSV (piste : `sorted(...)`).
- **Format de date supposé** : `jj/mm/aaaa`. Une date mal formée (`5/3/25`) provoquerait des résultats faux ou une erreur.

**Questions posées au mentor avant les fonctionnalités 2 et 3**
1. D'où vient le revenu mensuel pour calculer l'épargne disponible ? → **Réponse reçue** : il manque bien dans les données. Avec le mentor, j'ai fixé `INCOME = 2000` en constante (voir section 8).
2. Quelle est la formule du prêt immobilier (taux, durée) ? → **Traitée** : formule d'annuité constante avec un taux annuel de 5 % et des durées de 10, 15 et 20 ans, en constantes (voir section 9).
3. Comment compter les « mois couverts » (voir limites) ? → **Décision provisoire** : on garde les mois distincts qui contiennent au moins une dépense (12 mois pour le CSV d'Emma, ce qui coïncide avec la durée réelle). **À confirmer avec le mentor** : cela change les moyennes des fonctionnalités 1, 2 et 3.

## 8. Étape 5 – Fonctionnalité 2 : simulation d'achat d'une voiture

**Objectif** (cahier des charges) : à partir de l'historique et du prix saisi, calculer l'épargne mensuelle disponible et afficher le nombre de mois nécessaires pour atteindre ce prix.

**Revenu** : il n'est dans aucun fichier. `INCOME = 2000` est une **constante** en haut du fichier, définie avec le mentor. Elle est passée en argument à `month_savings` : la fonction travaille avec ce qu'elle reçoit (`income`), elle ne va pas chercher la constante elle-même.

**Menu** : « Car Purchase Simulator » en 4 (le mot « Loan » a été remplacé, car la fonctionnalité calcule une durée d'épargne et non un prêt), « Quit » en 5 ; le message d'erreur du menu indique « between 1 and 5 ».

**Organisation du code** : `show_month_for_car()` lit, valide la saisie et **affiche**. Les calculs sont dans trois nouvelles fonctions sans `print`, qui renvoient une valeur. Elles réutilisent `total_expenses` et `months_covered` de la fonctionnalité 1.

| Fonction | Reçoit | Renvoie |
|---|---|---|
| `average_expenses_monthly(global_expense, months_cov)` | le total des dépenses et le nombre de mois | la dépense moyenne par mois (nombre) |
| `month_savings(income, av)` | le revenu et la dépense moyenne | l'épargne mensuelle, ou `None` si elle est ≤ 0 |
| `months_to_buy(choice_car_price, savings)` | le prix et l'épargne | le nombre de mois entiers (`math.ceil`) |

Déroulé de `show_month_for_car()` :
1. Lit les dépenses ; si la liste est vide, message et `return` (avant même de demander le prix).
2. Demande le prix (la virgule est remplacée par un point, comme dans `add_expense`), le convertit avec `float()` et refuse un texte, un prix nul ou négatif, `nan` et `inf`.
3. Calcule la moyenne mensuelle, puis l'épargne.
4. Si l'épargne est `None` : message « No savings available » et `return`. Sinon calcule le nombre de mois et l'affiche.

**Formules** : épargne mensuelle = `INCOME` − (total des dépenses ÷ nombre de mois) ; nombre de mois = prix ÷ épargne, arrondi au mois supérieur.

**Choix de conception**
- **`None` quand l'épargne est ≤ 0** : évite la division par zéro (épargne nulle) et un nombre de mois négatif (épargne négative). Le test est dans `show_month_for_car`, pas dans le calcul, pour que les fonctions de calcul ne fassent aucun `print`.
- **`math.ceil`** : 18,02 mois donnent 19, car 18 mois ne suffisent pas à atteindre le prix.
- **Validation du prix** : `float()` dans un `try/except`, puis `amount <= 0 or not math.isfinite(amount)`. C'est la piste notée à la section 5 pour `nan` et `inf`.
- **Garde-fou « historique vide » avant la saisie** : on ne demande pas un prix pour dire ensuite qu'il n'y a pas de données, et on évite une division par zéro dans la moyenne.

**Vérifications faites** (CSV d'Emma, `INCOME = 2000`)

| Cas | Résultat observé |
|---|---|
| Prix 9000 | « You need : 19 months » |
| Calcul indépendant | 18 006,35 ÷ 12 = 1 500,53 de dépenses par mois ; épargne 499,47 ; 9 000 ÷ 499,47 = 18,02, donc 19 |
| `INCOME = 1000` (temporaire) | « No savings available », retour au menu, pas de plantage |
| Prix `0` et `-5` | « Invalid price, enter a positive number » |
| Prix `nan` | « Invalid price, enter a positive number » |
| Prix `abc` | « Invalid amount, input only numbers. » |
| Options 1 et 3 après modification | inchangées (18006.35 EUR, 12 mois, mêmes moyennes) |

**Piège rencontré** : une première valeur attendue (15 mois) avait été calculée à partir de statistiques faussées par une dépense de test de 150 € ajoutée en novembre 2026 (13 mois, 18 156,35 €). Sur le CSV d'origine, le bon résultat est 19. Conclusion : toujours recalculer la valeur de référence sur des données non modifiées.

**Limites constatées**
- **Revenu fixé dans le code** : il n'est ni saisi ni lu dans un fichier, et il est identique pour `emma_expenses.csv` et `personnal_expenses.csv`.
- **L'épargne dépend des « mois couverts »** : la moyenne est calculée sur les mois qui ont au moins une dépense, comme pour les statistiques (même question ouverte pour le mentor). Elle inclut le logement.
- **Calcul simplifié** : pas d'intérêts, d'inflation, d'apport ni de revente d'un véhicule ; la dépense moyenne passée est supposée identique dans le futur.
- **Singulier** : l'affichage dit « 1 months » si le résultat vaut 1.
- **Pas de plafond sur le prix** : un prix énorme donne un nombre de mois énorme, affiché tel quel.

**Questions encore ouvertes à la fin de la fonctionnalité 2** (traitées dans la section 9)
1. Formule du prêt immobilier (taux, durée) ?
2. Définition des « mois couverts » (mois distincts, ou durée entre la première et la dernière dépense) ?

## 9. Étape 5 – Fonctionnalité 3 : simulation de prêt immobilier

**Objectif** (cahier des charges) : à partir de ma dépense « logement » et de mon épargne mensuelle disponible, calculer le montant empruntable avec la formule fournie, dans la limite d'un taux d'endettement de 35 %. L'énoncé ne dit rien du format d'affichage : le tableau ci-dessous est un choix personnel.

**Menu** : « Mortgage Simulator » en 5, « Quit » en 6 ; le message d'erreur du menu indique « between 1 and 6 ».

**Constantes** (en haut du fichier) : `ANNUAL_RATE = 0.05`, `LOAN_YEARS = (10, 15, 20)` (un tuple : valeurs fixes), `MAX_DEBT_RATIO = 0.35`, en plus de `INCOME = 2000`.

**Interprétation de la capacité de remboursement mensuelle**
- Le loyer actuel disparaît avec l'achat : la dépense moyenne mensuelle « housing » (780 € pour Emma) devient de la capacité de remboursement, **en plus** de l'épargne mensuelle disponible.
- Mensualité maximale = min( housing mensuel + épargne disponible ; `INCOME` × `MAX_DEBT_RATIO` ).
- Si l'épargne vaut `None` (revenu insuffisant, voir fonctionnalité 2), on la remplace par 0 : il reste alors le loyer, plafonné à 35 % du revenu.
- Avec le CSV d'Emma : 780,00 + 499,47 = 1 279,47, plafonné à 2 000 × 0,35 = **700 €**.

**Formule du capital emprunté** (annuité constante) : `capital = mensualité × (1 − (1 + t)^(−n)) / t`, avec `t` = taux annuel ÷ 12 et `n` = durée en années × 12.
Implémentation avec la bibliothèque **`numpy-financial`** : `-npf.pv(annual_rate / 12, years * 12, max_capacity)`. `pv` renvoie une valeur négative (la mensualité est un flux sortant), le signe `-` devant la remet positive.

**Dépendance**
- Installation dans le `.venv` : `pip install numpy-financial` (nom d'installation avec un tiret) ; import dans le code : `import numpy_financial as npf` (nom avec un tiret bas).
- Version installée : 1.1.0 (Python 3.14, numpy 2.5.4).
- `.venv` est dans `.gitignore` : sans `requirements.txt`, une autre personne ne saurait pas quoi installer. Le fichier contient `numpy-financial` ; installation : `pip install -r requirements.txt`.

**Organisation du code** : trois fonctions, la première réutilise les fonctions des fonctionnalités 1 et 2.

| Fonction | Reçoit | Renvoie / fait |
|---|---|---|
| `monthly_max_capacity(expenses)` | la liste des dépenses | la mensualité maximale (nombre) ; réutilise `total_expenses`, `months_covered`, `average_expenses_monthly`, `totals_by_category`, `monthly_averages`, `month_savings` |
| `loan_capacity(max_capacity, years, annual_rate)` | la mensualité, la durée en années, le taux annuel | le capital empruntable (nombre), sans `print` |
| `show_loan_available()` | rien | lit les dépenses, garde-fou « historique vide », affiche la mensualité puis une ligne par durée de `LOAN_YEARS` |

**Choix de conception**
- **`loan_capacity` est une fonction pure** : elle ne lit ni fichier ni constante, tout lui est passé en paramètre. On la teste seule (700 €, 5 %, 10 ans). Les noms des paramètres sont en minuscules (`annual_rate`) : la constante `ANNUAL_RATE` n'est écrite qu'à l'appel, dans `show_loan_available`.
- **La mensualité est calculée une fois, avant la boucle** : elle ne change pas d'une durée à l'autre. Seul le capital change, donc l'appel à `loan_capacity` est dans la boucle.
- **`INCOME` et `MAX_DEBT_RATIO` sont lus directement** dans `monthly_max_capacity` (le principe de la constante `INCOME` a été validé avec le mentor pour la fonctionnalité 2) ; en revanche le taux et la durée sont passés en paramètres.
- **Format de l'affichage** : `{valeur:>10,.0f}` : alignement à droite, 10 caractères, séparateur de milliers (virgule), aucune décimale.

Exemple d'affichage avec le CSV d'Emma :

```
--- Mortgage Simulator ---

Monthly payment: 700 Euros

Duration    Amount
10 years    65,997 Euros
15 years    88,519 Euros
20 years   106,068 Euros
```

**Vérifications faites**

| Cas | Résultat observé |
|---|---|
| Mensualité 700 €, 5 %, 10 / 15 / 20 ans, valeurs de référence calculées avant de coder avec la formule | 65 996,95 / 88 518,67 / 106 067,72 € |
| Même cas dans le programme (CSV d'Emma, `INCOME = 2000`) | 65 997 / 88 519 / 106 068 € (65996.945…, 88518.669…, 106067.719… avant arrondi) |
| `INCOME = 1000` (temporaire) | mensualité 350 € (le loyer 780 € est plafonné à 35 % de 1 000) ; 32 998 / 44 259 / 53 034 € |
| Historique vide (`FILENAME` pointant vers un fichier inexistant, temporaire) | « No expense saved yet, add one first. », pas de plantage |

**Pièges rencontrés**
- **Ordre des arguments de `npf.pv`** : la signature est `pv(rate, nper, pmt)`. En passant les valeurs dans le mauvais ordre, le programme tournait sans erreur mais affichait 507 € : la mensualité était lue comme une valeur finale. Corrigé en vérifiant chaque argument (taux **mensuel**, nombre de **mois**, mensualité).
- **Tuple multiplié** : `LOAN_YEARS * 12` ne multiplie pas les nombres, il **répète le tuple** 12 fois (36 éléments), sans message d'erreur. Il faut travailler sur une seule durée à la fois, avec la boucle.
- **Paramètre qui a le même nom que la constante** : écrire `ANNUAL_RATE` comme nom de paramètre masque la constante et enfreint la convention (majuscules réservées aux constantes). Corrigé en `annual_rate`.
- **Un test laissé dans le code** : voir la section 6 (`FILENAME` modifié pour le test de l'historique vide).

**Limites constatées**
- **Taux, durées, revenu et plafond sont fixés dans le code** : ni saisis ni lus dans un fichier. Un taux nul n'a pas été testé.
- **Calcul simplifié** : ni frais de notaire, ni assurance, ni apport, ni durée de recherche du bien ; la même mensualité maximale est supposée pour les trois durées.
- **Le loyer disparaît entièrement** : on suppose que la dépense « housing » devient capacité de remboursement. C'est une interprétation de l'énoncé, à confirmer avec le mentor.
- **Dépend des « mois couverts »** : la mensualité utilise les moyennes mensuelles (voir section 7, question 3).
- **Épargne négative traitée comme 0** : cas du `INCOME = 1000` ; l'application ne le signale pas à l'utilisateur.
- **Présentation du tableau** : montants arrondis à l'euro, durée sur 2 caractères (suffisant pour 10, 15, 20) ; une durée à 3 chiffres décalerait la colonne.

**Questions à poser au mentor**
1. L'interprétation « loyer actuel + épargne disponible, plafonné à 35 % du revenu » correspond-elle à ce qui est attendu ?
2. Définition des « mois couverts » : on garde les mois distincts avec au moins une dépense ?
3. Le format d'affichage (une ligne par durée, avec la mensualité en tête) est-il acceptable ?
