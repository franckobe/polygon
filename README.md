                                          _ \       |
                                         |   | _ \  | |   |  _` |  _ \  __ \
                                         ___/ (   | | |   | (   | (   | |   |
                                        _|   \___/ _|\__, |\__, |\___/ _|  _|
                                                     ____/ |___/
                                        



#Search engine called Polygon

## Database
### On utilise un trigrame pour differencier les tables rapidement et favoriser l'indentation

### Table contenant la liste des nom de domaines. Le champ LDW_IS_ALLOW permet de savoir si le domaine à été validé ou pas. On ajoute en clé etrangère le propriétaire du domaine (si on le connait)i
LDW_LIST_DOMAIN_WEBSITE
LDW_ID(AI), LDW_NAME(String), LDW_IS_ALLOW(1 : yes, 0 : no, -1 : in progress), LDW_OWNER_ID,

### Table contenant la liste des pages qu'on index. Et on y ajoute le contenu de la table parsé en xml. Cette table est liée avec la table LDW en clé etrangère
LWP_LIST_WEBSITE_PAGE
LWP_ID(AI), LWP_URL(string), LWP_CONTENT(string), LDW_ID

### Table pour les catégories de site que l'on peux rencontrer
CSW_CATEGORY_WEBSITE
CSW_ID(AI), CSW_CATEGORY(string)

### Table de concaténation entre les pages et les catégories de sorte a pouvoir avoir une relation many to many
DCW_DOMAIN_CATEGORY_WEBSITE
CSW_ID, LDW_ID

### Table pour les propriétaires de domaine (si on le connait via les meta=author
ODW_OWNER_DOMAIN_WEBSITE
ODW_ID(AI), ODW_NAME(string), ODW_TYPE (entreprise, Person…), ODW_CITY, ODW_ADRESS… ?

### liste des key word avec leurs poids par page (ou nom de domaine ?)
LKW_LIST_KEY_WORD
LKW_ID(AI), LKW_VALUE, LKW_PONDERATION, LWP_ID

### Historique de recherche des utilisateurs
HUS_HISTORY_USER_SEARCHING
HUS_ID, USERS_ID, HUS_LKW_ID, HUS_TIMESTAMP

### Table utilisateur
USER
USER_ID, USER_LOGIN, USER_PASSWORD, USER_SURNAM, USER_LASTNAME, USER_PICTURE, USER_CREATE, USER_UPDATE, USER_BIRTHDAY, USER_ADRESS

