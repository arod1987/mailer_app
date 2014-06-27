class UserMailer < ActionMailer::Base
  default from: "from@example.com"

  def demo_mail(user, reviews)
    @user = user.first
    #if user.second != nil
    #  @email = user.second
    #else
    #  @email = "astest.chronus@gmail.com"
    #end
    @email = "astest.chronus@gmail.com"
    @reviews = reviews
    mail(:from => "Testmail@demo.com",
       :to => @email,
       :subject => "Review Painer Digest",
       :template => "demo_email")    
  end 
end
