class Comment < ApplicationRecord
  belongs_to :article
  belongs_to :user
  validates :body, presence: true, length: { minimum: 10 }
end
