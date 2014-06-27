class User < ActiveRecord::Base
  attr_accessible :email, :name

  def mail_user
    p self 
    UserMailer.demo_mail(self).deliver!
  end
end
