# Large Scale Data Management Project: Benchmark de Performance du PageRank

## Description du Projet

Ce projet a pour objectif d'évaluer les performances de l'algorithme PageRank implémenté sur les DataFrames et les RDD (Resilient Distributed Datasets) sur Google Cloud Platform (GCP).

## Membres du groupe : 

- Loay Chlih ( ATAL)
- Mohammed Hmitouch (ATAL)

## Ressources Fournies

- **Crédit de 50 $ par personne** sur Google Cloud Platform pour configurer et utiliser les clusters.

## Processus de Benchmarking

Tous les scripts utilisés pour les benchmarks sont situés dans le répertoire `scripts`.

Chaque dossier contient des scripts Bash pour créer un cluster et exécuter l'algorithme PageRank, spécifiques aux technologies testées :

- `runrdd.sh` : Exécute PageRank avec RDD (en utilisant `pagerankrdd.py`).
- `rundata.sh` : Exécute PageRank avec DataFrame (en utilisant `pagerankdataframe.py`).

## Configurations des Clusters

Pour cette expérience, plusieurs configurations de clusters ont été utilisées, chacune avec le même matériel CPU/RAM par nœud pour assurer la comparabilité des résultats :

### 1. Cluster à 1 nœud

- **Type de machine** : `n1-standard-4`
- **vCPUs** : 4
- **Mémoire** : 15 Go
- **Disque persistant** : 500 Go
- **SSD local** : Oui
- **Image** : `2.0-debian10`
- **Zone** : `europe-west1-c`

### 2. Cluster à 2 nœuds

- **Type de machine** : `n1-standard-4` (identique à la configuration à 1 nœud)
- **vCPUs** : 4 par nœud
- **Mémoire** : 15 Go par nœud
- **Disque persistant** : 500 Go par nœud
- **SSD local** : Oui
- **Image** : `2.0-debian10`
- **Zone** : `europe-west1-c`

### 3. Cluster à 4 nœuds

- **Type de machine** : `n1-standard-4` (identique à la configuration à 1 et 2 nœuds)
- **vCPUs** : 4 par nœud
- **Mémoire** : 15 Go par nœud
- **Disque persistant** : 500 Go par nœud
- **SSD local** : Oui
- **Image** : `2.0-debian10`
- **Zone** : `europe-west1-c`

## Résultats

### Résultats du Benchmark de small_page_links.nt : 

Les benchmarks ont été réalisés en variant le nombre de travailleurs, comme détaillé ci-dessous :

#### RDD

| Nombre de Travailleurs | Temps RDD avec partitionnement | Temps RDD sans partitionnement |
| ---------------------- | ------------------------------ | ------------------------------------ |
| 1                      | 44.99299740791321 s             | 45.278162717819214 s                     |
| 2                      | 37.06561207771301 s          | 37.021756649017334 s                       |
| 4                      | 36.382244348526 s           | 36.139880895614624 s                     |

#### DataFrame

| Nombre de Travailleurs | Temps DataFrame avec partitionnement | Temps DataFrame sans partitionnement |
| ---------------------- | ----------------------------------- | ------------------------------------- |
| 1                      | 35.75928416307245 s             |     38.97059342108653                   |
| 2                      |   30.59381746290831 s                |   32.61837294508192                 |
| 4                      |    28.40967285139752 s               |     30.78420531967284                 |

#### Entité avec le plus grand page rank : 
L'entité avec le plus grand PageRank est 🏅 <http://dbpedia.org/resource/Attention-deficit_hyperactivity_disorder>' 0.30051150556157313

![TOP10](https://github.com/user-attachments/assets/dfc054e5-b0db-4ef9-a394-62b9716954bc)
#### RDD

| Nombre de Travailleurs | Temps RDD avec partitionnement | Temps RDD sans partitionnement |
| ---------------------- | ------------------------------ | ------------------------------------ |
| 1                      | 44.99299740791321 s             | 45.278162717819214 s                     |
| 2                      | 37.06561207771301 s          | 37.021756649017334 s                       |
| 4                      | 36.382244348526 s           | 36.139880895614624 s                     |

#### DataFrame

| Nombre de Travailleurs | Temps DataFrame avec partitionnement | Temps DataFrame sans partitionnement |
| ---------------------- | ----------------------------------- | ------------------------------------- |
| 1                      |  s             |                        |
| 2                      |    s                |                    |
| 4                      |     s               |                      |

#### Entité avec le plus grand page rank : 
L'entité avec le plus grand PageRank est 🏅 : <http://dbpedia.org/resource/Living_people> ' 36794.33146754483

![TOP10KBIR](https://github.com/user-attachments/assets/1af4b92c-d947-437a-9bc6-53579fc70b1f)

### Résultats du Benchmark de page_links_en.nt.bz2 :


## Instructions de Configuration

Pour exécuter les benchmarks, suivez ces étapes :

1. **Configurez un cluster** en utilisant les scripts Bash fournis pour chaque technologie. Par exemple :
    - Pour **RDD** : Exécutez `./runrdd.sh` en remplacant les donnees par small_page_links.nt
    - Pour **Dataframe** : Exécutez `./rundata.sh`en remplacant les donnees par small_page_links.nt

2. **Modifiez le nombre de travailleurs dans les fichiers .sh**

Assurez-vous que votre compte Google Cloud est configuré et que vous disposez des autorisations nécessaires pour lancer des clusters Dataproc.

## Conclusion
