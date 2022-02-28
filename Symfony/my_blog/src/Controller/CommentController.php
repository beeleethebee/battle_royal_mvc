<?php

namespace App\Controller;

use App\Entity\Article;
use App\Entity\Comment;
use App\Form\CommentType;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;


#[Route('/comment')]
class CommentController extends AbstractController
{

    #[Route('/new/{article_id}', name: 'comment_new', methods: ['POST'])]
    public function new(int $article_id, Request $request, EntityManagerInterface $entityManager): Response
    {
        $this->denyAccessUnlessGranted('ROLE_USER');
        $user = $this->getUser();
        $article = $entityManager->getRepository(Article::class)->find($article_id);
        $comment = new Comment();
        $comment->setWriter($user);
        $comment->setArticle($article);
        $form = $this->createForm(CommentType::class, $comment);
        $form->handleRequest($request);

        if ($form->isSubmitted() && $form->isValid()) {
            $entityManager->persist($comment);
            $entityManager->flush();

            return $this->redirectToRoute('article_show', ["id" => $comment->getArticle()->getId()], Response::HTTP_SEE_OTHER);
        }
    }



    #[Route('/{id}', name: 'comment_delete', methods: ['POST'])]
    public function delete(Request $request, Comment $comment, EntityManagerInterface $entityManager): Response
    {
        $article = $comment->getArticle();
        if ($this->isCsrfTokenValid('delete'.$comment->getId(), $request->request->get('_token'))) {
            $entityManager->remove($comment);
            $entityManager->flush();
        }

        return $this->redirectToRoute('article_show', ['id' => $article->getId()], Response::HTTP_SEE_OTHER);
    }
}
