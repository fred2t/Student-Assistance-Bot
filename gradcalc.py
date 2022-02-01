from typing import *

from udb import data

"""
!gradprogress
This command will track your graduation progress, let you know how close you are to your high 
school diploma, giving you a %. It will also notify you on what you're falling behind on whether 
that is community hours or a few credits you are missing.
"""

StudentID = int
Credits = int
Hours = int
Literacy = Union[int, Literal[0, 1]]


class Graduation:
	def __init__(self) -> None:
		self.images: List[str] = ["https://anopensuitcase.com/wp-content/uploads/2016/11/maui.jpg.webp", 
			"https://memegenerator.net/img/instances/65144233/youre-welcome.jpg", 
			"https://image.shutterstock.com/image-vector/youre-welcome-text-lettering-sign-600w-1707907489.jpg",
			"https://i2.wp.com/yukaichou.com/wp-content/uploads/2014/05/Image-of-a-person-handing-a-book-through-a-laptop-screen.jpg?w=500&ssl=1"
		]
	
		self._credits_req = 30
		self._hours_req = 40
		self._test_req = 1

		self._credits_value = 48.46
		self._hours_value = 31.45
		self._test_value = 20.09


	def _get_graduation_info(self, pers_id: StudentID):
		"""gets the user's graduation requirements' information to use"""
		
		return list(data.cur.execute("""
				SELECT 
				Credits, Hours
				FROM profiles WHERE UserID = (?)
				""",
				(pers_id,)
			)
		)

	def graduation_percentage(self, pers_id: StudentID, test_status):
		
		pers_info = self._get_graduation_info(pers_id)
		assert pers_info, "User doesn't have an existing profile"

		# not done above to prevent index error before assertion
		pers_info = pers_info[0]

		# re assigned because the assertion would be caught even though someone has a profile if they
		# had 0 credits and hours
		credits, hours = pers_info

		# # percentage of points rewarded
		cred_point = min(credits / self._credits_req, 1)
		hour_point = min(hours / self._hours_req, 1)
		test_point = min(test_status / self._test_req, 1)

		return round(sum(
			user * requirement 
			for user, requirement in zip(
				(self._credits_value, self._hours_value, self._test_value),
				(cred_point, hour_point, test_point)
			)), 5
		)





gtools = Graduation()