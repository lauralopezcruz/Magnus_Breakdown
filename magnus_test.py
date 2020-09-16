from magnus import *
import unittest

class TestIO(unittest.TestCase):
    def test_syllable_methods(self):
        x = Syllable("x",[],1)
        x = x.pow(3)
        x = x.add_subscript(0)
        self.assertEqual(x, Syllable("x",[0],3))
        x = x.add_subscript(1)
        self.assertEqual(x, Syllable("x",[0,1],3))
        x = x.inverse()
        self.assertEqual(x, Syllable("x",[0,1],-3))
        x = x.base()
        self.assertEqual(x, Syllable("x",[0,1],1))
        self.assertEqual(str(x.pow(55)), "x_{0,1}^{55}")

    def test_str_to_syllable(self):
        self.assertEqual(str_to_syllable("a_{0}^5"), Syllable("a",[0],5))
        self.assertEqual(str_to_syllable("a^11_{0}"), Syllable("a",0,11))
        self.assertEqual(str_to_syllable("a^11"), Syllable("a",[],11))
        self.assertEqual(str_to_syllable("a_{123}"), Syllable("a",123,1))
        self.assertEqual(str_to_syllable("a_123"), Syllable("a",123,1))
        self.assertEqual(str_to_syllable("a_{12,3}^9"), Syllable("a",[12,3],9))

    def test_str_to_word(self):
        b = Syllable("b",[],1)
        c3 = Syllable("c",[],3)
        self.assertEqual(str_to_word("bc^3"), [b,c3])
        self.assertEqual(str_to_word("(bc^3)^2"), [b,c3,b,c3])

        x = Syllable("x",[],1)
        y = Syllable("y",[],1)
        commutator = [x.inverse(), y.inverse(), x, y]
        self.assertEqual(str_to_word("[x,y]"), commutator)
        self.assertEqual(str_to_word("[x,y]^2"), commutator + commutator)

        a = Syllable("a",[],1)
        z = Syllable("z",[],1)
        bc3_inverse = invert_word([b,c3])
        self.assertEqual(str_to_word("[x,y]^2a(bc^3)^2"),
                         commutator + commutator + [a,b,c3,b,c3])
        self.assertEqual(str_to_word("[x,y]^2a(bc^3)"),
                         commutator + commutator + [a,b,c3])
        self.assertEqual(str_to_word("[x,y]^2a(bc^3)^-2z"),
                         commutator + commutator + [a]
                         + bc3_inverse + bc3_inverse + [z])

        g = Syllable("g",[1,2,3],33)
        h = Syllable("h",[44,5],1)
        commutator = [g.inverse(), h.inverse(), g, h]
        self.assertEqual(str_to_word("[g_{1,2,3}^{33}, h_{44,5}]"), commutator)

    def test_word_to_str(self):
        a = Syllable("a",[],1)
        b = Syllable("b",[],1)
        c3 = Syllable("c",[],3)
        x = Syllable("x",[],1)
        y = Syllable("y",[],1)
        z = Syllable("z",[],1)
        commutator = [x.inverse(), y.inverse(), x, y]
        bc3_inverse = invert_word([b,c3])
        word = commutator + commutator + [a] + bc3_inverse + bc3_inverse + [z]

        s = "x^{-1} y^{-1} x y x^{-1} y^{-1} x y a c^{-3} b^{-1} c^{-3} b^{-1} z"
        self.assertEqual(word_to_str(word), s)

    def test_str_to_group(self):
        x = Syllable("x",[],1)
        y = Syllable("y",[],1)
        relation = [x, y, x.inverse(), y.inverse()]
        group = Group([x,y],[relation])
        self.assertEqual(str_to_group("<x,y|xy=yx>"), group)



class TestMagnusCase1(unittest.TestCase):
    def test1(self):
        a = Syllable("a",[],1)
        b = Syllable("b",[],1)
        c = Syllable("c",[],1)
        relation = reduce_word([a.inverse(), b, c, a, a, b.inverse()])
        group = Group([a,b,c],[relation])
        self.assertEqual(group, str_to_group("<a,b,c|a^-1 b c a^2 b^-1>"))

        a_minus1 = Syllable("a",-1,1)
        a_0      = Syllable("a",0,1)
        c_minus1 = Syllable("c",-1,1)
        t        = Syllable("t",[],1)

        HNN_rel1 = [a_0.inverse(), c_minus1, a_minus1.pow(2)]
        HNN_rel2 = [t.inverse(), a_minus1, t, a_0.inverse()]
        HNN = Group([a_minus1, a_0, c_minus1, t], [HNN_rel1, HNN_rel2])

        new_group = Group([a_minus1, a_0, c_minus1], [HNN_rel1])

        [G, H, used_letters] = magnus_case1(group)
        self.assertEqual(HNN, G)
        self.assertEqual(new_group, H)

    def test2(self):
        a = Syllable("a",[],1)
        b = Syllable("b",[],1)
        c = Syllable("c",[],1)
        word = [b, a, c, b.pow(2), a.pow(-3), c.pow(3), a.pow(2)]
        relation = reduce_word(word)
        group = Group([a,b,c],[relation])
        self.assertEqual(group, str_to_group("<a,b,c|bacb^2a^-3c^3a^2>"))

        c_minus1 = Syllable("c",-1,1)
        c_0      = Syllable("c",0,1)
        c_1      = Syllable("c",1,1)
        c_2      = Syllable("c",2,1)
        b_minus1 = Syllable("b",-1,1)
        b_0      = Syllable("b",0,1)
        t        = Syllable("t",[],1)

        HNN_rel1 = [b_0, c_minus1, b_minus1.pow(2), c_2.pow(3)]
        HNN_rel2 = [t.inverse(), c_minus1, t, c_0.inverse()]
        HNN_rel3 = [t.inverse(), c_0,      t, c_1.inverse()]
        HNN_rel4 = [t.inverse(), c_1,      t, c_2.inverse()]
        HNN_rel5 = [t.inverse(), b_minus1, t, b_0.inverse()]
        HNN_gens = [c_minus1, c_0, c_1, c_2, b_minus1, b_0, t]
        HNN = Group(HNN_gens, [HNN_rel1, HNN_rel2, HNN_rel3, HNN_rel4, HNN_rel5])

        new_group_gens = [b_minus1, b_0, c_minus1, c_0, c_1, c_2]
        new_group = Group(new_group_gens, [HNN_rel1])

        [G, H, used_letters] = magnus_case1(group)
        self.assertEqual(HNN, G)
        self.assertEqual(new_group, H)

    def test3(self):
        # group = <a,b,c,d,e,f,x | b a c b^{2} a^{-3} c^{3} a^{2} d>
        a = Syllable("a",[],1)
        b = Syllable("b",[],1)
        c = Syllable("c",[],1)
        d = Syllable("d",[],1)
        e = Syllable("e",[],1)
        f = Syllable("f",[],1)
        x = Syllable("x",[],1)
        relation = [b, a, c, b.pow(2), a.pow(-3), c.pow(3), a.pow(2), d]
        group = Group([a,b,c,d,e,f,x], [relation])

        free_gens, G = free_gen_rewrite(group)
        self.assertEqual(free_gens, [e,f,x])
        self.assertEqual(G, Group([a,b,c,d], [relation]))

        b_minus1 = Syllable("b",-1,1)
        b_0      = Syllable("b",0,1)
        d_0      = Syllable("d",0,1)
        c_minus1 = Syllable("c",-1,1)
        c_0      = Syllable("c",0,1)
        c_1      = Syllable("c",1,1)
        c_2      = Syllable("c",2,1)
        t        = Syllable("t",[],1)

        HNN_rel1 = [b_0, c_minus1, b_minus1.pow(2), c_2.pow(3), d_0]
        HNN_rel2 = [t.inverse(), b_minus1, t, b_0.inverse()]
        HNN_rel3 = [t.inverse(), c_minus1, t, c_0.inverse()]
        HNN_rel4 = [t.inverse(), c_0,      t, c_1.inverse()]
        HNN_rel5 = [t.inverse(), c_1,      t, c_2.inverse()]
        HNN_gens = [b_minus1, b_0, d_0, c_minus1, c_0, c_1, c_2, t]
        HNN = Group(HNN_gens, [HNN_rel1, HNN_rel2, HNN_rel3, HNN_rel4, HNN_rel5])

        new_group_gens = [b_minus1, b_0, d_0, c_minus1, c_0, c_1, c_2]
        new_group = Group(new_group_gens, [HNN_rel1])

        [G_as_HNN, H, used_letters] = magnus_case1(G)
        self.assertEqual(G_as_HNN, HNN)
        self.assertEqual(H, new_group)

    def test4(self):
        a = Syllable("a",[],1)
        b = Syllable("b",[],1)
        relation = [a, b.pow(10), a, b.pow(-7), a, b.pow(-3)]
        group = Group([a,b], [relation])
        self.assertEqual(group, str_to_group("<a,b|ab^10 ab^{-7} ab^{-3}>"))

        HNN_gens = [Syllable("a",i,1) for i in range(-10,1)]
        new_group_gens = HNN_gens.copy()
        t = Syllable("t",[],1)
        HNN_gens.append(t)

        HNN_rel1 = [Syllable("a",0,1), Syllable("a",-10,1), Syllable("a",-3,1)]
        HNN_rels = [[t.inverse(), Syllable("a",i,1), t, Syllable("a",i+1,-1)]
                    for i in range(-10,0)]
        HNN_rels.append(HNN_rel1)
        HNN = Group(HNN_gens, HNN_rels)

        new_group = Group(new_group_gens, [HNN_rel1])

        [G, H, used_letters] = magnus_case1(group)
        self.assertEqual(G, HNN)
        self.assertEqual(H, new_group)


class TestMagnusCase2(unittest.TestCase):
    def test1(self):
        a = Syllable("a",[],1)
        b = Syllable("b",[],1)
        c = Syllable("c",[],1)
        relation = [a, b.pow(2), c, b.inverse(), a, b.inverse()]
        group = Group([a,b,c], [relation])
        self.assertEqual(group, str_to_group("<a,b,c|ab^2cb^-1ab^-1>"))

        x = Syllable("x",[],1)
        y = Syllable("y",[],1)
        new_rel = [y, x.pow(4), c, x.pow(-2), y, x.pow(-2)]
        new_group = Group([x,y,c], [new_rel])
        self.assertEqual(new_group,
                         str_to_group("<x, y, c | y x^{4} c x^{-2} y x^{-2}>"))

        C, used_letters = magnus_case2(group)
        self.assertEqual(C, new_group)


if __name__ == '__main__':
    unittest.main()


#groups = magnus_breakdown(str_to_group("<a,b,c|bacb^2a^-3c^3a^2>"))
#groups = magnus_breakdown(str_to_group("<a,b,c,d|a^2bc^-1a>"))
