from aiogram import types
import naxApi
from aiogram.utils.callback_data import CallbackData

nax = naxApi.Nax()

next_post = CallbackData("next", "id") 
prev_post = CallbackData('prev', 'id')
source_callback = CallbackData('source', 'src')

gitHubButton = types.InlineKeyboardButton('Project Github', url='https://github.com/Coolenov/NaxProject')


def getStartButtons():
	sources = nax.GetSources()

	buttons_arr = []
	for name in sources:
		buttons_arr.append(types.InlineKeyboardMarkup(text=name,callback_data=source_callback.new(src=name)))
	
	
	return buttons_arr

def getPaginationButtons(content:naxApi.Content):
	next_button = types.InlineKeyboardButton(text = 'Next post', callback_data=next_post.new(id = content.Id))
	prev_button = types.InlineKeyboardButton(text = 'Previous post', callback_data=prev_post.new(id = content.Id))
	buttons_arr = [prev_button,next_button]
	
	return buttons_arr

def getSourceLinkButton(content:naxApi.Content):
	return types.InlineKeyboardButton(text = "Read more..", url = content.Link)

def getMainMenuButton():
	return types.InlineKeyboardButton(text = "Main menu", callback_data = 'back_to_main_menu')