class MemberController < ApplicationController
    def index
        @users = User.all
    end
end
