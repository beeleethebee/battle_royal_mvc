Rails.application.routes.draw do
  root "home#index"

  get "/", to: "home#index"
  get 'sign_up', to: 'registrations#new'
  post 'sign_up', to: 'registrations#create'
  get 'sign_in', to: 'sessions#new'
  post 'sign_in', to: 'sessions#create', as: 'log_in'
  delete 'logout', to: 'sessions#destroy'
  get '/member', to: 'member#index'
  get "/category/:id", to: "category#show"

  resources :articles do
    resources :comments
  end
end
