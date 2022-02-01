import os

from typing import *
import os
import shutil

from udb import data

"""
SUBJECTS --------------- WILL BE TABLES
COMMAND: $note [subject] [source: link MAYBE implement file] [*args: desc]

MAYBE TRY: ADDING FEAture to prevent spam: cannot post more than 3 in x minutes
loop a bot task, check if it is summer break, if it is, delete all notes

Structure: 
| userID ( so they can remove ) | ?id so user can recognize what to delete | Subject | Optional Link | optional Description


"""

"""
$mynotes: see only users own notes

separate:
- $noteslink: post a link as note
- $notes: post a file as a note

$notes [subject] 2 see all for sub

$notes - see all notes
- loop through, look for type of note (file, link, text)
$notes [subject]
- loop through, look for type of note (file, link, text)

"""


StudentID = int



class Notes:
	def __init__(self) -> None:
		self.subjects = set(
			('english', 'math', 'physics', 'chemistry', 'biology', 
			'geography', 'history', 'civics', 'compe', 'cs', 'gym', 'arts', 'french',)
		)



		self.note_file_dir = "NotesFiles"
		self._curr_dir = os.getcwd()
		self.changeable_notes = ("subject", "note", "description")


	def make_file_dir(self):
		"""make a new directory used for moving all note files into it to reduce crowdiness"""

		path = os.path.join(self._curr_dir, self.note_file_dir)
		
		try:
			os.mkdir(path)

		except:
			print("This folder storage already exists")

	def del_file_dir(self):
		"""removes the directory used for moving file-type notes and all it's contents"""

		
		shutil.rmtree(fr"{self._curr_dir}\{self.note_file_dir}")

	def del_note_table(self):
		"""removes notes table - used for when year ends and notes can be cleared"""

		data.cur.execute("DROP TABLE notes")




	def get_note_type(self, noteid: int):
		return data.cur.execute("SELECT NoteType FROM notes WHERE NoteID=:nid",
			{'nid': noteid}).fetchone()[0]



	def get_note_id(self) -> Union[int, Literal[0]]:
		"""finds last accumulated note id, sends that, it will be increased by 1 to be practically
		used later
		if there isn't any data existing in the table, there's no id to exist either, this function
		would send 0 back, and once again, will be increased by 1 later to start the ids at 1 
		"""

		return data.cur.execute("SELECT MAX(NoteID) FROM notes").fetchone()[0] or 0



	def add_link_note(self, uid: StudentID, subj: str, link: str, desc: Tuple[str, ...]) -> None:
		"""gives user the option to add a link-based note"""

		note_id = self.get_note_id()

		# joins the tuple of words into a single string
		description_text = ' '.join(desc)

		# add a new note in the database with an id of 1 greater than the last accumulative integer id
		with data.connection:
			data.cur.execute("INSERT INTO notes VALUES (:u, :nid, :ntype, :sub, :link, :d)", 
				{'u': uid, 'nid': note_id + 1, 'ntype': 'link', 'sub': subj, 'link': link, 'd': description_text}
			)




	def add_file_note(self, uid: StudentID, nid: int, subj: str, file: str, desc: Tuple[str, ...]) -> None:
		"""user sends in files as a note, they will be downloaded and their location will be stored
		in the database for later lookup
		"""

		description_text = ' '.join(desc)

		# unlike the last time, `1` isn't added to the noteid, this is because we have already done
		# that earlier to improve readability at that point
		with data.connection:
			data.cur.execute("INSERT INTO notes VALUES (:u, :nid, :ntype, :sub, :tnotes, :des)",
				{'u': uid, 'nid': nid, 'ntype': 'file', 'sub': subj, 'tnotes': file, 'des': description_text}
			)




	def add_text_note(self, uid: int, subject: str, note: Tuple[str, ...]) -> None:
		"""add the note in text form"""

		noteid = self.get_note_id() + 1
		note_text = ' '.join(note)
		descrip = "N/A"

		with data.connection:
			data.cur.execute("""INSERT INTO notes VALUES (
				:user, :noid, :noty, :sub, :note, :des)""", {
					'user': uid, 
					'noid': noteid, 
					'noty': 'text', 
					'sub': subject, 
					'note': note_text, 
					'des': descrip
				})



	def remove_note(self, note_id: int) -> None:
		"""self explanatory tho
		function also removes the file related to the deleted note, IF the note is a file
		this is so that the file folder/area doesn't crowd the directory
		"""

		note_type, note = data.cur.execute(
			"SELECT NoteType, Note FROM notes WHERE NoteID=:nid", {'nid': note_id}
		).fetchone()
			
		if note_type == 'file':
			"""and the one for cleaner storage"""
			os.remove(fr"{self._curr_dir}/{self.note_file_dir}/{note}")

			# os.remove(note)
		

		with data.connection:
			data.cur.execute("DELETE from notes WHERE NoteID=:nid", {'nid': note_id})


	

	def get_file_name(self, noteid: str) -> str:
		"""used to get notes in file form"""
		


		note = data.cur.execute("SELECT Note FROM notes WHERE NoteID=:nid", {'nid': noteid}).fetchone()

		assert note, "NoteID does not exist"


		return note[0]




	def update_note(self, noteid: int, updating: Literal["subject", "note", "description"], update_to: Tuple[str, ...]) -> None:
		"""discord command that lets users update one of their notes
		they may not update their userid, noteid, notetype
		"""

		updated: str = ' '.join(update_to)

		with data.connection:
			data.cur.execute(f"""UPDATE notes SET {updating} = :upt
								WHERE NoteID = :nid""",
								{'upt': updated, 'nid': noteid})




	def get_all_notes(self, subject: Optional[str] = None) -> List[Tuple[str]]:
		"""get all the notes
		filter out a single subject if chosen to
		"""

		if subject:
			return data.cur.execute("""SELECT NoteID, NoteType, Subject, Note, Description
									FROM notes
									WHERE Subject=:sub""",
									{'sub': subject}).fetchall()

		return data.cur.execute("""SELECT NoteID, NoteType, Subject, Note, Description
								FROM notes""").fetchall()



	def front_end_info(
			self, 
			low_bound: int, 
			post_bound_grab: int, 
			subject: Optional[str] = None
		) -> List[Tuple[str]]:

		"""send the important info needed to make the front end
		includes everything in the table except for, UserID
		"""

		# boolean to check if low_bound specifically isn't None to allow 0 to be valid

		if low_bound == 0 and post_bound_grab and not subject:
			return data.cur.execute(f"""SELECT NoteID, NoteType, Subject, Note, Description
								FROM notes
								limit {post_bound_grab}""").fetchall()

		if low_bound and post_bound_grab and not subject:
			return data.cur.execute(f"""SELECT NoteID, NoteType, Subject, Note, Description
								FROM notes
								limit {low_bound}, {post_bound_grab}""").fetchall()

		if low_bound == 0 and post_bound_grab and subject:
			return data.cur.execute(f"""SELECT NoteID, NoteType, Subject, Note, Description
								FROM notes
								WHERE Subject=:sub
								limit {post_bound_grab}""",
								{'sub': subject}).fetchall()

		return data.cur.execute(f"""SELECT NoteID, NoteType, Subject, Note, Description
								FROM notes
								WHERE Subject=:sub
								limit {low_bound}, {post_bound_grab}""",
								{'sub': subject}).fetchall()


		

	def get_person_notes(self, userid: StudentID) -> List[Tuple[str]]:
		return data.cur.execute("""SELECT NoteID, NoteType, Subject, Note, Description 
								FROM notes WHERE UserID=:uid""", 
								{'uid': userid}).fetchall()



nools = Notes()