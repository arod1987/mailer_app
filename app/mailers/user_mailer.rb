class UserMailer < ActionMailer::Base
  default from: "from@example.com"

  def demo_mail(user, reviews)
    @user = user.first
    #@email = user.email
    @email = "ishan.dutta@chronus.com"
    @reviews = reviews
    mail(:from => "Testmail@demo.com",
       :to => @email,
       :subject => "Greet User",
       :template => "demo_email")    
  end 
end
