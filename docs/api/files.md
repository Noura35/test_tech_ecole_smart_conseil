# Module Files

Le module `files` gère l'upload, le stockage et la gestion des fichiers associés aux écoles.  
Il fournit : modèles, sérialiseurs, vues API, utilitaires, validateurs et tests complets.

---

## 1. Modèles

### 1.1 Fichier principal

::: files.models.File
- Représente un fichier lié à une école.
- Champs : `file`, `filename`, `file_type`, `file_size`, `mime_type`, `description`, `uploaded_by`, `ecole`.
- Méthodes : 
    - `save()` : extraction automatique des métadonnées
    - `delete()` : suppression du fichier physique
    - `get_file_size_display()` : retourne la taille formatée

---

## 2. Sérialiseurs

### 2.1 Sérialiseur complet

::: files.serializers.FileSerializer
- Sérialiseur détaillé pour CRUD complet.
- Champs calculés : `uploaded_by_username`, `ecole_name`, `file_size_display`, `file_url`.

### 2.2 Sérialiseur pour upload

::: files.serializers.FileUploadSerializer
- Pour l’upload de fichiers.
- Validation : existence de l’école.

### 2.3 Sérialiseur pour listes

::: files.serializers.FileListSerializer
- Sérialiseur léger pour afficher les fichiers dans des listes.
- Champs : `id`, `filename`, `file_type`, `file_size`, `ecole_name`, `uploaded_by_username`, `uploaded_at`.

---

## 3. Vues

### 3.1 ViewSet principal

::: files.views.FileViewSet
- Gestion complète CRUD via DRF.
- Actions personnalisées : `download`, `upload_multiple`.
- Filtrage : par école, type de fichier, fichiers de l'utilisateur.
- Permissions :
    - Admin uniquement pour suppression et mise à jour.
    - Authentification requise pour lecture et upload.

---

## 4. Utils

::: files.utils
- Fonctions utilitaires :
    - `get_file_path()` : chemin de stockage
    - `determine_file_type()` : type basé sur l'extension
    - `get_mime_type()` : détection du type MIME

---

## 5. Validators

::: files.validators
- Validation des fichiers :
    - `validate_file_size()` : limite 10MB
    - `validate_file_extension()` : extensions autorisées

---

## 6. URLs

::: files.urls

### 6.1 Routes API disponibles

| Méthode | Endpoint                   | Action |
|---------|----------------------------|--------|
| GET     | /api/files/                | Liste fichiers (filtrable) |
| POST    | /api/files/                | Upload fichier unique |
| POST    | /api/files/upload_multiple/| Upload multiple fichiers |
| GET     | /api/files/{id}/           | Détails d'un fichier |
| PUT     | /api/files/{id}/           | Mise à jour (admin) |
| PATCH   | /api/files/{id}/           | Mise à jour partielle (admin) |
| DELETE  | /api/files/{id}/           | Suppression (admin) |
| GET     | /api/files/{id}/download/  | Téléchargement fichier |

---

## 7. Tests

### 7.1 Description générale
- Contient des **tests unitaires et d'intégration** pour valider le fonctionnement du module File.
- Tests sur : modèles, API (CRUD), filtrages, upload simple et multiple, suppression, téléchargement, pagination.

::: files.tests

### 7.2 Tableau récapitulatif des tests

| Catégorie                | Test                                    | Description / Comportement attendu                                                                 | Asserts principaux |
|---------------------------|----------------------------------------|---------------------------------------------------------------------------------------------------|------------------|
| **Modèle**               | Création fichier                        | Vérifie `filename`, `file_type`, `file_size` et `mime_type`                                        | `filename`, `file_type`, `file_size > 0`, `mime_type` correct |
|                           | Suppression physique                     | Supprime l'objet File et le fichier sur le disque                                                | Fichier existait avant, fichier supprimé après |
|                           | Formatage taille                         | Vérifie `get_file_size_display()` retourne une chaîne lisible (B, KB, MB)                         | Contient unité `KB` pour 2KB |
| **API - Upload**          | Upload fichier unique                   | Authentifié peut uploader un fichier                                                              | Status 201, objet File créé, `uploaded_by` correct |
|                           | Upload multiple fichiers                | Upload simultané de plusieurs fichiers                                                           | Tous fichiers créés, erreurs collectées |
|                           | Upload sans authentification            | Non authentifié ne peut pas uploader                                                              | Status 401/403, aucun fichier créé |
| **API - Lecture / List**  | Liste fichiers                          | Récupération de la liste complète ou filtrée                                                    | Status 200, nombres corrects, champs calculés (`file_size_display`) |
|                           | Filtrage par école                       | Filtrage fichiers pour une école spécifique                                                     | Status 200, uniquement fichiers de l'école demandée |
|                           | Filtrage par type                        | Filtrage fichiers par `file_type`                                                               | Status 200, tous fichiers retournés ont le type demandé |
|                           | Filtrage par utilisateur (`my_files`)   | Affiche uniquement fichiers uploadés par l'utilisateur courant                                  | Status 200, fichiers uniquement de l'utilisateur |
|                           | Détails d’un fichier                     | Récupère les détails d’un fichier spécifique                                                    | Status 200, `filename`, `description`, `ecole_name` corrects |
| **API - Suppression**     | Suppression utilisateur standard         | Non admin ne peut pas supprimer                                                                  | Status 403, fichier toujours en base |
|                           | Suppression par admin                    | Superuser peut supprimer                                                                        | Status 204, fichier supprimé |
| **API - Téléchargement**  | Download fichier                         | Vérifie téléchargement avec headers corrects                                                    | Status 200, `Content-Disposition` correct, mime_type correct |
| **Tests sans pagination** | Lecture / filtrage simplifié            | Filtrage et lecture quand pagination désactivée                                                | Status 200, fichiers filtrés correctement |
