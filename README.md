# Large Scale Data Management Project: Benchmark de Performance du PageRank

## Description du Projet

Ce projet a pour objectif d'évaluer les performances de l'algorithme PageRank implémenté sur les DataFrames et les RDD (Resilient Distributed Datasets) sur Google Cloud Platform (GCP).

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

### Résultats du Benchmark

Les benchmarks ont été réalisés en variant le nombre de travailleurs pour chaque technologie, comme détaillé ci-dessous :

#### RDD

| Nombre de Travailleurs | Temps RDD avec partitionnement | Temps RDD sans partitionnement |
| ---------------------- | ------------------------------ | ------------------------------------ |
| 1                      | 44.99299740791321 s             | 45.278162717819214 s                     |
| 2                      | 37.06561207771301 s          | 37.021756649017334 s                       |
| 4                      | 36.382244348526 s           | 36.139880895614624 s                     |

#### DataFrame

| Nombre de Travailleurs | Temps DataFrame avec partitionnement | Temps DataFrame sans partitionnement |
| ---------------------- | ----------------------------------- | ------------------------------------- |
| 1                      |                  |                         |
| 2                      |                   |                         |
| 4                      |                  |                         |

## Instructions de Configuration

Pour exécuter les benchmarks, suivez ces étapes :

1. **Configurez un cluster** en utilisant les scripts Bash fournis pour chaque technologie. Par exemple :
    - Pour **RDD** : Exécutez `./runrdd.sh`
    - Pour **PySpark Classique** : Exécutez `./spark-classic.sh`
    - Pour **PySpark Optimisé** : Exécutez `./spark-optimised.sh`

2. **Modifiez le nombre de travailleurs dans les fichiers .sh**

Assurez-vous que votre compte Google Cloud est configuré et que vous disposez des autorisations nécessaires pour lancer des clusters Dataproc.

## Conclusion
