namespace :demo do
  desc "This is to send an email to users"
    task(:mail_users => :environment) do
      ReviewPainer.review_painer
    end
end
