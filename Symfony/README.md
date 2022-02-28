# Symfony
### Mon aventure en tant que symfoniste néophyte


## Introduction

Mon premier contact avec PHP a été lors de mon apprentissage basique du développement en école. Je n'ai jamais vraiment aimé la syntaxe.
Encore fraîchement traumatisé par les pointeurs en C, me revoilà jouant avec des flèches et des $ 🤨. À l'époque j'ai décidé le plus vite 
possible d'arrêter d'utiliser cette techno que je jugeais horrible à utiliser, `old school`. Je me suis alors tourné vers Ruby 💎 et vraiment 
ça a été le coup de foudre direct. Pendant plus de 3 ans je n'ai juré que par Ruby pour faire mes scripts, mes API, mes WebApp, mon café, etc.

Aujourd'hui j'ai grandi, il est temps d'établir un deuxième contact avec l'étrange et de passer au-dessus des mauvais souvenirs. 
Je vais donc, avec beaucoup de préparation physique et mentale, utiliser Symfony et rendre compte de comment s'est déroulé mon expérience.


## 1. Installation de Symfony et setup du projet

Comme le sujet l'impose, j'ai suivi la documentation [officielle de symfony](https://symfony.com/doc/current/setup.html#creating-symfony-applications).

`symfony new my_blog --webapp`

L'installation se déroule sans accroc, déjà un bon point 🥳 ! Toutes les dépendances via composer se sont
installées automatiquement. Dans mon projet je n'ai a priori pas besoin d'installer de dépendance JavaScript, 
ce qui est aussi un bon point pour moi.

J'essaye de créer la base de base de donnée et là je me confronte à mon premier mur, le fichier `.env` 🥊.

Voici la partie qui nous intéresse :

```.dotenv
APP_ENV=dev
APP_SECRET=acc37c4b0327fe0388b6922007fa1ca7
# DATABASE_URL="sqlite:///%kernel.project_dir%/var/data.db"
# DATABASE_URL="mysql://db_user:db_password@127.0.0.1:3306/db_name?serverVersion=5.7&charset=utf8mb4"
DATABASE_URL="postgresql://blog:ChangeMe@127.0.0.1:5432/app?serverVersion=13&charset=utf8"
```

Il se trouve que par (mauvaise) habitude j'utilise postgresql sans utilisateur et sans rôle en dev -> aucune sécurité.
J'ai dû passer une bonne trentaine de minute avant de trouver LA combinaison qui fais que la base de donnée se créée bien :

```dotenv
DATABASE_URL="postgresql://:blog@127.0.0.1:5432/app?serverVersion=13&charset=utf8"
```

Je trouve que laisser la syntaxe en forme d'URL induit beaucoup à la confusion, comparé à Rails qui ordonne les
informations de configurations de base de donnée dans un fichier `.yml` où les informations y sont bien plus claires.

Finalement, la commande de création de base de donnée fonctionne enfin, je peux donc lancer mon serveur et atterrir sur cette LA page de bienvenue :
<div style="width:50%; margin: auto;">

![](screenshots/welcome_page.png)

</div>

## 2. Setup mes premières "Entités"
#### _parce que chez symfony un Model c'est une Entity_

