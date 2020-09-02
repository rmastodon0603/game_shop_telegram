test_text = 'Hello world first_name anrey'
if test_text.split().count('first_name'):
	print (test_text.split().count('first_name'))
	print (test_text.find('first_name'))
	l = len(test_text)
	index_of_first_name = int(test_text.find('first_name')) - 1
	test_text_part1 = test_text[0:index_of_first_name]
	print(test_text_part1)
	test_text_part2 = test_text[index_of_first_name+11:l]
	print(test_text_part2)
else:
	print('No')