from aiogram import types
import buttons
import naxApi

def getStartMarkup():
	keyboard_markup = types.InlineKeyboardMarkup(row_width=9)
	

	buttons_arr = buttons.getStartButtons()
	result_arr = []
	for button in range(0, len(buttons_arr), 2):
	  temp_list = []
	  temp_list.append(buttons_arr[button:button + 2])
	  result_arr.append(temp_list)

	for i in result_arr:


		keyboard_markup.row(*i[0])
	keyboard_markup.add(buttons.gitHubButton)
	return keyboard_markup

def getPaginationMarkup(content:naxApi.Content):
	keyboard_markup = types.InlineKeyboardMarkup(row_width=3)

	buttons_arr = buttons.getPaginationButtons(content)

	keyboard_markup.row(*buttons_arr)
	keyboard_markup.add(buttons.getSourceLinkButton(content))
	keyboard_markup.add(buttons.getMainMenuButton())

	return keyboard_markup









