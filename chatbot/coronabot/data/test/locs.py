import os 

lines = open('location.txt').read().splitlines()
lines.remove('')

strings = []
strings.append("- [صدر](location) میں حادثہ ہوا ہے")
strings.append("- [صدر](location) کے نزدیک ہادثہ ہوا")
strings.append("- گاڑی [صدر](location) رکی ہے")
strings.append("- گاڑی [صدر](location) کھڑی ہے")
strings.append("- بس [صدر](location) کھڑی ہے")		
strings.append("- [صدر](location) کے پاس ایکسیڈینٹ ہوا")
strings.append("- ہم [صدر](location) کھڑے ہیں")
strings.append("- میرا گھر [صدر](location) میں ہے")

new_lines = []
for each in lines[0:500]:
	for string in strings: 
		new_lines.append(string.replace('صدر',each))

for each in new_lines:
	print(each)
