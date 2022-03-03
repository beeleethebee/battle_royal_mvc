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

Habitué du rails, je cherche une commande qui fais tout le travail à ma place. Je tombe assez rapidement sur `php bin/console make:controller [EntityName]`.
C'est parfait cela me génère le CRUD pour mon Entité exactement comme un `rails g scaffold` ferais.

<div style="display: flex; width: 100%; justify-content: space-evenly;">

<div style="width: 40%">

L'architecture de génération est super... originale 🤯. Pour les controllers et les entities sela me semble normal d'être regroupé ensemble. Cependant je ne comprends pas tellement
l'apport du dossier `Form` et `Repository`. De ce que je comprends, on doit pouvoir générer nos formulaires directement depuis une classe PHP. Je trouve cela vraiment très limitant car
pour suivre la doctrine de symfony cela nous impose d'avoir nos formulaires toujours pareils. Je pense qu'avec de petites entité cela ne pose pas de problème, mais lorsque l'on commence à avoir
des formulaires imbriqués des dépendances de ressources cela ne doit vraiment pas être pratique du tout. Les `Repository` sont comme le guide d'utilisation propre à une entité. C'est-à-dire que si
je veux fetch de la donné je dois obligatoirement passer par cette class pour interagir avec ma base de donnée. Je pense que c'est quelque chose d'intéressant d'avoir décorrélé les méthodes propres à une
entité, qui sont utilisé pour la manipuler, des méthodes pour rechercher la donnée. Cela rajoute une couche de complexité, certes, mais au moins le code est mieux découpé.
</div>

<div style="width: 20%">

![](screenshots/architecture.png)
</div>


</div>



Passons à la structure même des controllers :
```php
# /src/Controller/ArticleController.php

#[Route('/article/new', name: 'article_new', methods: ['GET', 'POST'])]
public function new(Request $request, EntityManagerInterface $entityManager): Response
{
    $this->denyAccessUnlessGranted('ROLE_USER');
    $article = new Article();
    $user = $this->getUser();
    $article->setWriter($user);
    $form = $this->createForm(ArticleType::class, $article);
    $form->handleRequest($request);

    if ($form->isSubmitted() && $form->isValid()) {
        $entityManager->persist($article);
        $entityManager->flush();

        return $this->redirectToRoute('article_index', [], Response::HTTP_SEE_OTHER);
    }

    return $this->renderForm('article/new.html.twig', [
        'article' => $article,
        'form' => $form,
    ]);
}
```

Premièrement, voyons le routing. Symfony dispose de 5 manières de déclarer ses routes, c'est beaucoup trop ! 
On peut choisir d'utiliser :
- Les Annotations dans le controller 😌
- Les Attributs dans le controller 😊
- Un fichier YAML 😕
- Un fichier XML 😬
- Un fichier PHP 💀

Pour simplifier au maximum la syntaxe je décide d'utiliser les attributs car c'est ce qui demande le moins de ligne et de caractères.
Son fonctionnement est très simple. J'indique le path auquel je veux rattacher ma méthode, je lui donne un nom générique afin de la retrouver indépendamment du path puis je renseigne les méthodes HTTP autorisé. C'est très simple et ça fonctionne on ne peut pas en attendre davantage.

Ensuite viens la définition de la méthode de controller elle-même. Le premier élément qui me chagrine vraiment c'est le fait de devoir passer des paramètres à ma méthode. C'est vraiment juste de la magie noire. Pour pouvoir lire les paramètres de ma requêtes ou pour pouvoir persister
mon entité je dois passer un paramètre dans ma fonction qui instancie les objects qui me permettent de le faire. C'est si compliqué et inutile pour rien.

Enfin, j'arrive à écrire ce que je souhaite faire sans gêner le code auto-généré : refuser l'accès à l'utilisateur non connecté et mettre par défaut le créateur de l'article en cours comme étant l'utilisateur connecté. Le code est assez lisible
dans son ensemble. Je trouve cela quand même redondant de devoir passer par un `EntityManager` pour persister mon entité plutôt que de faire par exemple `$article->save()`. Je trouve cette syntaxe inutile et j'ai vraiment l'impression d'être passé à côté de quelque chose de plus simple.

Pour finir, les vues. Symfony utilise Twig pour faire ses templates. Sa syntaxe est vraiment très simple, ce n'est pas du PHP donc forcément... 😇

```html
{% for article in articles %}
    <tr>
        <td>{{ article.title }}</td>
        <td>{{ article.writer.email }}</td>
        <td>
            <a href="{{ path('article_show', {'id': article.id}) }}">show</a>
            {% if article.writer == app.user %}
                <a href="{{ path('article_edit', {'id': article.id}) }}">edit</a>
                {{ include('article/_delete_form.html.twig') }}
            {% endif %}
        </td>
    </tr>
    {% else %}
    <tr>
        <td colspan="3">no records found</td>
    </tr>
{% endfor %}
```

La double accolade `{{` sers à interpoler de la donnée dans la vue quant à `{%` sert aux conditions et aux boucles. Il est tout de même important de lire la [documentations de twig](https://twig.symfony.com/doc/3.x/templates.html) afin de bien l'utiliser.

## 4. Les difficultés

Sincèrement le projet n'a pas été trop compliqué. La partie la plus "dure" c'est de devoir lire des pages de documentations dans son intégralité pour être sûr d'être dans la bonne direction.

Cependant je peux lister quelques tâches qui ont été plus longues que ce que j'aurai aimé :
1. Mettre une root page. Comme en Rails on doit manuellement définir la homepage je pensais vraiment qu'en Symfony il y aurais quelque chose de similaire. Ma solution -> J'ai retiré la base url de mon `ArticleController` pour forcer l'url `/`
à être la root url.
   
2. J'ai eu un problème de routes qui s'entrecroisent avec le login et les commentaires. La conséquence est que lorsque j'essayais de me connecter le serveur comprenais que je voulais supprimer un commentaire et du coup `500`.

3. J'ai trop longtemps voulu essayer d'utiliser la méthode HTTP `DELETE` pour mes routes de suppression de ressource. Je n'ai pas réussi à le faire fonctionner donc j'ai rapidement céder à la simplicité de laisser la méthode en `POST`.


## Conclusion 

Sincèrement, ce fût une expérience agréable. Pas suffisamment pour que je fasse un nouveau projet avec Symfony, mais je ne regrette pas d'avoir fait cette expérience.

### Je note ce framework à 14/20


#### Les plus
- Une documentation incroyable, qui suit vraiment le développeur et qui t'aide à comprendre les bases dont tu as besoins pour faire du MVC
- Des commandes faciles qui aident beaucoup au développement (mention spéciale à l'entity maker)
- Pleins de façon de consommer le framework. Même si ce n'est pas le cadre de ce projet, on peut facilement y brancher un framework JS front et s'affranchir de twig

#### Les moins
- C'est du PHP. Le code PHP n'est pas forcément le plus lisible. Je n'aime toujours pas PHP.
- Les EntityForm pour moi c'est un gros moins car même si l'idée est bonne on perds énormément en flexibilité dans le développement des formulaires pour faire quelque chose de très custom.


J'ai cette sensation d'avoir reçu un cadeau de noël que j'ai envie de revendre à CashConverter après avoir joué pendant 4 heures. C'étais cool le temps que ça a duré mais je ne me projette absolument pas l'utiliser davantage. 