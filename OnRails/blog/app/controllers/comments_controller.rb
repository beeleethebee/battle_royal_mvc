class CommentsController < ApplicationController
  def create
    @article = Article.find(params[:article_id])
    @comment = Comment.new(comment_params)
    
  end

end
