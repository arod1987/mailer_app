require 'json'

class ReviewPainer
	def self.review_painer
		#command = "python /home/arunkumar/work/rails_projects/mailer_app/script/user_parser.py"

		#value = `#{command}`

		#command = "python /home/arunkumar/work/rails_projects/mailer_app/script/review_parser.py"

		#value = `#{command}`

		file = File.read("/home/arunkumar/work/rails_projects/mailer_app/script/out.json")

		file1 = File.read("/home/arunkumar/work/rails_projects/mailer_app/script/user.json")

		data_hash = JSON.parse(file)

		user_hash = JSON.parse(file1)

		answer = {}

		data_hash.each do
			
			|x,y|
			common = []
			y.each do
				|a,b|
				if a=="reviewers"
					b.each do |reviewer_name,no_of_unadrressed|
					m = {}
					m[reviewer_name] = user_hash[reviewer_name]
					  unless answer.has_key? m
						answer[m] = []
					  end
					  c=[]
					  c.push(no_of_unadrressed)
					  answer[m].push(common + c)
					end
		        else
					common.push(b)
			    end
			end	
		end

		puts answer

		answer.each do |answer|
			UserMailer.demo_mail(answer.first.first, answer.second).deliver!
		end
	end
end

