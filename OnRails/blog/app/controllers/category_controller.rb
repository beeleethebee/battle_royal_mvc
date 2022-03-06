class CategoryController < ApplicationController
  def show
    @articles = Article.where(category_id: params[:id])
    
  end
end
