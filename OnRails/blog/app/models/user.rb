class User < ApplicationRecord
    has_many :comments
    has_many :articles
    # adds virtual attributes for authentication
    has_secure_password
    # validates email
    validates :email, presence: true, uniqueness: true, format: { with: /\A[^@\s]+@[^@\s]+\z/, message: 'Invalid email' }

end
