import sqlite3 as sql
from typing import *
from discord.ext import commands#type:ignore
# from all_courses import get_data

bot = commands.Bot(command_prefix='$')


class Database:

	def __init__(self, file:str):
		self.file = file
		self.connection = sql.connect(file)
		self.cur = self.connection.cursor()

	def user_exists(self, user_id: int):

		# Searches for an existing user from the profiles table
		existing_user = list(
			self.cur.execute(
				"SELECT * FROM profiles WHERE UserID = (?)", 
				(user_id,)
			)
		)
		return True if existing_user else False

	async def create_profile(
		self, 
		user_id: int,
		user: str, 
		name: Optional[str] = '', 
		student_id: Optional[int] = 000000, 
		courses: Optional[Dict] = None):
	
	 
		existing_user = self.user_exists(user_id)

		# Creates a record in the table for the user's profile information, if no such record already exists. 
		if existing_user:
			if courses:
				await bot.loop.create_task(remove_classrooms(user_id, None))


		if not existing_user:  
			self.cur.execute(
				"INSERT INTO profiles VALUES (?, ?, ?, ?, 0, 'None', 0, 0, 'None' )",
				(user_id, user, name, student_id,)
			)
			self.connection.commit()
	
		if not courses:
			return
		
		# Creates a record for all of the user's courses for that school year
		for semester in (1, 2):
			total_courses = courses[semester]

			for course, teacher, week in total_courses:
				self.cur.execute(
					"INSERT INTO courses VALUES (?, ?, ?, ?, ?)",
					(user_id, course, teacher, week, semester,)
				)
		
		self.connection.commit()
		return

	def get_profile(self,
		table: Literal["profiles", "courses"],
		user: Union[str, int]) -> List[Tuple]:

		# Changes query and input depending on the type of table the user is searching for
		if table == 'profiles':
			query = """
			SELECT * FROM profiles 
			WHERE 
				UserID = (?) 
				or Username = (?) 
				or StudentID = (?)
				or Name =(?)
			LIMIT 1
			"""

			users = (user, user, user, user,)

		elif table == 'courses':
			query = "SELECT * FROM courses where UserID = (?)"
			users = (user,)

		# Retrieves the user's courses/profile
		return list(self.cur.execute(query, users))


	def delete_profile(self, user_id: int):

		self.cur.execute("DELETE FROM profiles WHERE UserID = (?)",(user_id,))

		bot.loop.create_task(remove_classrooms(user_id, None))

		self.connection.commit()

	def edit_profile(
		self, 
		category: Literal[
					'grade',
					'username',
					'interests',
					'clubs',
					'credits',
					'hours',
					'studentID',
					'name'
				],
		edit: Union[str,int],
		user_id: int):
		
		if category:
			
			
			fixed_categories = ['name','studentID','grade']

			if category in fixed_categories:
				
				
				#This index finds the specific category's location in our profiles table
				result = self.get_profile(
					'profiles',
					 user_id
					)[0][fixed_categories.index(category) + 2]

				if result:
					return

			query = f"""
				UPDATE profiles
				SET {category.capitalize()} = (?) 
				WHERE UserID = (?)
				"""

			self.cur.execute(query,(edit, user_id,))
			self.connection.commit()

	def create_table(self):
		# Creating table for testing
		self.cur.execute("""CREATE TABLE profiles(
			UserID integer,
			Username text,
			Name text,
			StudentID integer,
			Grade integer,
			Clubs text,
			Credits integer,
			Hours integer,
			Interests text
		)""")

		self.cur.execute("""CREATE TABLE courses(
			UserID integer,
			Course text,
			Teacher text,
			Week integer,
			Semester integer
		)""")
		
		self.connection.commit()








	def func(self):
		return 1

		
		


	def ok(self):
		self.edit_profile('interests', '', 392795163900248080)

	def asd(self):
		
		return self.cur.execute("SELECT * FROM profiles WHERE userID=:uid", {'uid': 392795163900248080}).fetchall()
		



data = Database('students.db')