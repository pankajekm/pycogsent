class porter_stem:

    def __init__(self):
        self.vowel = ('a', 'e', 'i', 'o', 'u' )


    def _is_vowel(self,word, i):
        """ returns true if word[i] is a consonent 
            p.s. y is not always a consonent
        """

        if (word[i] in self.vowel):
            return True
        elif (word[i] == 'y'):
            if (i == 0):
                return False
            else:
                return self._is_vowel(word,i-1)
        else:
            return False


    def _cv_form(self,word):
        """ converts word to the form [C](VC){m}[V]

                A consonant will be denoted by c, a vowel by v. A list ccc... of length
            greater than 0 will be denoted by C, and a list vvv... of length greater
            than 0 will be denoted by V.
        """

        pattern = ''
        for i in range(len(word)):
            if self._is_vowel(word,i):
                pattern += 'V'
            else:
                pattern += 'C'
        return pattern


    def _m_count(self,word):
        """finds the value of m in form [C](VC){m}[V]"""

        cv_format = self._cv_form(word)
        count = cv_format.count('VC')
        return (count)

    def _replace(self, word, suffix, new_suffix):
        """Replaces suffix of word with new_suffix"""

        assert word.endswith(suffix), "check if word ends with suffix"
        if suffix == "":
            return word + new_suffix
        else:
            return word[: -len(suffix)] + new_suffix

    def _has_vowel(self,word):
        """ checks if word has vowel"""
        for i in range(len(word)):
            if self._is_vowel(word,i):
                return True
        return False

    def _doubleCons(self, word):
        """ Checks if word ends with double consonent rule *d"""
        if len(word) >= 2:
            if word[-1] == word[-2] and not(self._is_vowel(word, -1) or self._is_vowel(word, -2)):
                return True
            else:
                return False
        else:
            return False
    def _cvc(self,word):
        """ checks rule *o 
        
        the stem ends cvc, where the second c is not W, X or Y (e.g.-WIL, -HOP)."""

        if (len(word) >= 3 and 
        not self._is_vowel(word, -3) and 
        self._is_vowel(word, -2) and 
        not self._is_vowel(word, -1) and 
        word[-1] not in ("w", "x", "y")):

            return True
        else:
            return False


    def _step1a(self,word):
        """ Step 1a

        SSES -> SS                         caresses  ->  caress
        IES  -> I                          ponies    ->  poni
        SS   -> SS                         caress    ->  caress
        S    ->                            cats      ->  cat 
        
        **_Additional_rule **
        IES -> IE (len(word) = 4)          ties      ->  tie 
        """

        if word.endswith('sses'):
            word = self._replace(word, 'sses', 'ss')
        elif word.endswith('ies'):
            if len(word) == 4:
                word = self._replace(word, 'ies', 'ie') 
            else:
                word = self._replace(word, 'ies', 'i')
        elif word.endswith('ss'):
            word = self._replace(word, 'ss', 'ss')
        elif word.endswith('s'):
            word = self._replace(word, 's', '')

        return word


    def _step1b(self,word):
        """Step 1b

            (m>0) EED -> EE                 feed      ->  feed
                                            agreed    ->  agree
            (*v*) ED  ->                    plastered ->  plaster
                                            bled      ->  bled
            (*v*) ING ->                    motoring  ->  motor
                                            sing      ->  sing

        If the second or third of the rules in Step 1b is successful, the following
        is done:

            AT -> ATE                       conflat(ed)  ->  conflate
            BL -> BLE                       troubl(ed)   ->  trouble
            IZ -> IZE                       siz(ed)      ->  size
            (*d and not (*L or *S or *Z))
            -> single letter
                                            hopp(ing)    ->  hop
                                            tann(ed)     ->  tan
                                            fall(ing)    ->  fall
                                            hiss(ing)    ->  hiss
                                            fizz(ed)     ->  fizz
            (m=1 and *o) -> E               fail(ing)    ->  fail
                                            fil(ing)     ->  file

        The rule to map to a single letter causes the removal of one of the double
        letter pair. The -E is put back on -AT, -BL and -IZ, so that the suffixes
        -ATE, -BLE and -IZE can be recognised later. This E may be removed in step 4.


        **_Additional_rule **

        IED -> ie (len(word) = 4)           died         ->  die
            -> i                            spied        ->  spi

        """

        rule_2_3_flag = False

        if word.endswith("ied"):
            if len(word) == 4:
                word =  self._replace(word, "ied", "ie")
            else:
                word =  self._replace(word, "ied", "i")
        elif word.endswith("eed"):
            if self._m_count(self._replace(word, "eed", "")) > 0 : # check if m>0
                word  = self._replace(word, "eed", "ee")
        elif word.endswith("ed"):
            if self._has_vowel(self._replace(word, "ed", "")): # checks if stem has vowel
                word = self._replace(word, "ed", "")
                rule_2_3_flag = True
        elif word.endswith("ing"):
            if self._has_vowel(self._replace(word, "ing", "")): # checks if stem has vowel
                word = self._replace(word, "ing", "")
                rule_2_3_flag = True
        
        if rule_2_3_flag == True:
            if word.endswith('at') or word.endswith('bl') or word.endswith('iz'):
                word += 'e'
            elif (self._doubleCons(word) and not  word.endswith('l')
            and not  word.endswith('s') and not  word.endswith('z')):
                word = word[:-1]
            elif self._m_count(word) == 1 and self._cvc(word):
                word += 'e'
            

        return word



    def _step1c(self,word):
        """Step 1c

        (*v*) Y -> I                    happy        ->  happi
                                        sky          ->  sky
        """
        if word.endswith('y') and self._has_vowel(word[:-1]):
            word = self._replace(word, 'y', 'i')

        return word


    def _step2(self,word):

        """*********NOT COMPLETED*********"""
    
        return word


    def _step3(self,word):

        """*********NOT COMPLETED*********"""
    
        return word


    def _step4(self,word):

        """*********NOT COMPLETED*********"""
    
        return word


    def _step5a(self,word):

        """*********NOT COMPLETED*********"""
    
        return word


    def _step5b(self,word):

        """*********NOT COMPLETED*********"""
    
        return word



    def stem(self,word):
        """
        finds stem root or word 
        """

        stem = word.lower()

        stem = self._step1a(stem)
        stem = self._step1b(stem)
        stem = self._step1c(stem)
        stem = self._step2(stem)
        stem = self._step3(stem)
        stem = self._step4(stem)
        stem = self._step5a(stem)
        stem = self._step5b(stem)

        return stem

if __name__ == "__main__":
    stemmer = porter_stem()
    test_string = ["caresses", "ponies", "caress", "cats","ties", "feed","agreed","plastered",
                "spied","died","conflated","troubled","sized","tanned","falling","failing","filing","happy","sky"]


    correct_stem = ["caress", "poni", "caress", "cat", "tie", "feed","agree","plaster",
                "spi","die","conflate","trouble","size","tan","fall","fail","file","happi","sky"]

    # test_string = ["plastered"]
    # correct_stem = ["plaster"]

    print(("{:<15} ==> {:<10} {:<10} {:<15}".format("word", "stemed_word", "actual_stem", "match")))
    for i in range(len(test_string)):
        word = test_string[i]
        stemed_word = stemmer.stem(test_string[i])
        actual_stem = correct_stem[i]
        print(("{:<15} ==>     {:<10} {:<10} {:<15}".format(word, stemed_word, actual_stem, stemed_word == actual_stem)))


