class Article < ApplicationRecord
    has_many :comments
    belongs_to :user
    belongs_to :category

    validates :title, presence: true
    validates :body, presence: true, length: { minimum: 10 }
end
