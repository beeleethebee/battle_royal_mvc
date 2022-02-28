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

Mon oeil n'as pas pu s'empêcher d'être attiré par la barre dite de _débogage_ situé en bas de la page. Sur cette barre on
y retrouve pas mal d'informations intéressantes : le code http, le temps d'exécution du serveur, la mémoire utilisé et d'autres
éléments qui échappent encore à mon domaine. Je tiens à souligner que je trouve ça assez impressionnant d'avoir autant d'outil.
Sur Rails, il n'y a pas de solution simple pour identifier les `memory leaks` ou encore identifier les `requêtes N+1`. Même si je pense que cela
n'omet pas d'utiliser une solution APM telle que Scout, c'est déjà un bon premier pied à l'étrier pour motiver le développeur
à optimiser son application ! 🏇

## 2. Setup mes premières "Entités"
#### _Parce que chez symfony un Model c'est une Entity_

D'après la documentation, pour créer et manipuler les entités il faut utiliser la commande `php bin/console make:entity`

Je lance la commande et juste Woaw ✨

<div style="width:50%; margin: auto;">

![](screenshots/entity_maker.png)

</div>

__C'est tellement cool à utiliser !__

On peut rapidement créer son entité et la faire évoluer juste en répondant à des questions. Je trouve 
cela sincèrement incroyable en terme d'expérience développeur c'est très intuitif et facile à utiliser.
De plus, pour créer ses relations entre entités c'est également très simplifié

<div style="width:50%; margin: auto;">

![](screenshots/relation_maker.png)

</div>

Je consulte [la documentation](https://symfony.com/doc/current/doctrine.html#creating-an-entity-class)
afin de bien comprendre toutes les questions mais en réalité tout coule de source pour l'instant.

Je génère donc mes entités `Article`, `User`, `Comment` avec une grande aisance 🛼.

Des fichiers correspondants à chacune de mes entités sont apparues dans le dossier `src/`. Première remarque on peut accéder à tous les attributs
de notre entité via son fichier. C'est intéressant à souligner car dans Rails tout est séparé dans plusieurs fichiers pour avoir 
des fichiers très petits. Dans notre cas, tous les attributs ainsi que leurs accesseurs et mutateurs sont disponible dans ce fichier.
Le bon point est que si l'on veut modifier un comportement ou ajouter un callback sur certaines actions c'est facile. Cependant
je pense que cela arrive très rarement car dans la majorité des cas on va créer une nouvelle méthode juste pour notre utilisation.

```php
# /src/Entity/Article.php
    
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column(type: 'integer')]
    private $id;

    #[ORM\Column(type: 'text')]
    private $content;

    #[ORM\ManyToOne(targetEntity: User::class, inversedBy: 'articles')]
    #[ORM\JoinColumn(nullable: false)]
    private $writer;

    #[ORM\Column(type: 'string', length: 100)]
    private $title;

    #[ORM\OneToMany(mappedBy: 'article', targetEntity: Comment::class)]
    private $comments;
```


## 3. Vues, controllers et routing