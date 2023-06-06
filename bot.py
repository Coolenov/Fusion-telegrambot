from aiogram import Bot, Dispatcher, executor, types
import markups
import naxApi
import buttons
from dotenv import load_dotenv
import os
from aiogram.types import InputMediaPhoto

load_dotenv()
# API_TOKEN = os.getenv('API_TOKEN')
API_TOKEN = '5913877491:AAEoeG0OpZr9h-XrTSGa3TnAr-Du_ajxZiI'

bot = Bot(token=API_TOKEN,parse_mode="HTML")
nax = naxApi.Nax()
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start_cmd_handler(message: types.Message):
	# await message.answer("Pick source", reply_markup = markups.getStartMarkup() )
	await message.answer_photo(caption="Pick source",photo = "https://www.verywellhealth.com/thmb/byKanhPiJ0kC3WLttQV_wVaf4yE=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/What-are-the-three-levels-of-autism-260233-5baab02fc9e77c002c390bd2.png", reply_markup=markups.getStartMarkup())


@dp.callback_query_handler(buttons.source_callback.filter())
async def inline_kb_answer_callback_handler(query: types.CallbackQuery, callback_data:dict):
	content = nax.GetLastContentBySource(callback_data["src"])
	text = nax.GetTextForTelegramMessage(content)

	if "photo" in query.message:
		if content.ImageUrl:
			media = InputMediaPhoto(media=content.ImageUrl, caption=text)
			await query.message.edit_media(media=media, reply_markup=markups.getPaginationMarkup(content))
			
		else:
			await query.message.delete()
			await query.message.answer(text,reply_markup=markups.getPaginationMarkup(content))
		
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
	content = nax.GetNextContent(callback_data["id"])
	if not content:
		await query.answer("No more content")
		return
	text = nax.GetTextForTelegramMessage(content)

	if "photo" in query.message:
		if content.ImageUrl:
			media = InputMediaPhoto(media=content.ImageUrl, caption=text)
			await query.message.edit_media(media=media, reply_markup=markups.getPaginationMarkup(content))
			
		else:
			await query.message.delete()
			await query.message.answer(text,reply_markup=markups.getPaginationMarkup(content))
		
	else:
		if content.ImageUrl:
			await query.message.delete()
			await query.message.answer_photo(caption=text, photo = content.ImageUrl, reply_markup = markups.getPaginationMarkup(content))
		else:
			await query.message.edit_text(text = text, reply_markup = markups.getPaginationMarkup(content))
	


@dp.callback_query_handler(buttons.prev_post.filter())
async def prev_callback_handler(query: types.CallbackQuery, callback_data: dict):
	content = nax.GetPreviousContent(callback_data["id"])
	text = nax.GetTextForTelegramMessage(content)
	if "photo" in query.message:
		if content.ImageUrl:
			media = InputMediaPhoto(media=content.ImageUrl, caption=text)
			await query.message.edit_media(media=media, reply_markup=markups.getPaginationMarkup(content))
			
		else:
			await query.message.delete()
			await query.message.answer(text,reply_markup=markups.getPaginationMarkup(content))
		
	else:
		if content.ImageUrl:
			await query.message.delete()
			await query.message.answer_photo(caption=text, photo = content.ImageUrl, reply_markup = markups.getPaginationMarkup(content))
		else:
			await query.message.edit_text(text = text, reply_markup = markups.getPaginationMarkup(content))

if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)



