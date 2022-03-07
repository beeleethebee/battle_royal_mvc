# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the bin/rails db:seed command (or created alongside the database with db:setup).
#
# Examples:
#
#   movies = Movie.create([{ name: "Star Wars" }, { name: "Lord of the Rings" }])
#   Character.create(name: "Luke", movie: movies.first)

Category.destroy_all
User.destroy_all
Article.destroy_all


NAMES = %w[Gaming Modding Crypto Informatique 18+]
Category.create(NAMES.map {|name| { name:name } })
p "Created successfully #{Category.count} categories"

User.create(email: 'a@gmail.com', username: 'asd', password_digest: 'aaass')
User.create(email: 'b@gmail.com', username: 'asd', password_digest: 'aaass')
User.create(email: 'c@gmail.com', username: 'asd', password_digest: 'aaass')
User.create(email: 'd@gmail.com', username: 'asd', password_digest: 'aaass')
p "Created successfully #{User.count} users"

Category.all.each do |category|
  User.all.each do |user|
    rand(0...10).times do |i|
      Article.create!(category: category, user: user, title: "Lorem", body: "LOREM stronger")
    end
  end
end
p "Created successfully #{Article.count} articles"
