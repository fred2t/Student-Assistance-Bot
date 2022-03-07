from discord.ext import commands, tasks
from discord_buttons_plugin import *
from typing import *
import discord
import os

from scholarship import Scholarship
from gradcalc import gtools
from aquaint import ptools
from notes import nools
from udb import data

# server used to dm person who called aquaint function
SERVER = 853023353525764117
PARTNER_PROGRAM_PARTICIPANTS = "partner program participants.txt"

bot = commands.Bot(command_prefix='$')
buttons = ButtonsClient(bot)

@bot.event
async def on_ready():
		print(f"{bot.user} online")



# Created outside the function(s) because the order of scholarships changes with each call,
## I believe this is because the part being scraped on the main website is an animation where the 
## text moves around
MAIN_SCHOLARSHIP_OBJECT = Scholarship()
SCHOLARSHIP_CONST = MAIN_SCHOLARSHIP_OBJECT.scholarship_names

@buttons.click
async def scholarship_info(ctx):
    await buttons.send(
        content="Learn more about scholarships", channel = ctx.channel.id, components = [
			ActionRow([
                Button(
					style = ButtonType().Link,
					label = "Canada finance services",
                    url="https://www.canada.ca/en/services/finance/educationfunding/scholarships.html",
                    emoji = {"name": "mage",
                             "id": "625891304081063986"
                        }
				),

				Button(
					style = ButtonType().Link,
					label = "Educanada Scholarships from Canada",
					url = "https://www.educanada.ca/scholarships-bourses/can/institutions/study-in-canada-sep-etudes-au-canada-pct.aspx?lang=eng",
                    emoji = {"name": "some",
                    "id": "891837218468003871"}
				),

                Button(
					style = ButtonType().Link,
					label = "Educanada International Scholarships",
					url = "https://www.educanada.ca/scholarships-bourses/non_can/index.aspx?lang=eng",
                    emoji = {"name": "some",
                    "id": "891837218468003871"}
				),
                
                Button(
					style = ButtonType().Link,
					label = "Universitystudy Plan",
					url = "https://www.universitystudy.ca/plan-for-university/scholarships-grants-and-bursaries-for-canadian-students/",
                    emoji = {"name": "some",
                    "id": "891837218468003871"}
				),
			])
		]
	)

@buttons.click
async def other_scholarship_sources(ctx):
    await buttons.send(
        content="Find more scholarships", channel = ctx.channel.id, components = [
			ActionRow([
                Button(
					style = ButtonType().Link,
					label = "Studentawards",
                    url="https://studentawards.com/",
                    emoji = {"name": "mage",
                             "id": "625891304081063986"
                        }
				),

				Button(
					style = ButtonType().Link,
					label = "Scholarshipportal Scholarships Canada",
					url = "https://www.scholarshipportal.com/scholarships/canada",
                    emoji = {"name": "some",
                    "id": "891837218468003871"}
				),

                Button(
					style = ButtonType().Link,
					label = "Univcan Programs and Scholarships",
					url = "https://www.univcan.ca/programs-and-scholarships/",
                    emoji = {"name": "some",
                    "id": "891837218468003871"}
				),
			])
		]
	)

@bot.command()
async def scholarship(ctx, scholarship_pick: int = 0):
    """get info about scholarship options, or pick a specific one to get more info about"""

    # if there wasn't a scholarship number given, assume user doesn't know them and send a list of all of them
    if not scholarship_pick:
        scholarship_message = '__The Scholarship Summit__'

        for point, scholarship_title in enumerate(SCHOLARSHIP_CONST):
            # docstring instead of looping 'message send' to decrease computation
            scholarship_message += f"""
            **{point + 1} | {scholarship_title}**"""
        
        await ctx.send(scholarship_message)
        await ctx.send("For more info on one, type scholarship [number]!") # return? removed

        return await buttons.send(
            content="What are scholarships? Show me more!? Click the buttons!", channel = ctx.channel.id, components = [
                ActionRow([
                    Button(
                        style = ButtonType().Primary,
                        label = "Info about Scholarships",
                        custom_id = "scholarship_info",
                        emoji = {"name": "mage",
                                "id": "625891304081063986"
                            }
                    ),

                    Button(
                        style = ButtonType().Success,
                        label = "Other Scholarship Sources",
                        custom_id = "other_scholarship_sources",
                        emoji = {"name": "some",
                        "id": "891837218468003871"}
                    )
                ])
            ]
        )
        
        

    # send error to discord if user gives a number not corresponding to a scholarship
    if scholarship_pick not in range(1, 16):
        return await ctx.send('```That number isn\'t on the list```')

    # if scholarship number otherwise given, send the three important pictures
    for picture_num in MAIN_SCHOLARSHIP_OBJECT.get_site_info(MAIN_SCHOLARSHIP_OBJECT.scholarship_links[scholarship_pick - 1]):
        await ctx.send(file=discord.File(f"scholp{picture_num + 1}.png"))
    # also send a place where caller can find more info
    await ctx.send(f"For more info, head to `{MAIN_SCHOLARSHIP_OBJECT.scholarship_links[picture_num - 1]}` !")
    
# rename to multship
@bot.command()
async def multship(ctx, first_filter: int = 0, sec_filter: int = 0):
    """sends all scholarships in the range of the two arguments inclusive, or from zero to the first 
    argument if the second one isn't given, this is to save the user time from finding each 
    scholarship one by one for all fifteen"""

    # if no filters given, this function shouldn't've been called, send error
    if not first_filter and not sec_filter:
        return await ctx.send("You need to add filters in this version of the scholarship function")

    # if any of the two filters not between 0 and 15, request makes no sense and error is sent
    if first_filter not in range(1, 16):
        return await ctx.send("```That does not exist```")

    # if only one filter given, assume user wants all scholarships from zero to the given filter
    if first_filter and not sec_filter:
        for scholarship in range(first_filter):
            for picture_numb in MAIN_SCHOLARSHIP_OBJECT.get_site_info(MAIN_SCHOLARSHIP_OBJECT.scholarship_links[scholarship]):
                await ctx.send(file=discord.File(f"{picture_numb + 1}.png"))
            await ctx.send(f"For more info, head to `{MAIN_SCHOLARSHIP_OBJECT.scholarship_links[scholarship]}` !")
        return
        

    
    # if both filters given, send all the scholarships in the range of what they inputted, inclusivce
    # they will all be sent at once, however they will still be easily recognizable because the
    # first picture_num is a title with a different colour from all the other white pictures
    for scholarship in range(first_filter - 1, sec_filter):
        if (first_filter or sec_filter) not in range(1, 16):
            return await ctx.send('```That number does not relate to a scholarship on the list```')

        for picture_num in MAIN_SCHOLARSHIP_OBJECT.get_site_info(MAIN_SCHOLARSHIP_OBJECT.scholarship_links[scholarship]):
            await ctx.send(file=discord.File(f"scholp{picture_num + 1}.png"))
        await ctx.send(f"To learn more, go to `{MAIN_SCHOLARSHIP_OBJECT.scholarship_links[scholarship]}` !")



"""btw test if main =name later"""
# school gps feature still in working progress
from mapanim import * # change import later
@bot.command()
async def map(ctx):
    if not os.path.exists('xdhmmname.gif'):
        await ctx.send(file=discord.File('route2.gif'))

        return os.remove('route2.gif')

    await ctx.send(file=discord.File("xdhmmname.gif"))

    for file in ['route2.gif', 'xdhmmname.gif']:
        os.remove(file)


@bot.command()
async def gradprogress(ctx):
	try:
		pers_id = ctx.message.author.id

		embed = discord.Embed(
			title='\\\\/ Graduation Progressifier calculates :face_with_monocle:',
			colour=discord.Colour.orange()
		)

		embed.add_field(name="If you've finished OSSLT (g10 literacy test)", value=f"You are {gtools.graduation_percentage(pers_id, 1)}% towards graduation :scream: !")
		embed.add_field(name="If you'ven't finished OSSLT (g10 literacy test)", value=f"You are {gtools.graduation_percentage(pers_id, 0)}% towards graduation :ok_hand: !")

		import random
		embed.set_image(url=random.choice(gtools.images))

		await ctx.send(embed=embed)
	
	except AssertionError:
		await ctx.send("LOL! You don't have a profile so I have no information in my records to judge! Go make one with the `create_profile` command bruh :thumbsup:")






"""NOTES"""
# add a link note, 
@bot.command()
async def notel(ctx, subject: str = None, link: str = None, *description: str) -> discord.message.Message:
	"""gives user the option to add a link-based note
	every argument is optional because that way, we will force an argument to be inputted, so no matter
	what, the user on the discord side will be able to see a customized error to know what went wrong
	"""

	# check if user types in a random word as a subject
	if subject not in nools.subjects:
		return await ctx.send(f":confused: I've never heard of a subject called `{subject}`!? :confused:")



	# do a sad attempt at an argument filter - checks if an argument hasn't been added
	# if it hasn't, that note has value too low to add to the database
	if not subject or not link:
		return await ctx.send("You're not giving enough information :confused:; use `$[command] [subject] [link] [*Optional Description*]`")

	

	if not description:
		description = ("N/A", )

	# real stuff
	uid = ctx.message.author.id

	nools.add_link_note(uid, subject, link, description) 
	return await ctx.send("CONGRATS! Your note has been added! :smiley:")

@bot.command()
async def delnote(ctx, note_id: int) -> discord.message.Message:
	try:
		user = ctx.message.author.id

		"""
		(392795163900248080, 1, 'math', 'https://www.hackerrank.com/challenges/collections-counter/problem', 'hello this is description')
		"""
		# print(data.cur.execute("SELECT * FROM notes WHERE NoteID=:nid", {'nid': note_id}).fetchone())
		# print(data.cur.execute("SELECT * FROM notes WHERE NoteID=:nid", {'nid': note_id}).fetchone()[0])

		if user == data.cur.execute("SELECT * FROM notes WHERE NoteID=:nid", {'nid': note_id}).fetchone()[0]:
			nools.remove_note(note_id)
			await ctx.send("Your note has been removed!")
		
		else:
			await ctx.send("You can't delete another person's notes! Sorry.")
	except:
		await ctx.send("Note does not exist")
		
# add text - based note
@bot.command()
async def notet(ctx, subject: str = None, *text: str) -> discord.message.Message:
	if not subject:
		return await ctx.send("Bruh what is this non-existent subject")

	if subject not in nools.subjects:
		return await ctx.send(f"Wtf is that subject? You're the only one I know that's learning {subject} :expressionless:")

	if not text:
		return await ctx.send("UHHHH, send in your note...?")


	

	uid = ctx.message.author.id
	nools.add_text_note(uid, subject, text)

	return await ctx.send("Your note has been saved! :pinched_fingers:")

#seesubjects
@bot.command()
async def seesub(ctx) -> discord.message.Message:
	await ctx.send('\n'.join(nools.subjects))

# notefile
@bot.command()
async def notef(ctx, subj: str = None, *descript: str) -> discord.message.Message:

	if not subj:
		return await ctx.send("At least type in a subject name first :confused:")
	
	if subj not in nools.subjects:
		return await ctx.send(f"Wow! what is that! I've never heard of the subject, {subj} :joy:")


	

	last_id = nools.get_note_id()
	stu_id = ctx.message.author.id


	for noid, attachment in enumerate(ctx.message.attachments, last_id + 1):
		file_dot = attachment.filename[::-1].index('.')

		# """making the option to save in a different folder to reduce crowdedness in this folder"""
		await attachment.save(f"{nools._curr_dir}/{nools.note_file_dir}/nofi{attachment.filename[-file_dot - 1:]}")

		file = f"nofi{noid}{attachment.filename[-file_dot - 1 :]}"
		# await attachment.save(file)



		if not descript:
			descript = ("N/A", )

		nools.add_file_note(stu_id, noid, subj, file, descript)

	await ctx.send("Your note file has been saved :sunglasses:")

# notes [noteid] - mainly to be used to get files - actually probably will be the only use
# the command to get the files will be a variadic, but if statements each time
@bot.command()
async def getnote(ctx, *noteid: str) -> discord.message.Message:
	try:
		if not noteid:
			return await ctx.send("UHH?? You gotta send the file's number id that you want to see")

		for id in noteid:
			file: str = nools.get_file_name(id)
			await ctx.send(file=discord.File(f"{nools._curr_dir}/{nools.note_file_dir}/{file}"))

	except AssertionError:
		await ctx.send("That Note ID does not exist, try rereading :stuck_out_tongue_closed_eyes:")

	except:
		await ctx.send(f"I mean, this isn't a file, there doesn't seem like a real reason to not use the bot message, but ok, :love_you_gesture:\n```{file}```")

# let people update their notes
@bot.command()
async def updatenote(ctx, noteid: int = None, updating: Union[str, Literal["subject", "note", "description"], None] = None, *update_to: str) -> discord.message.Message:
	if (not noteid) or (not updating):
		# print(noteid, updating)
		# print(not noteid, not updating)
		return await ctx.send("You're not giving enough info on a note :unamused:")


	note_type = nools.get_note_type(noteid)
	if note_type == 'file':
		return await ctx.send("You can't change a file. You can delete the file and add a note with that file however, that is, if you'd like to.")
	
	
	user = ctx.message.author.id

	if not (user == data.cur.execute("SELECT UserID FROM notes WHERE NoteID=:nid",
									{'nid': noteid}).fetchone()[0]):
		
		return await ctx.send("LOL! You can't edit a not that you haven't made")

	# else:
	if (upda := updating.lower()) not in nools.changeable_notes:
		return await ctx.send(f"WTF?? What is that word called {upda}?? loool")



	if not update_to:
		return await ctx.send("Umm?? Make your edit")



	if (updating == "subject") and (sub := update_to[0].lower()) not in nools.subjects:
		
		# await ctx.send(f"What? What is that subject called {update_to}")
		return await ctx.send(f"What? What is that subject called `{sub}` :smile:")


	nools.update_note(noteid, updating, update_to)

	await ctx.send("CONgrats! Your note has been updated")



"""THIS WILL BE MAIN FRONT END COMMAND TO VIEW NOTES"""

@bot.command()
async def s2d_text(
		embed: discord.embeds.Embed, 
		noteid: int, 
		subject: str, 
		note: str, 
		description: str
	) -> discord.embeds.Embed:
	
	return embed.add_field(name=f"Note ID: {noteid}, Note type: Text, Subject: {subject}", value=f"Note: {note}", inline=False)

@bot.command()
async def s2d_link(
		embed: discord.embeds.Embed, 
		noteid: int, 
		subject: str, 
		note: str, 
		description: str
	) -> discord.embeds.Embed:
	
	return embed.add_field(name=f"Note ID: {noteid}, Note type: Text, Subject: {subject}\nNote: {note}", value=f"Description: {description}", inline=False)

@bot.command()
async def s2d_file(
		embed: discord.embeds.Embed, 
		noteid: int, 
		subject: str, 
		note: str,
		description: str
	) -> discord.embeds.Embed:
	
	note_message = "The note is stored in file format in my database.\nTo access it use `[bot prefix]getnote [note_id]`"

	return embed.add_field(name=f"Note ID: {noteid}, Note type: Text, Subject: {subject}\nNote: {note_message}", value=f"Description: {description}", inline=False)

DB_NOTE_TYPE_IDENTIFIER: Dict[Literal["text", "link", "file"], discord.ext.commands.core.Command] = {
	"text": s2d_text, 
	"link": s2d_link, 
	"file": s2d_file
}

# SHOW ABSOLUTELY EVERYTHING
@bot.command()
async def allnotes(ctx: discord.ext.commands.context.Context):
	# field text limit is 1024
	# field count limit is 30
	# embed size - (max text space) max is 6000

	"""
	NoteID, NoteType, Subject, Note, Description
	"""

	embed = discord.Embed(
		title='Greetings',
		colour=discord.Colour.orange()
	)

	all_notes_info = nools.get_all_notes()

	for note_info in all_notes_info:
		noteid, notetype, subject, note, description = note_info

		await DB_NOTE_TYPE_IDENTIFIER[notetype](embed, noteid, subject, note, description)

		# embed.add_field(name=f"Note ID: {noteid}, Note type: {notetype}, Subject: {subject}\nNote: {note}", value=f"Description: {description}", inline=False)

	embed.set_image(url="https://cdn.shopify.com/s/files/1/0583/7221/files/SOFTCOVER-thickness.jpg?v=1503354723")
	
	
	await ctx.send(embed=embed)

# untested ~ note sure if it will mess up and delete
one_month = 30.4167 * 24
@tasks.loop(hours=one_month)
async def remove_notes_end_year() -> None:
	"""if it's summer break, delete all notes and their files in their respective locations"""

	print("this was sent from the tasks.loop")
	

	now = date.today()
	month = now.month

	jul, oct = 6, 10
	
	


	return
	return
	if jul < month < oct:
		nools.del_note_table()
		data.make_note_table()
		
		
		nools.del_file_dir()
		nools.make_file_dir()
# remove_notes_end_year.start() # optional to start

@buttons.click
async def go_forward(ctx) -> None:
	global start
	total_no_notes: int = len(list(data.cur.execute("SELECT NoteID FROM notes")))
	no_note_pages = total_no_notes // 10 + 1

	start += 1
	if start == no_note_pages:
		return await ctx.reply("You're on the last page :/")


	notes_info = nools.front_end_info(start * 10, 10)

	embed = discord.Embed(
		title='Greetings',
		colour=discord.Colour.orange()
	)

	# create the new embed with new notes
	for note in notes_info:
		noteid, notetype, subject, note, description = note

		await DB_NOTE_TYPE_IDENTIFIER[notetype](embed, noteid, subject, note, description)
	
	# for note in range(start * 10, (start + 1) * 10):
	# 	embed.add_field(name=f'some{note}', value='lol', inline=False)
	embed.set_image(url="https://cdn.shopify.com/s/files/1/0583/7221/files/SOFTCOVER-thickness.jpg?v=1503354723")
	embed.set_footer(text=f"Page {start + 1} of {no_note_pages}")
	return await wtf.edit(embed=embed)
	
@buttons.click
async def go_backwards(ctx):
	# globaled first because compiler doesn't allow it to be used before being globaled 
	global start
	if start == 0:
		return await ctx.reply("You're at the first page already :confused:")

	# print(start)
	start -= 1
	# print(start)

	notes_info = nools.front_end_info(start * 10, 10)
	# print(len(notes_info))

	embed = discord.Embed(
		title='Greetings',
		colour=discord.Colour.orange()
	)

	for note in notes_info:
		noteid, notetype, subject, note, description = note

		await DB_NOTE_TYPE_IDENTIFIER[notetype](embed, noteid, subject, note, description)
	
	embed.set_image(url="https://cdn.shopify.com/s/files/1/0583/7221/files/SOFTCOVER-thickness.jpg?v=1503354723")
	await wtf.edit(embed=embed)

@bot.command()
async def notes(ctx, subject_filter: Optional[str] = None):
	if subject_filter and subject_filter not in nools.subjects:
		return await ctx.send(f"Never heard of that subject `{subject_filter}`")


	if subject_filter:
		embed = discord.Embed(
			title='Greetings',
			colour=discord.Colour.orange()
		)

		all_notes_info = nools.get_all_notes(subject_filter)

		for note_info in all_notes_info:
			noteid, notetype, subject, note, description = note_info

			await DB_NOTE_TYPE_IDENTIFIER[notetype](embed, noteid, subject, note, description)

			# embed.add_field(name=f"Note ID: {noteid}, Note type: {notetype}, Subject: {subject}\nNote: {note}", value=f"Description: {description}", inline=False)

		embed.set_image(url="https://cdn.shopify.com/s/files/1/0583/7221/files/SOFTCOVER-thickness.jpg?v=1503354723")
		
		return await ctx.send(embed=embed)

	embed = discord.Embed(
		title='Greetings',
		colour=discord.Colour.orange()
	)

	# if the command is called again, it will reset the page
	global start
	start = 0

	# each embed page will have 10 items max
	notes_info = nools.front_end_info(0, 10)
	# print(notes_info)

	# for note_info in notes_info:
	# 	noteid, notetype, subject, note, description = note_info

	# 	await DB_NOTE_TYPE_IDENTIFIER[notetype](embed, noteid, subject, note, description)


	# embed.set_image(url="https://cdn.shopify.com/s/files/1/0583/7221/files/SOFTCOVER-thickness.jpg?v=1503354723")
	# await ctx.send(embed=embed)

	for notes_info in notes_info:
		noteid, notetype, subject, note, description = notes_info

		await DB_NOTE_TYPE_IDENTIFIER[notetype](embed, noteid, subject, note, description)
		# embed.add_field(name=f'some{note}', value='lol', inline=False)


	embed.set_image(url="https://cdn.shopify.com/s/files/1/0583/7221/files/SOFTCOVER-thickness.jpg?v=1503354723")
	embed.set_footer(text="Page 1 of [add here later]")

	# global so we can access it inside the button command
	global wtf
	wtf = await ctx.send(embed=embed)
	return await buttons.send(
		content = '**To view a specific note use:** `[prefix]getnote [note_id]`', channel = ctx.channel.id, components = [
			ActionRow([
				Button(
					style = ButtonType().Primary,
					label = "<---------------------",
					custom_id = "go_backwards",
				),

				Button(
					style = ButtonType().Primary,
					label = "---------------------->",
					custom_id = "go_forward"
				),
			])
		]
	)

#mynotes
@bot.command()
async def mynotes(ctx):
	user = ctx.message.author.id

	embed = discord.Embed(
		title='Greetings',
		colour=discord.Colour.orange()
	)

	all_notes_info = nools.get_person_notes(user)

	for note_info in all_notes_info:
		noteid, notetype, subject, note, description = note_info

		await DB_NOTE_TYPE_IDENTIFIER[notetype](embed, noteid, subject, note, description)

		# embed.add_field(name=f"Note ID: {noteid}, Note type: {notetype}, Subject: {subject}\nNote: {note}", value=f"Description: {description}", inline=False)

	embed.set_image(url="https://cdn.shopify.com/s/files/1/0583/7221/files/SOFTCOVER-thickness.jpg?v=1503354723")
	
	
	await ctx.send(embed=embed)






"""
these  4 functions will work with inputted information for INTERESTS and CLUBS to show, add, 
remove, or delete all of any given attributes in command call

They go together because both items in the database are of the same format
"""
@ptools.check_missing_profile
@bot.command()
async def show_attributes(ctx, attri: Union[str, Literal['interests', 'clubs']]) -> discord.message.Message:
	user_attrs = ptools.get_attribute(ctx.message.author.id, attri)

	if not user_attrs:
		return await ctx.send(f"What are you doing? Your {attri} list is empty")
	

	visual = discord.Embed(
		title=f'Your {attri}',
		colour=discord.Colour.orange()
	)

	user_attrs = user_attrs.split(", ")
	for attribute in user_attrs:
		visual.add_field(name='-' * 30, value=attribute, inline=False)

	await ctx.send(embed=visual)

@ptools.check_missing_profile
@bot.command()
async def add_attributes(ctx, attri: Literal['interests', 'clubs'], *interest: str) -> discord.message.Message:
	"""adds interest to profile, splitting each new added interest with a comma"""


	if not interest:
		return await ctx.send(f"You gotta state an {attri} to add -.-; use $`addinterest [your_{attri[: -1]}] [your_{attri[: -1]}] ... [your_{attri[: -1]}]`")
	
	
	user_id = ctx.message.author.id
	previous_attributes = ptools.get_attribute(user_id, attri)

	# remove duplicates easily with set
	pre_attrs_list = previous_attributes.split(', ')
	added_attributes = ', '.join(
		attr 
		for attr in set(interest) 
		if attr not in pre_attrs_list
	) 
	if not added_attributes:
		return await ctx.send('That\'s already in your list wtf')

	

	# if user had an empty interest list previously, we can't start with a comma (, int_1, int_2 (??))
	if not previous_attributes:
		ptools.add_attribute(user_id, attri, previous_attributes, added_attributes)
		return await ctx.send(f"Your new {attri} list is: {ptools.get_attribute(user_id, attri)}")

	# otherwise, we can safely split each new interest added with commas
	# comma prefix added to string to add
	to_add = ', ' + added_attributes
	ptools.add_attribute(user_id, attri, previous_attributes, to_add)
	await ctx.send(f"Your previous {attri} list: {previous_attributes}")
	await ctx.send(f"Your new {attri} list is: {previous_attributes + to_add}")

@bot.command()
async def remove_attributes(ctx, attri: Literal['interests', 'clubs'], *delete_requests: str) -> discord.message.Message:
	try: 
		if not delete_requests:
			return await ctx.send(f"Well you gotta delete something. Use `del{attri} [your_{attri[: -1]}] [your_{attri[: -1]}] ... [your_{attri[: -1]}]`")

		userid = ctx.message.author.id
		prev_attributes = ptools.get_attribute(userid, attri)

		if not prev_attributes:
			return await ctx.send(f"What you doing? Your {attri} list is already empty")



		# easily guard against users typing multiple of the same interests in one message while also
		# making it easily indexable (since tuples cannot use `remove`)
		delete_requests = list(set(delete_requests))
		for attribute in delete_requests:
			if attribute not in prev_attributes.split(', '):
				return await ctx.send(f"Error: `{attribute}` is not in your `{attri}` list")


		await ctx.send(f"Your previous {attri} list: ```{prev_attributes}```")

		ptools.remove_attribute(userid, attri, prev_attributes, delete_requests)
		
		
		
		updated_attributes = ptools.get_attribute(userid, attri)
		
		# check if the list is empty after the removals
		if not updated_attributes:
			return await ctx.send("```Wow! You have an empty list now! Clean!```")

		await ctx.send(f"Your new {attri} list is: ```{updated_attributes}```")


	except AssertionError:
		await ctx.send("You don't have a profile, go make one first")

	except:
		await ctx.send("Unable to read your requested removals") 

@bot.command()
async def DELETEALLMYATTRIBUTES(ctx, attri: Literal['interests', 'clubs']) -> discord.message.Message:
	ptools.delete_attribute(ctx.message.author.id, attri)

	await ctx.send(f"Your {attri} list has been deleted")

"""
decorators for exceptions if profile doesn't exist (ONLY for assertion errors (no profiles))
"""

# interests
@bot.command()
async def myinterests(ctx) -> discord.message.Message:
	await show_attributes(ctx, 'interests')

@bot.command()
async def addinterests(ctx, *interests_to_add: str) -> discord.message.Message:
	await add_attributes(ctx, 'interests', *interests_to_add)

@bot.command()
async def removeinterests(ctx, *requested_removals: str) -> discord.message.Message:
	await remove_attributes(ctx, 'interests', *requested_removals)

@bot.command()
async def DELETEALLMYINTERESTS(ctx) -> discord.message.Message:
	await DELETEALLMYATTRIBUTES(ctx, 'interests')


"""clubs"""
@bot.command()
async def myclubs(ctx) -> discord.message.Message:
	await show_attributes(ctx, 'clubs')

@bot.command()
async def addclubs(ctx, *clubs_to_add) -> discord.message.Message:
	await add_attributes(ctx, 'clubs', *clubs_to_add)

@bot.command()
async def removeclubs(ctx, *requested_removals) -> discord.message.Message:
	await remove_attributes(ctx, 'clubs', *requested_removals)

@bot.command()
async def DELETEALLMYCLUBS(ctx) -> discord.message.Message:
	await DELETEALLMYATTRIBUTES(ctx, 'clubs')





"""same as last 4 functions, works for both hours & credits as they are both of INTEGER form"""
@ptools.check_missing_profile
@bot.command()
async def my_numbers(ctx, attri: Literal['hours', 'credits']) -> discord.message.Message:
	number = ptools.get_attribute(ctx.message.author.id, attri)

	visual = discord.Embed(
		title=f'Your Recorded {attri.capitalize()} Count',
		description=f"You have {number} {attri}! :scream:",
		colour=discord.Colour.orange()
	)

	await ctx.send(embed=visual)


@bot.command()
async def edit_number(ctx, attri: Literal['hours', 'credits'], set_to: int) -> discord.message.Message:
	# no need for try...except to check if person has profile because `mynumbers' catches it with 
	# it's own try..except
	try:
		if set_to <= 0:
			return await ctx.send(f"Bruh, negative {attri}?")
			
		ptools.edit_number(ctx.message.author.id, attri, set_to)
		await my_numbers(ctx, attri)


	except OverflowError:
		await ctx.send("That number makes no sense??")


@bot.command()
async def add_number(ctx, attri: Literal['hours', 'credits'], change: int) -> discord.message.Message:
	try:
		prev_num = ptools.get_attribute(ctx.message.author.id, attri)
		
		ptools.edit_number(ctx.message.author.id, attri, prev_num, change)
		await my_numbers(ctx, attri)
		
	except AssertionError: 
		await ctx.send("You don't have a profile, go make one first")

	except OverflowError:
		await ctx.send("That number makes no sense??")

@ptools.check_missing_profile
@bot.command()
async def remove_number(ctx, attri: Literal['hours', 'credits'], change) -> discord.message.Message:
	# no need to check foR overflow error because
	# the number will already be checked if it goes below 0 in the edit_number function, before it 
	# can happen
	
	prev_num = ptools.get_attribute(ctx.message.author.id, attri)
	
	if prev_num - change < 0:
		return await ctx.send(f"How the negative {attri} lol?")

	ptools.edit_number(ctx.message.author.id, attri, prev_num, -change)
	await my_numbers(ctx, attri)
		

# hours
@bot.command()
async def myhours(ctx) -> None:
	await my_numbers(ctx, 'hours')

@bot.command()
async def sethours(ctx, change2x: int) -> discord.message.Message:
	await edit_number(ctx, 'hours', change2x)

@bot.command()
async def addhours(ctx, increase: int) -> discord.message.Message:
	await add_number(ctx, 'hours', increase)
	
@bot.command()
async def removehours(ctx, decrease: int) -> discord.message.Message:
	await remove_number(ctx, 'hours', decrease)


# credits
@bot.command()
async def mycredits(ctx) -> None:
	await my_numbers(ctx, 'credits')

@bot.command()
async def setcredits(ctx, change2x: int):
	await edit_number(ctx, 'credits', change2x)
	
@bot.command()
async def addcredits(ctx, adder: int) -> discord.message.Message:
	await add_number(ctx, 'credits', adder)
	
@bot.command()
async def removecredits(ctx, decrease: int) -> discord.message.Message:
	await remove_number(ctx, 'credits', decrease)



# matches people based off interests: rename later: maybe $match or $acquaint (less intimate name,
# people might be more comfortable with that)\
@bot.command()
async def aquaint(ctx):
	"""matches people with each other based on factors such as hours, grade, interests, and clubs,
	then notifies both users through discord direct message"""

	try:
		MemberID = AffinityPoints = int
		# print(dir(ctx))
		# print(ctx.author_id)

		user_id = ctx.author.id
		

		all_user_affinities: Dict[MemberID, AffinityPoints] = {}
		
		guild = bot.get_guild(SERVER)
		command_caller = await guild.fetch_member(user_id)
		await command_caller.create_dm()
		
		# for debugging
		# with open(PARTNER_PROGRAM_PARTICIPANTS, 'r', encoding='cp1252') as f:
		# 	partnerable_users_including_self = f.read().split()
		# 	await ctx.send(f"Possible partnerable-pairs including self: {partnerable_users_including_self}")
		
		
		
		with open(PARTNER_PROGRAM_PARTICIPANTS, 'r', encoding='cp1252') as f:
			partnerable_users: List[MemberID] = f.read().split()

		# check if dictionary is empty
		if not partnerable_users:
			await command_caller.dm_channel.send("Hello :wave:! You are the first participant of this partnership command. There is no one to match with at the moment. You will be added to the list as the first participant :one:! We will notify you right away when a match is found!")
			return ptools.add_participant_to_program(user_id)

		if str(user_id) in partnerable_users:
			partnerable_users.remove(str(user_id))
		
		if not partnerable_users:
			return await command_caller.dm_channel.send("You're still the only participant. We will call you when we find one, you don't need to repeat! :thumbsup:")




		# debug
		# await ctx.send(f"Possible partnerable people: {partnerable_users}")
		

		# this gives all possible matches:
		for participant in partnerable_users:
			# add each person's affinities to the list of all affinities
			all_user_affinities[participant] = ptools.affinity(user_id, participant)
		
		#debug
		# await ctx.send(f"All user affinities: {all_user_affinities}")

		
		
		# find highest one, pick any above 80% of it
		# give minimum points

		# we use a dictionary taking the student's discord id, then their affinity value so we can access
		# both of them in the same place, which we will need to later




		
		
		highest_affinity = max(all_user_affinities.values())
		min_partnerable_affinity = 44
		
		
		# stores the discord usernames of matched people - we can later exchange each their username's with
		# each other to start talking
		
		MemberUsername = str
		# keeps track of usernames along with user so we can send the matched person's name to the person
		# who called this command. a username is more helpful because they can search for it directly after
		# seeing it, unlike the other person's, say, real life name
		found_partners: Dict[MemberID, MemberUsername] = {}

		for person_id in all_user_affinities:
			person_affinity_score = all_user_affinities[person_id]
			if ptools.partner_eligible(person_affinity_score, highest_affinity, min_partnerable_affinity):
				found_partners[person_id] = ptools.get_user_username(person_id)

				# debugging
				# await ctx.send(ptools.get_user_username(person_id))
				# await ctx.send('work')

		#debugging
		# await ctx.send(found_partners)

		# if no partners found, send a message to the user notfiying them there hasn't been a match found,
		# but they will be put on a waitlist right away. they will be added on the wait list at the end of
		# this function to avoid repetition
		partnership_command_info_message = "This bot command matches people based on mutual themes and inclues factors such as grade level, volunteer hours, courses, clubs, and interests. Then gives them values and calculates how matchable users are. If you would like stop getting dms, use $... in our server!"
		
		# check if dict is empty - no partners found
		if not found_partners:
			await command_caller.dm_channel.send(
				"Hello :wave:! Unfortunately, there have not been any matches found for you yet :coffin:. You have been put on a waitlist and will be notified if anyone has chosen to be matched, and has matched with you :pray:!"
			)



		# notify command caller of successful partner finds
		# prepare a message from the first user till the last user
		# @ at the start because the first item in a list won't be joined, so we add it to the start
		# if there is only one match, we can't use a plural message
		
		

		elif len(found_partners) == 1: 
			matched_person_message = f"@{', @'.join([found_partners[partner] for partner in found_partners])}"
			await command_caller.dm_channel.send(f"A match has been found :scream:! Their username's {matched_person_message}")

		# remove the comma from the message since the grammar wouldn't need it
		elif len(found_partners) == 2:
			found_partners[list(found_partners)[-1]] = 'and @' + found_partners[list(found_partners)[-1]]
			matched_person_message = f"@{' '.join([found_partners[partner] for partner in found_partners])}"
			
			await command_caller.dm_channel.send(f"Matches found!!! They are: {matched_person_message}")


		# send a message with plural grammar
		else:
			middle_matched_people_message = f"@{', @'.join([found_partners[partner] for partner in list(found_partners)[:-1]])}"
			last_matched_person_message = f', and @{found_partners[list(found_partners)[-1]]}'
			await command_caller.dm_channel.send(f"Matches been found :white_check_mark:! They are: {middle_matched_people_message + last_matched_person_message}")


		# dm the matched people of a matche found
		for person in found_partners: 
			person_matched = await guild.fetch_member(person)
			await person_matched.create_dm()

			command_caller_username = ptools.get_user_username(user_id)
			await person_matched.dm_channel.send(f"We've found a new match for you! @{command_caller_username} will surely be glad to meet you!")


		
		
		# add command caller to partner program waitlist, first check if they're alredady on it
		if not ptools.user_participating(user_id):
			ptools.add_participant_to_program(user_id)
	
	except:
		await ctx.send(":rofl: LMAO! You don't have a profile! Make one with the `create_profile` command! :thumbsup:")



@bot.command()
async def test(ctx) -> discord.message.Message:
	await ctx.send(type(test))


TOKEN = "[ADDYOURSHERE]"
bot.run(TOKEN)
