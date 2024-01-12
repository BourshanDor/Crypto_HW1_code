cipher_path = r"/home/dorbourshan/projects/Self_Study/crypto/BSc/cipher.txt"
common_words_path = r"/home/dorbourshan/projects/Self_Study/crypto/BSc/common_words.txt"

common_words = [] 
with open(common_words_path, "r") as file :
    lines = file.readlines()
for line in lines: 
    common_words.append(line.strip())

double_letter_frequencies_english = ['l']
trigram_letter_frequencies_english = ['the']

decryption_key = {} 


def letter_frequencies_in_text(text : str) -> dict: 
    """
    Letter frequency counter :  
    return a dictionary with pairs : (latter :  frequency in the text)  
    """
    english_letters = 'abcdefghijklmnopqrstuvwxyz'
    text_letter_frequency = {} 
    for letter in english_letters : 
        text_letter_frequency[letter] = 0 

    letter_number_factor = 100/len(text)

    for letter in text : 
        text_letter_frequency[letter] += 1

    for letter in text_letter_frequency : 
        text_letter_frequency[letter] *= letter_number_factor 
        text_letter_frequency[letter] = round(text_letter_frequency[letter], 1)
    
    return  dict(sorted(text_letter_frequency.items(), key=lambda item: -1 * item[1]))

def double_letter_frequencies_in_text(text : str, double_letter_frequencies_english_list=double_letter_frequencies_english): 
    """
    The function counters the double letter in the text and calculates the frequencies.

    update the decryption key as well. 
    """
    double_letter_frequency_text = {} 

    for i in range(len(text) - 1) : 
        if text[i] == text[i+1] : 
            common_double_letter_english = text[i]
            if common_double_letter_english not in double_letter_frequency_text : 
                double_letter_frequency_text[common_double_letter_english] = 1 
            else : 
                double_letter_frequency_text[common_double_letter_english] += 1  
                
    for common_double_letter_english in double_letter_frequencies_english_list : 
        common_double_letter_text  = max(double_letter_frequency_text, key=lambda k: double_letter_frequency_text[k])
        if common_double_letter_text not in decryption_key and  common_double_letter_english not in decryption_key: 
                decryption_key[common_double_letter_text] = common_double_letter_english
                decryption_key[common_double_letter_english] = common_double_letter_text
                del double_letter_frequency_text[common_double_letter_text]


def trigrams_letter_frequencies_in_text(text : str, trigram_letter_frequencies_english_list = trigram_letter_frequencies_english): 
    """
    Add to the decryption key 6 (because it is symmetric) letters.    
    Those letters are the most apparent together in the English texts. 
    Update the decryption key as well. 
    """
    trigrams_text_letter_frequency = {} 
    
    for i in range(len(text) - 2) : 
        trigrams = text[i:i+3]
        if trigrams not in trigrams_text_letter_frequency : 
            trigrams_text_letter_frequency[trigrams] = 1 
        else : 
            trigrams_text_letter_frequency[trigrams] += 1 

    
    
    for common_trigrams_letters_english in trigram_letter_frequencies_english_list : 
        common_trigrams_letters_text  = max(trigrams_text_letter_frequency, key=lambda k: trigrams_text_letter_frequency[k])

        for letter1, letter2 in zip(common_trigrams_letters_text, common_trigrams_letters_english) : 
            if letter1 not in decryption_key and  letter2 not in decryption_key: 
                decryption_key[letter1] = letter2
                decryption_key[letter2] = letter1
        del trigrams_text_letter_frequency[common_trigrams_letters_text]


def get_decrypt_keys(letter_frequency_text : dict) -> list[dict]: 
    """
    Take the most frequency letter in the cipher and match it to the most frequency letter in english texts. 
    create a list of optional decrypt keys, by switching near by letter frequencies.
    return the decrypt_keys
    """
    letter_frequency = {'e' : 12.7,'t' : 9.10, 'a' : 8.2, 'o' : 7.5, 'i' : 7.0, 'n' : 6.7, 's' : 6.3, 'r' : 6.0, 'h' : 6.1, 'd' : 4.3, 'l' : 4.0, 'u' : 2.8, 'c' : 2.8, 'm' : 2.4, 'f' : 2.2, 'y' : 2.0, 'w' : 2.4, 'g' : 2.0, 'p' : 1.9, 'b' : 1.5,'v' : 1.0, 'k' : 0.8, 'x' : 0.2, 'q' : 0.1, 'j' : 0.2, 'z' : 0.1 }
    
    letter_frequency = dict(sorted(letter_frequency.items(), key=lambda item: -1 * item[1]))
    for key in decryption_key : 
        del letter_frequency[key]
        del letter_frequency_text[key]

    list_letter_english = list(letter_frequency.keys())
    list_letter_text = list(letter_frequency_text.keys())
    switch_lists_letter_english = [list_letter_english.copy()] 
    for i in range(len(list_letter_english) - 1) : 
        switch_list = list_letter_english.copy() 
        tmp = switch_list[i+1] 
        switch_list[i+1] = switch_list[i]
        switch_list[i] = tmp 
        switch_lists_letter_english.append(switch_list)

    list_decryption_key = [] 
    for list_letter in switch_lists_letter_english : 

        copy_decryption_key = decryption_key.copy()

        for i,cipher_letter in enumerate(list_letter_text) :
            copy_decryption_key[cipher_letter] = list_letter[i]
            copy_decryption_key[list_letter[i]] = cipher_letter
        list_decryption_key.append(copy_decryption_key)

    return list_decryption_key

def counter_common_words(plaintext :str, common_words=common_words) : 
    """
    return the number of common words that appear in the plaintext. 
    """
    counter = 0 

    for word in common_words : 
        counter += plaintext.count(word) 
    return counter


def decrypt(cipher : str) -> str :
    """
    decrypt the cipher and return the best plaintext that found with the decryption key. 
    """
    plaintext = '' 
    trigrams_letter_frequencies_in_text(cipher)
    double_letter_frequencies_in_text(cipher)
    decrypt_keys = get_decrypt_keys(letter_frequencies_in_text(cipher))

    winner_plaintext = '' 
    winner_counter = 0
    winner_decrypt_key = {} 
    for decrypt_key in decrypt_keys : 
        plaintext = ''
        for letter in cipher :
            plaintext += decrypt_key[letter] 
        counter = counter_common_words(plaintext)
        if counter > winner_counter : 
            winner_counter = counter
            winner_plaintext = plaintext
            winner_decrypt_key = decrypt_key
    

    return winner_plaintext, winner_decrypt_key


def main() : 
    with open(cipher_path, "r") as file : 
        cipher = file.read() 

    plaintext, decrypt_key = decrypt(cipher)
    print(plaintext) 
    print(decrypt_key) 
    print("*************************************************************************************************************")
    fine_tuning_key =  {'x': 'a', 'a': 'x', 'm': 'l', 'l': 'm', 'o': 'e', 'e': 'o', 'n': 't', 't': 'n', 'q': 'g', 'g': 'q', 'i': 'z', 'z': 'i', 's': 's', 'b': 'c', 'c': 'b', 'w': 'r', 'r': 'w', 'u': 'h', 'h': 'u', 'k': 'd', 'd': 'k', 'j' : 'f', 'f' : 'j', 'p' :'v', 'v' :'p', 'y' :'y'}
    plaintext = ''
    for letter in cipher :
        if letter in fine_tuning_key : 
            plaintext += fine_tuning_key[letter]
        else : 
            plaintext += letter
    print(plaintext)


if __name__ == '__main__' : 
    main() 
