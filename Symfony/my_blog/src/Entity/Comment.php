<?php

namespace App\Entity;

use App\Repository\CommentRepository;
use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity(repositoryClass: CommentRepository::class)]
class Comment
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column(type: 'integer')]
    private $id;

    #[ORM\Column(type: 'text')]
    private $content;

    #[ORM\Column(type: 'integer', nullable: true, )]
    private $up_vote = 0;

    #[ORM\ManyToOne(targetEntity: User::class, inversedBy: 'comments')]
    #[ORM\JoinColumn(nullable: false)]
    private $writer;

    #[ORM\ManyToOne(targetEntity: Article::class, inversedBy: 'comments')]
    private $article;

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getContent(): ?string
    {
        return $this->content;
    }

    public function setContent(string $content): self
    {
        $this->content = $content;

        return $this;
    }

    public function getUpVote(): ?int
    {
        return $this->up_vote || 0;
    }

    public function setUpVote(?int $up_vote): self
    {
        $this->up_vote = $up_vote;

        return $this;
    }

    public function incrementUpVote(): self
    {
        $this->up_vote++;
        return $this;
    }

    public function decrementUpVote(): self
    {
        $this->up_vote--;
        return $this;
    }

    public function getWriter(): ?User
    {
        return $this->writer;
    }

    public function setWriter(?User $writer): self
    {
        $this->writer = $writer;

        return $this;
    }

    public function getArticle(): ?Article
    {
        return $this->article;
    }

    public function setArticle(?Article $article): self
    {
        $this->article = $article;

        return $this;
    }
}
