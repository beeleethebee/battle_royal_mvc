class ArticlesController < ApplicationController
  def show
    @article = Article.find(params[:id])
    @user = User.find(@article.users_id)
  end

  def new
    @article = Article.new
    @categorys = Category.all
  end

  def create
    @article = Article.new(article_params)
    

    if @article.save
      redirect_to @article
    else
      render :new, status: :unprocessable_entity
    end
  end

  def edit
    @article = Article.find(params[:id])
  end

  def update
    @article = Article.find(params[:id])

    if @article.update(article_params)
      redirect_to @article
    else
      render :edit, :unprocessable_entity
    end
  end
  
  def destroy
    @article = Article.find(params[:id])
    @article.destroy

    redirect_to root_path, status: :see_other
  end


  private
    def article_params
      users_id = { users_id: Current.user.id }
      params.require(:article).permit(:title, :body, :category_id, :users_id).reverse_merge(users_id)
    end
end
