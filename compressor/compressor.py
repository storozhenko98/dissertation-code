sample_text = "But I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness. No one rejects, dislikes, or avoids pleasure itself, because it is pleasure, but because those who do not know how to pursue pleasure rationally encounter consequences that are extremely painful. Nor again is there anyone who loves or pursues or desires to obtain pain of itself, because it is pain, but because occasionally circumstances occur in which toil and pain can procure him some great pleasure. To take a trivial example, which of us ever undertakes laborious physical exercise, except to obtain some advantage from it? But who has any right to find fault with a man who chooses to enjoy a pleasure that has no annoying consequences, or one who avoids a pain that produces no resultant pleasure?"
#get sample text size in bytes
sample_text_size = len(sample_text.encode('utf-8'))
print("Sample text size: " + str(sample_text_size) + " bytes")

#compressor
##create word list
word_list = sample_text.split()
##for each word in word list, give unique number unless same word 
##has already been given a number
word_dict = {}
n=1
for word in word_list:
    if word not in word_dict:
        word_dict[word] = len(word_dict)+n
        n+=1
#print(word_dict)
#convert string to list of numbers
compressed_text = []
for word in word_list:
    compressed_text.append(word_dict[word])
#print(compressed_text)

#get compressed text size in bytes
compressed_text_size = len(compressed_text)*4
print("Compressed text size: " + str(compressed_text_size) + " bytes")

#convert back 
decompressed_text = []
for number in compressed_text:
    for word in word_dict:
        if word_dict[word] == number:
            decompressed_text.append(word)
#print(decompressed_text)

#convert back to string
decompressed_text_string = " ".join(decompressed_text)
#print(decompressed_text_string)

#calculate efficiency 
efficiency = (compressed_text_size/sample_text_size)*100
print("Efficiency: " + str(round(efficiency, 2)) + "%")
print("Compression ratio: " + str(round(sample_text_size/compressed_text_size, 2)))
print("This means that the compressed text is " + str(round(sample_text_size/compressed_text_size, 2)) + " times smaller than the original text")

#check if decompressed text is the same as original text
if decompressed_text_string == sample_text:
    print("Decompressed text is the same as original text")
else:
    print("Decompressed text is not the same as original text")

