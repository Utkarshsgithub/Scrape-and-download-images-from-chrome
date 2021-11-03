import time
from selenium.webdriver.common.by import By
from selenium import webdriver
import requests
import io
import time
from PIL import Image


PATH = r"C:\Users\Dell\Desktop\Web Scraping Images\chromedriver.exe"

wd = webdriver.Chrome(PATH)

def get_images_from_google(wd, delay, max_images):
	def scroll_down(wd):
		wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(delay)

	url = "https://www.google.com/search?q=apple+products+900x900+images&tbm=isch&ved=2ahUKEwjhkuLUyvTzAhU2nksFHQGJBHMQ2-cCegQIABAA&oq=apple+products+900x900+images&gs_lcp=CgNpbWcQA1AAWLULYMQRaABwAHgBgAGZAogB1wuSAQUwLjMuNJgBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=A4N-YaGFELa8rtoPgZKSmAc&bih=674&biw=1036&hl=en-US"

	wd.get(url)

	image_urls = set()
	skips = 0

	while len(image_urls) + skips < max_images:
		scroll_down(wd)

		thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

		for img in thumbnails[len(image_urls) + skips:max_images]:
			try:
				img.click()
				time.sleep(delay)
			except:
				continue

			images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
			for image in images:
				if image.get_attribute('src') in image_urls:
					max_images += 1
					skips += 1
					break

				if image.get_attribute('src') and 'http' in image.get_attribute('src'):
					image_urls.add(image.get_attribute('src'))
					print(f"Found Image {len(image_urls)}")

	return image_urls


def download_image(download_path, url, file_name):
	try:
		image_content = requests.get(url).content
		image_file = io.BytesIO(image_content)
		image = Image.open(image_file)
		file_path = download_path + file_name

		with open(file_path, "wb") as f:
			image.save(f, "JPEG")

		print("Success! Image Downloaded")
	except Exception as e:
		print('FAILED -', e)

urls = get_images_from_google(wd, 1, 6)

for i, url in enumerate(urls):
	download_image("images/", url, str(i) + ".jpg")

wd.quit()
