from aiogram import Bot, Dispatcher, executor, types
import markups
import api_requests
import buttons
from dotenv import load_dotenv
from aiogram.types import InputMediaPhoto

load_dotenv()
# API_TOKEN = os.getenv('API_TOKEN')
API_TOKEN = '6241788210:AAHr2tzLuD1aGQChDWqnyau_pjnC6WD7FyA'
bot = Bot(token=API_TOKEN,parse_mode="HTML")
fusion = api_requests.Request()
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start_cmd_handler(message: types.Message):
	await message.answer_photo(caption="Сhoose an interesting resource.",
							   photo = "https://e7.pngegg.com/pngimages/471/782/png-clipart-software-testing-beta-tester-computer-software-api-testing-roblox-others-emblem-service-thumbnail.png",
							   reply_markup=markups.getStartMarkup())


@dp.callback_query_handler(buttons.source_callback.filter())
async def inline_kb_answer_callback_handler(query: types.CallbackQuery, callback_data:dict):
	content = fusion.GetLastContentBySource(callback_data["src"])
	text = fusion.GetTextForTelegramMessage(content)

	if "photo" in query.message:
		if content.ImageUrl:
			media = InputMediaPhoto(media=content.ImageUrl, caption=text)
			await query.message.edit_media(media=media, reply_markup=markups.getPaginationMarkup(content))
			
		else:
			await query.message.delete()
			await query.message.answer(text, reply_markup=markups.getPaginationMarkup(content))
		
	else:
		if content.ImageUrl:
			await query.message.delete()
			await query.message.answer_photo(caption=text, photo = content.ImageUrl, reply_markup = markups.getPaginationMarkup(content))
		else:
			await query.message.edit_text(text = text, reply_markup = markups.getPaginationMarkup(content))

		





@dp.callback_query_handler(text='back_to_main_menu') 
async def inline_kb_answer_callback_handler(query: types.CallbackQuery):
	await query.message.delete()
	await start_cmd_handler(query.message)


@dp.callback_query_handler(buttons.next_post.filter())
async def next_callback_handler(query: types.CallbackQuery, callback_data: dict):
	content = fusion.GetNextContent(callback_data["id"])
	if not content:
		await query.answer("No more content")
		return
	text = fusion.GetTextForTelegramMessage(content)

	if "photo" in query.message:
		if content.ImageUrl:
			media = InputMediaPhoto(media=content.ImageUrl, caption=text)
			await query.message.edit_media(media=media, reply_markup=markups.getPaginationMarkup(content))
			
		else:
			await query.message.delete()
			await query.message.answer(text, reply_markup=markups.getPaginationMarkup(content))
		
	else:
		if content.ImageUrl:
			await query.message.delete()
			await query.message.answer_photo(caption=text, photo = content.ImageUrl, reply_markup = markups.getPaginationMarkup(content))
		else:
			await query.message.edit_text(text = text, reply_markup = markups.getPaginationMarkup(content))
	


@dp.callback_query_handler(buttons.prev_post.filter())
async def prev_callback_handler(query: types.CallbackQuery, callback_data: dict):
	content = fusion.GetPreviousContent(callback_data["id"])
	text = fusion.GetTextForTelegramMessage(content)
	if "photo" in query.message:
		if content.ImageUrl:
			media = InputMediaPhoto(media=content.ImageUrl, caption=text)
			await query.message.edit_media(media=media, reply_markup=markups.getPaginationMarkup(content))
			
		else:
			await query.message.delete()
			await query.message.answer(text, reply_markup=markups.getPaginationMarkup(content))
		
	else:
		if content.ImageUrl:
			await query.message.delete()
			await query.message.answer_photo(caption=text, photo = content.ImageUrl, reply_markup = markups.getPaginationMarkup(content))
		else:
			await query.message.edit_text(text = text, reply_markup = markups.getPaginationMarkup(content))

if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)



