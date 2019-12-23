import urllib.request
from bs4 import  BeautifulSoup

def get_html(url):
	try:
		response = urllib.request.urlopen(url)
	except urllib.error.HTTPError as e:
		return "-1"
	except urllib.error.URLError as e:
		return "-1"
	else:
		return response.read()

def validation(word):
	try:
		word.encode('ascii')
		word.encode(encoding = 'utf-8')
	except UnicodeEncodeError:	
		return False
	else:
		return word.isalpha()

def parse_word(word):
	search_url = "https://www.dictionary.com/browse/" + word + "?s=t"
	html = get_html(search_url)
	if validation(word) == True and html !="-1":
		soup  = BeautifulSoup(html, features = "html5lib")
		soups = soup.find_all('section', class_="css-pnw38j e1hk9ate0", limit =3)
		output = ""
		# print(len(soups))
		for soup in soups:
			output += soup.get_text("\n", strip = True) + "\n"
		# print(output)
		output = output.replace("SEE MORE","")
		output = output.replace("SEE LESS","")
		output = output.replace("SEE FEWER IDIOMS","")
		output = output.replace("IDIOMS","")

		list = output.splitlines()
		output = "*" + word + "*\n\n"
		for line in list:
			if len(line)>2: output += line + "\n"
		output = output.replace("noun","\n*noun*")
		output = output.replace("adverb","\n*adverb*")
		output = output.replace("verb ","\n*verb*")
		output = output.replace("adjective","\n*adjective*")
		output = output.replace("Informal","_Informal_")
		output = output.replace("Slang","_Slang_")
		return output
	else:
		output = "Sorry, but there is an error with the given word. You may try again. (that word must contains only english letters)"
		return output

def parse_synonyms(word):
	synonyms_url = "https://www.thesaurus.com/browse/" + word + "?s=t"
	html = get_html(synonyms_url)
	if validation(word) == True and html !="-1":		
		soup  = BeautifulSoup(html, features = "html5lib")
		output = soup.find('div', class_="css-1kc5m8x e1qo4u830").get_text("\n",strip=True)
		word  = word.lower()
		output = output[output.find(word)+len(word):len(output)]
		output = "Synonyms for *" + word + "*:\n" + output
		output = output.replace("MOST RELEVANT","")
		# print(output)
		return output
	else:
		output = "Sorry, but there is an error with the given word. You may try again. (that word must contains only english letters)"
		return output

def parse_word_of_the_day():
	html = get_html("https://www.dictionary.com/e/word-of-the-day/")
	soup = BeautifulSoup(html, features="html5lib")
	word = soup.find('div', class_="wotd-item-headword__word").get_text(strip = True)
	output = 'Today, the word is ' + '*' + word + '*\n\n'  + '_Explanation:_\n'
	# print(word)
	explanation = soup.find('div', class_="wotd-item-headword__pos").get_text("|",strip = True)
	word_type =  explanation[0:explanation.find("|")]
	other_stuff = ""
	explanation = explanation[explanation.find("|")+1:len(explanation)]
	while(explanation.find("|")!=-1):
		other_stuff += explanation[0:explanation.find("|")-1] + "\n"
		explanation = explanation[explanation.find("|")+1:len(explanation)]
	other_stuff += explanation
	output+= word_type + '\n' + other_stuff
	# print(word_type)
	# print(other_stuff)
	return output


