import string

##################
##################
# SYLLABLE CLASS #
##################

# The Syllable class represents group elements raised to a power. The group
# element may have a subscript, which is stored as a separate attribute.
class Syllable:
    def __init__(self, letter, subscript, exponent):
        self.ltr = letter    # string
        self.sub = subscript # int or empty string
        self.exp = exponent  # int

    def __str__(self):
        string = str(self.ltr)
        if self.sub != "":
            string = string + "_{" + str(self.sub) + "}"
        if self.exp != 1:
            string = string + "^{" + str(self.exp) + "}"
        return string

    def __eq__(self, other):
        if not isinstance(other, Syllable):
            return False
        return (self.ltr == other.ltr and
                self.sub == other.sub and
                self.exp == other.exp)

    def inverse(self):
        new_exp = -self.exp
        return Syllable(self.ltr, self.sub, new_exp)

    # Makes a new syllable with an additional subscript. If this syllable
    # already has a subscript, then the old subscript is moved into the letter.
    def add_subscript(self, new_subscript):
        if self.sub == "":
            return Syllable(self.ltr, new_subscript, self.exp)
        else:
            new_ltr = self.ltr + "_{" + str(self.sub) + "}"
            return Syllable(new_ltr, new_subscript, self.exp)

    def base(self):
        return Syllable(self.ltr, self.sub, 1)



#################################################################
#################################################################
# CONVERTING FROM STRINGS TO SYLLABLES AND WORDS AND VICE VERSA #
#################################################################

def str_to_syllable(string):
    letter = string[0]

    if "_" not in string: # e.g., a^5
        subscript = ""
    else: # e.g., a^5_3 or a_3^5
        left = string.index("_")+1
        right = string.index("^") if "^" in string[left:] else len(string)
        substring = string[left:right].replace("{","").replace("}","")
        subscript = int(substring)

    if "^" not in string: # e.g., b_2
        exponent = 1
    else: # e.g., a^5_3 or a_3^5
        left = string.index("^")+1
        right = string.index("_") if "_" in string[left:] else len(string)
        substring = string[left:right].replace("{","").replace("}","")
        exponent = int(substring)

    return Syllable(letter, subscript, exponent)

# A "word" is a list of syllables.
def word_to_str(word):
    if word == []:
        return "1"
    else:
        return " ".join([str(syllable) for syllable in word])

# This assumes there are no subscripts or greek letters...
def str_to_word(string):
    string = string.replace(" ","").replace("{","").replace("}","")

    # Expands commutators, e.g., [x,y]^2 -> (x^-1 y^-1 x y)^2
    while "]" in string:
        right = string.index("]")
        left = string[:right].rfind("[")
        comma = string[:right].rfind(",")
        first_arg = string[left+1:comma]
        second_arg = string[comma+1:right]

        string = (string[:left]
                  + "("
                  + word_to_str(invert_word(str_to_word(first_arg)))
                  + word_to_str(invert_word(str_to_word(second_arg)))
                  + first_arg
                  + second_arg
                  + ")"
                  + string[right+1:])

    # Replace any substrings in parentheses like (abc)^2 with the
    # substring repeated the right number of times, like abcabc
    while ")" in string:
        right = string.index(")")
        left = string[:right].rfind("(")
        substr = string[left+1:right]

        # If the substring in parentheses isn't followed by an exponent
        if right == len(string)-1 or string[right+1] != "^":
            string = string[:left] + substr + string[right+1:]
            continue

        # Otherwise build the exponent by taking all numeric characters or
        # minus signs following the carat.
        exp_str = ""
        exp_index = right+2
        for i in range(right+2, len(string)):
            if string[i].isnumeric() or string[i] == "-":
                exp_str = exp_str + string[i]
                exp_index = exp_index + 1
            else:
                break
        exp = int(exp_str)
        if exp >= 0:
            repeated_substr = substr * exp
        else:
            inverted_substr = word_to_str(invert_word(str_to_word(substr)))
            inverted_substr = inverted_substr.replace(" ","")
            repeated_substr = inverted_substr * -exp
        string = string[:left] + repeated_substr + string[right+2+len(exp_str):]

    # Cut string into syllables, assuming that an alphabet character indicates
    # the start of a new syllable (so this doesn't work for greek letters...)
    syllables = []
    syl_str = ""
    for i in range(len(string)):
        if not string[i].isalpha():
            syl_str = syl_str + string[i]
        else:
            if syl_str != "":
                print(syl_str)
                syllables.append(str_to_syllable(syl_str))
            syl_str = string[i]

    print(syl_str)
    syllables.append(str_to_syllable(syl_str))

    return syllables



####################################
####################################
# ALGEBRAIC MANIPULATIONS OF WORDS #
####################################

def reduce_word(word): # e.g., abaaa^-5 -> aba^-3
    syllables = word.copy()
    i = 0
    while i < len(syllables)-1:
        s1 = syllables[i]
        s2 = syllables[i+1]
        if s1.base() == s2.base():
            exp = s1.exp + s2.exp
            if exp !=0:
                product = Syllable(s1.ltr, s1.sub, exp)
                syllables = syllables[:i] + [product] + syllables[i+2:]
            else:
                syllables = syllables[:i] + syllables[i+2:]
        else:
            i = i+1
    return syllables

def invert_word(syllables): # e.g., a^2bc -> c^-1 b^-1 a^-2
    return [syl.inverse() for syl in list(reversed(syllables))]



###############
###############
# GROUP CLASS #
###############

class Group:
    def __init__(self, generators, relations):
        self.gens = generators # list of syllables
        self.rels = relations  # list of words

    def __str__(self):
        gens_str = ", ".join([str(g) for g in self.gens])
        rels_str = ", ".join([word_to_str(r) for r in self.rels])
        return "<" + gens_str + " | "  + rels_str + ">"

def str_to_group(string):
    string = (string.replace("<","").replace(">","")
                    .replace("\\langle","").replace("\\rangle","")
                    .replace(" ",""))

    divider = "\\mid" if "\\mid" in string else "|"

    generators_string = string[:string.index(divider)]
    generators = [str_to_syllable(s) for s in generators_string.split(",")]

    relations_string = string[string.index(divider)+len(divider):]
    strings = relations_string.split(",")
    relations = []
    for s in strings:
        if "=" not in s: # e.g., xyx^{-1}y^{-1}
            relations.append(str_to_word(s))
        else: # e.g., xy=yx or xyx^-1=1
            left = s[:s.index("=")]
            left_word = str_to_word(left)

            right = s[s.index("=")+1:]
            right_word = str_to_word(right)

            if left == "1":
                relations.append(right_word)
            elif right == "1":
                relations.append(left_word)
            else:
                left_word.extend(invert_word(right_word))
                relations.append(left_word)

    return Group(generators, relations)



###################################################
###################################################
# HELPER FUNCTIONS FOR MAGNUS BREAKDOWN ALGORITHM #
###################################################

def get_new_letters(used_letters, num_letters, preferred_letters=[]):
    available_letters = list(string.ascii_lowercase)
    available_letters.remove("i")
    available_letters.remove("j")
    greek_letters = ["alpha","beta","gamma","delta","epsilon","zeta","eta",
                     "theta","iota","kappa","lambda","mu","nu","xi","pi","rho",
                     "tau","phi","chi","psi","omega"]
    for letter in greek_letters:
        letter = "\\" + letter
    available_letters.extend(greek_letters)

    for letter in used_letters:
        available_letters.remove(letter)

    for letter in reversed(preferred_letters):
        if letter in available_letters:
            available_letters.remove(letter)
            available_letters.insert(0, letter)

    return available_letters[:num_letters]

def exponent_sum(generator, relation):
    return sum([syl.exp for syl in relation if syl.base() == generator.base() ])

# Here we rewrite relation so that the generator with exponent sum=0
# is not in the first position relation and generators are already adjusted
def remove_exp_zero(zero_generator,relation):
    syl = relation[0]
    if zero_generator.ltr == syl.ltr and zero_generator.sub == syl.sub:
        return reduce_word(relation[1:] + [syl.inverse()])
    else:
        return relation

def relation_prime(zero_generator,relation):
    new_relation = [relation[0].add_subscript(0)]
    for i in range(1,len(relation)):
        if relation[i].ltr != zero_generator.ltr:
            subscript = -exponent_sum(zero_generator, relation[:i])
            syl = relation[i].add_subscript(subscript)
            new_relation.append(syl)
    return(reduce_word(new_relation))

def smallest_subscript(letter,relation):
    return min([syl.sub for syl in relation if syl.ltr == letter])

def largest_subscript(letter,relation):
    return max([syl.sub for syl in relation if syl.ltr == letter])



##############################
##############################
# MAGNUS BREAKDOWN ALGORITHM #
##############################

def magnus_case1(group, used_letters=set()):
    generators = group.gens
    relation = reduce_word(group.rels[0])

    # Find a generator with exponent sum zero
    for generator in generators:
        if exponent_sum(generator, relation)==0:
            zero_generator = generator
            break

    relation_shifted = remove_exp_zero(zero_generator, relation)
    relation_p = relation_prime(zero_generator, relation_shifted)

    letters = {syl.ltr for syl in relation_p}
    new_generators = []
    letter_max_sub={}
    for letter in letters:
        l_subscript = largest_subscript(letter,relation_p)
        s_subscript = smallest_subscript(letter,relation_p)
        letter_max_sub[letter]=l_subscript
        for i in range(s_subscript, l_subscript+1):
            new_generators.append(Syllable(letter, i, 1))

    # Rewrite G as HNN extension
    used_letters = used_letters.union({g.ltr[0] for g in new_generators}).union({g.ltr[0] for g in relation})
    t=get_new_letters(used_letters,1,["t"])[0]
    used_letters = used_letters.union(t)
    new_generators_of_group=new_generators.copy()
    new_generators_of_group.append(Syllable(t,"",1))
    new_relations_of_group=[relation_p]
    for generator in new_generators:
        if generator.sub != letter_max_sub[generator.ltr]:
            new_relations_of_group.append([Syllable(t,"",-1),
                                           generator,
                                           Syllable(t,"",1),
                                           Syllable(generator.ltr,generator.sub+1,generator.exp*-1)])

    return [Group(new_generators_of_group, new_relations_of_group),
            Group(new_generators, [relation_p]),
            used_letters]

# This function rewrites a group G as a free product of free groups and a one
# relator group. It outputs a one relator group where all gen appear in relation
# and the free generators
def free_gen_rewrite(group):
    generators = group.gens
    relation = reduce_word(group.rels[0])
    free_generators=[]
    relation_letters=[(syl.ltr,syl.sub) for syl in relation]

    for generator in generators:
        if (generator.ltr,generator.sub) not in relation_letters:
            free_generators.append(generator)

    new_generators=[]
    for gen in generators:
        if gen not in free_generators:
            new_generators.append(gen)

    return [free_generators, Group(new_generators,[relation])]

# Returns a group that does have a zero generator than you can then input into
# magnus_case1
def magnus_case2(group, used_letters=set()):
    generators = group.gens
    gen0 = generators[0]
    gen1 = generators[1]
    relation=group.rels[0]
    exp_sum0 = exponent_sum(gen0,relation)
    exp_sum1 = exponent_sum(gen1,relation)

    used_letters = used_letters.union({gen.ltr[0] for gen in generators})
    x,y = get_new_letters(used_letters,2,["x","y"]) #gets two new letters for new generators
    used_letters = used_letters.union({x,y})
    syl_0=Syllable(x,"",1)
    syl_1=Syllable(y,"",1)
    replacement0 = [syl_1, Syllable(x, "", -exp_sum1)] #yx^{-\beta}
    replacement1 = [Syllable(x, "", exp_sum0)]         #x^{\alpha},x (syl_1) will be zero_gen now

    new_relation = []
    for i in range(len(relation)):
        if relation[i].ltr==gen0.ltr and relation[i].sub==gen0.sub:
            exp = relation[i].exp
            if exp >= 0:
                replacements = replacement0 * exp
            else:
                replacements = invert_word(replacement0) * (-exp)
            new_relation.extend(replacements)

        elif relation[i].ltr == gen1.ltr and relation[i].sub==gen1.sub:
            exp = relation[i].exp
            if exp >= 0:
                replacements = replacement1 * exp
            else:
                replacements = invert_word(replacement1) * (-exp)
            new_relation.extend(replacements)
        else:
            new_relation.append(relation[i])

    new_generators=[syl_0,syl_1]
    new_generators.extend(generators[2:])

    return [Group(new_generators,[reduce_word(new_relation)]),
            used_letters]

def magnus_breakdown(group):
    print(group)
    hierarchy_of_groups=[group]

    used_letters = {gen.ltr[0] for gen in group.gens}

    while relation_length(hierarchy_of_groups[-1].rels[0])>1:
        free_generators, group =free_gen_rewrite(group)
        generators = group.gens
        relation = reduce_word(group.rels[0])

        zero_gen=None
        for gen in generators:
            if exponent_sum(gen,relation)==0:
                zero_gen=gen
                break
        if zero_gen != None:
            [original_group, group, used_letters] = magnus_case1(group, used_letters)
            hierarchy_of_groups.append(group)
            print("\nCase 1: "+str(group))
        else:
            [group, used_letters] = magnus_case2(group, used_letters)
            hierarchy_of_groups.append(group)
            print("\nCase 2: "+str(group))

    return hierarchy_of_groups
