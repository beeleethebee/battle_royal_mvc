class Article < ApplicationRecord
    has_many :comments
    has_one :users
    has_one :category
    validates :title, presence: true
    validates :body, presence: true, length: { minimum: 10 }
end
