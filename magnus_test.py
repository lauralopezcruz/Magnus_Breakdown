from magnus import *

print(str_to_syllable("a_{0}^5"))
print(str_to_syllable("a^11_{0}"))
print(str_to_syllable("a^11"))
print(str_to_syllable("a_123"))

print(word_to_str(str_to_word("[x,y]^2a(bc^3)^2")))
print(word_to_str(str_to_word("[x,y]^2a(bc^3)")))
print(word_to_str(str_to_word("[x,y]^2a(bc^3)^-2z")))

print(str_to_group("<x,y|xy=yx>"))

#groups = magnus_breakdown(str_to_group("<a,b,c|bacb^2a^-3c^3a^2>"))
#groups = magnus_breakdown(str_to_group("<a,b,c,d|a^2bc^-1a>"))
