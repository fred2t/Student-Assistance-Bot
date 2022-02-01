from typing import *
import discord#type:ignore

from udb import data

StudentInfo = Union[int, str]
Course = str
ComparableProfileInformation = Union[StudentInfo, Set[StudentInfo]]
StudentProfile = Tuple[StudentInfo]
PARTNER_PROGRAM_PARTICIPANTS = "partner program participants.txt"



class Partnership:
	def __init__(self) -> None:
		self.discord_username_index = 1
		self.interests_index = 8
		
		


	def create_partner_participant_file(self) -> None:
		"""create a file to contain all the people who can be partner-matched with, all of which 
		voluntarily chosed to participate with the partnering
		SHOULD ONLY ran once to avoid overriding an existing file due to 'w'"""

		with open(PARTNER_PROGRAM_PARTICIPANTS, 'w', encoding='cp1252') as f:
				f.write('')




	def get_user_username(self, user_id: int) -> str:
		"""e"""

		return data.get_profile('profiles', user_id)[0][self.discord_username_index]




	

	

	def person_information(self, userid: int) -> Tuple[ComparableProfileInformation, Set[Course]]:
		"""returns a user's grade/clubs/hours/interests/courses specifically.
			used as a convenient tool to grab specific items from the tables quicker"""

		profile = list(
			data.cur.execute(
				"""
				SELECT 
				Username, Grade, Hours, Clubs, Interests 
				FROM profiles WHERE UserID = (?)
				""",
				(userid,)
			)
		)

		assert profile, f"Profile for user (id: {userid}) does not exist."
	 
		profile = profile[0]
		# print(profile)

		profile = profile[1 : 3] + (
			set(profile[3].split(', ')),
			set(profile[4].split(', '))
		)

		# returns list of course codes in tuples, ex. [('MCR3U0',), ('PPL3OM',), ('ICS3U0',), ('ENG3U0',), ('SCH3U0',), ('SPH3U0',), ('MDM4U0',), ('SES4U0',)]
		courses = list(
			data.cur.execute("SELECT Course FROM courses WHERE UserID = (?)", (userid,))
		)
		# print(courses)

		assert courses, f"Courses for user (id: {userid}) does not exist."

		return profile, set(tupl[0] for tupl in courses)




	def affinity(self, p1: int, p2: int) -> int:
		"""finds the affinity between two users in points
		generally used where: p1=command caller, p2=person to compare with"""

		# 5 factors: grade: 1, clubs: 8, hours: 3, interests: 10, courses: 5
		# already tuple, no need another parentheses pair
		(p1_grade, p1_hours, p1_clubs, p1_interests), p1_courses = self.person_information(p1)
		(p2_grade, p2_hours, p2_clubs, p2_interests), p2_courses = self.person_information(p2)

		# we add to this because if we add each thing at the end, there might not exist something to add
		affinity_points = 0
		

		
		# points based on commonalities

		# check if the two people are aged within one year of each other
		# (usually high-schoolers don't value spending time with people >1 year apart)
		# awards more points depending on the difference in grade years
		if p1_grade and p2_grade:
			for award_point, grade_diff in enumerate(range(3, -1, -1)): 
				if abs(p1_grade - p2_grade) == grade_diff:
					affinity_points += award_point * (abs(p1_grade - p2_grade) == grade_diff)
					break
				

		# all printing for debugging
		# print(p1_grade, p2_grade)
		# print(3 * (p1_grade - p2_grade < 2))
		# print(affinity_points)


		# check if the two people have a 10 hour difference within their volunteer hours
		# (people who volunteer a lot would like to meet like-minded-hyper-volunteers, or people with
		# a moderate amount just want to talk about experiences with people within their range of
		# time invested)

		# more points awarded as hour range increases in multiples of 40
		no_of_mults40 = max(p1_hours, p2_hours) // 40 if max(p1_hours, p2_hours) % 40 == 0 else max(p1_hours, p2_hours) // 40 + 1
		for award_point in range(no_of_mults40, -1 , -1):
			if abs(p1_hours - p2_hours) < 11:
				affinity_points += award_point / 2
				break



		affinity_points += 10 * len(p1_interests & p2_interests)
		# print(p1_interests, p2_interests)
		# print(10 * len(p1_interests & p2_interests))
		# print(affinity_points)

		
		affinity_points += 5 * len(p1_courses & p2_courses)
		# print(p1_courses, p2_courses)
		# print(5 * len(p1_courses & p2_courses))
		# print(affinity_points)

		# ((0, 0, {'None'}, {'interest2', 'interest1'}), {'MCR3U0', 'SES4U0', 'ENG3U0', 'ICS3U0', 'MDM4U0', 'SPH3U0', 'SCH3U0', 'PPL3OM'})
		
		# this will alawys give 8 points at the moment because profile default is a 'None' string
		affinity_points += 8 * len(p1_clubs & p2_clubs)
		# print(p1_clubs, p2_clubs)
		# print(8 * len(p1_clubs & p2_clubs))
		# print(affinity_points)

		return affinity_points

	








	def partner_eligible(self, user_affinity_score: int, highest_affinity: int, min_partnerable_affinity: Optional[Union[float, int]] = 39) -> bool: 
		"""check if potential partner-person is qualified to partnered with the first user"""
		
		assert not isinstance((user_affinity_score, highest_affinity, min_partnerable_affinity), (int, float)), \
			'Type(s) of arguments are not a number'

		return user_affinity_score > highest_affinity * 0.8 and user_affinity_score > min_partnerable_affinity




	def user_participating(self, userid: int) -> bool:
		"""checks if a user is participating in the partner program"""
			
		with open(PARTNER_PROGRAM_PARTICIPANTS, 'r', encoding='cp1252') as f:

			# type changed to int because both read() and split() return strs
			return userid in map(int, f.read().split())
			



	def add_participant_to_program(self, userid: int) -> None:
		with open(PARTNER_PROGRAM_PARTICIPANTS, 'r+', encoding='cp1252') as f:
		#   x = f.read()
		#   print(x)
		#   print(bool(x))

		
			# check if text file is empty
			if not f.read():
					
				f.write(str(userid))
					
			else:
				# no need to cnovert to stirng, already f string
				f.write(f" {userid}")


	
	def add_attribute(self, userid: int, attr: Literal['interests', 'clubs'], old_attrs: str, attrs_to_add: str) -> None:
		"""add additional interests/participations to interests/clubs list"""

		with data.connection:
			data.cur.execute(f"""UPDATE profiles 
								SET {attr}=:int 
								WHERE UserID=:uid""", 
								{'int': old_attrs + attrs_to_add, 'uid': userid})


	
	def remove_attribute(self, userid: int, attr: Literal['interests', 'clubs'], original_attrs: str, to_remove: List[str]) -> None:
		"""remove interests/participations to interests/clubs list"""

		

		original_interests = original_attrs.split(', ')

		# cant use replace cause wouldnt work if it was first item in string - no comma to find
		for interest in to_remove:
			assert interest in original_interests, "Given interest is not in profile"

			original_interests.remove(interest)



		updated_attributes = ', '.join(original_interests)
		
		with data.connection:
			data.cur.execute(
				f"""UPDATE profiles
				SET {attr}=:int
				WHERE UserID=:uid""",
				{'int': updated_attributes, 'uid': userid}
			)
	


	def delete_attribute(self, userid: int, attribute: Literal['interests', 'clubs']) -> None:
		with data.connection:
			data.cur.execute(
				f"""UPDATE profiles
				SET {attribute}=:T
				WHERE UserID=:uid""",
				{'T': "", 'uid': userid}
			)





	def get_attribute(self, userid: int, attribute: Literal['interests', 'clubs', 'hours', 'credits']) -> Union[str, int]:
		profile = (
			data.cur.execute(
				f"""SELECT {attribute} 
				FROM profiles 
				WHERE UserID=:uid""",
				{'uid': userid}
			).fetchone()
		)

		assert profile, "Profile does not exist"

		return profile[0]
		




	def edit_number(self, userid: int, attri: Literal['hours', 'credits'], set_to: int, change: int = 0) -> None:
		"""set user's hour or credit count to a hard number,
		or
		modify hour or credits instead, work by, giving set_to the previous amount, and giving change
		the addition or subtraction
		design choice chosen over making a new function that changes only because it's not possible
		to add to the previous number record in 1 database call, so done in same place to save lines"""
		
		with data.connection:
			data.cur.execute(
				f"""
				UPDATE profiles
				SET {attri} = :att
				WHERE UserID = :u
				""",
				{'att': set_to + change, 'u': userid}
			)




	def check_missing_profile(self, command: Union[Callable, discord.ext.commands.core.Command]):
		"""decorator to check if user doesn't have a profile
		pointless to use if there are other exceptions required in the function, here for example,
		when we need to check for OverflowError"""

		async def inner(*args: Tuple[Union[str, int]]):
			try:
				await command(*args)
			except AssertionError:
				# args[0] is the command context
				await args[0].send('You don\'t have a profile, go make one first')
		return inner




ptools = Partnership()