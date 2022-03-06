class HomeController < ApplicationController
  def index
    @user_current = Current
    @category = Category.all
  end

end
