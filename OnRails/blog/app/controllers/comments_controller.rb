class CommentsController < ApplicationController
  def create
    @article = Article.find(params[:article_id])
    @comment = Comment.new(comment_params)
    @comment.user = Current.user
    @comment.save!

    redirect_to article_path(@article)
  end

  def destroy
    @comment = Comment.find(params[:id])
    @comment.destroy
    redirect_to article_path(params[:article_id])
  end

  def comment_params
    params.permit(:body, :article_id)
  end

end
