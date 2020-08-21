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

        **_modified_rule **

        (*c and not c) Y -> I           happy        -> happi
                                        enjoy       -> enjoy
                                        spy          -> spi
        """


        if word.endswith('y') and len(word) > 2 and not self._is_vowel(word,-2):
            word = self._replace(word, 'y', 'i')
            
        return word


    def _step2(self,word):

        """Step 2

        (m>0) ATIONAL ->  ATE           relational     ->  relate
        (m>0) TIONAL  ->  TION          conditional    ->  condition
                                        rational       ->  rational
        (m>0) ENCI    ->  ENCE          valenci        ->  valence
        (m>0) ANCI    ->  ANCE          hesitanci      ->  hesitance
        (m>0) IZER    ->  IZE           digitizer      ->  digitize
        (m>0) ABLI    ->  ABLE          conformabli    ->  conformable
        (m>0) ALLI    ->  AL            radicalli      ->  radical
        (m>0) ENTLI   ->  ENT           differentli    ->  different
        (m>0) ELI     ->  E             vileli        - >  vile
        (m>0) OUSLI   ->  OUS           analogousli    ->  analogous
        (m>0) IZATION ->  IZE           vietnamization ->  vietnamize
        (m>0) ATION   ->  ATE           predication    ->  predicate
        (m>0) ATOR    ->  ATE           operator       ->  operate
        (m>0) ALISM   ->  AL            feudalism      ->  feudal
        (m>0) IVENESS ->  IVE           decisiveness   ->  decisive
        (m>0) FULNESS ->  FUL           hopefulness    ->  hopeful
        (m>0) OUSNESS ->  OUS           callousness    ->  callous
        (m>0) ALITI   ->  AL            formaliti      ->  formal
        (m>0) IVITI   ->  IVE           sensitiviti    ->  sensitive
        (m>0) BILITI  ->  BLE           sensibiliti    ->  sensible
        

        **_Additional_rule **

        (m>0) logi    ->  log
        (m>0) fulli   -> ful     



         **_modified_rule **

        The Step 2 rule
            (m>0) abli  →  able
        is replaced by
            (m>0) bli  →  ble
        
        
        """


        if word.endswith('ational') and self._m_count(word[:-7]):
            word = self._replace(word, 'ational', 'ate')
        elif word.endswith('tional')  and self._m_count(word[:-6]):
            word = self._replace(word, 'tional', 'tion')
        elif word.endswith('enci')  and self._m_count(word[:-4]):
            word = self._replace(word, 'enci', 'ence')
        elif word.endswith('anci')  and self._m_count(word[:-4]):
            word = self._replace(word, 'anci', 'ance')
        elif word.endswith('izer')  and self._m_count(word[:-4]):
            word = self._replace(word, 'izer', 'ize')
        elif word.endswith('bli')  and self._m_count(word[:-3]):
            word = self._replace(word, 'bli', 'ble')
        elif word.endswith('alli')  and self._m_count(word[:-4]):
            word = self._replace(word, 'alli', 'al')
        elif word.endswith('entli')  and self._m_count(word[:-5]):
            word = self._replace(word, 'entli', 'ent')
        elif word.endswith('eli')  and self._m_count(word[:-3]):
            word = self._replace(word, 'eli', 'e')
        elif word.endswith('ousli') and self._m_count(word[:-5]):
            word = self._replace(word, 'ousli', 'ous')
        elif word.endswith('ization')  and self._m_count(word[:-7]):
            word = self._replace(word, 'ization', 'ize')
        elif word.endswith('ation')  and self._m_count(word[:-5]):
            word = self._replace(word, 'ation', 'ate')
        elif word.endswith('ator')  and self._m_count(word[:-4]):
            word = self._replace(word, 'ator', 'ate')
        elif word.endswith('alism')  and self._m_count(word[:-5]):
            word = self._replace(word, 'alism', 'al')
        elif word.endswith('iveness')  and self._m_count(word[:-7]):
            word = self._replace(word, 'iveness', 'ive')
        elif word.endswith('fulness')  and self._m_count(word[:-7]):
            word = self._replace(word, 'fulness', 'ful')
        elif word.endswith('ousness')  and self._m_count(word[:-7]):
            word = self._replace(word, 'ousness', 'ous')
        elif word.endswith('aliti')  and self._m_count(word[:-5]):
            word = self._replace(word, 'aliti', 'al')
        elif word.endswith('iviti')  and self._m_count(word[:-5]):
            word = self._replace(word, 'iviti', 'ive')
        elif word.endswith('biliti')  and self._m_count(word[:-6]):
            word = self._replace(word, 'biliti', 'ble')
        elif word.endswith('logi')  and self._m_count(word[:-3]):
            word = self._replace(word, 'logi', 'log')
        elif word.endswith('logi')  and self._m_count(word[:-4]):
            word = self._replace(word, 'logi', 'log')
        elif word.endswith('fulli')  and self._m_count(word[:-5]):
            word = self._replace(word, 'fulli', 'ful')

        return word


    def _step3(self,word):

        """Step 3

        (m>0) ICATE ->  IC              triplicate     ->  triplic
        (m>0) ATIVE ->                  formative      ->  form
        (m>0) ALIZE ->  AL              formalize      ->  formal
        (m>0) ICITI ->  IC              electriciti    ->  electric
        (m>0) ICAL  ->  IC              electrical     ->  electric
        (m>0) FUL   ->                  hopeful        ->  hope
        (m>0) NESS  ->                  goodness       ->  good
        """

        if word.endswith('icate') and self._m_count(word[:-5]):
            word = self._replace(word, 'icate', 'ic')
        elif word.endswith('ative') and self._m_count(word[:-5]):
            word = self._replace(word, 'ative', '')
        elif word.endswith('alize') and self._m_count(word[:-5]):
            word = self._replace(word, 'alize', 'al')
        elif word.endswith('iciti') and self._m_count(word[:-5]):
            word = self._replace(word, 'iciti', 'ic')
        elif word.endswith('ical') and self._m_count(word[:-4]):
            word = self._replace(word, 'ical', 'ic')
        elif word.endswith('ful') and self._m_count(word[:-3]):
            word = self._replace(word, 'ful', '')
        elif word.endswith('ness')and self._m_count(word[:-4]):
            word = self._replace(word, 'ness', '')
    
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
                "spied","died","conflated","troubled","sized","tanned","falling","failing","filing","happy","sky","enjoy",
                'relational', 'conditional', 'rational', 'valenci', 'hesitanci', 'digitizer', 'conformabli', 'radicalli',
                'differentli', 'vileli', 'analogousli', 'vietnamization', 'predication', 'operator', 'feudalism',
                'decisiveness', 'hopefulness', 'callousness', 'formaliti', 'sensitiviti', 'sensibiliti',"geologi",
                'triplicate', 'formative', 'formalize', 'electriciti', 'electrical', 'hopeful', 'goodness']


    correct_stem = ["caress", "poni", "caress", "cat", "tie", "feed","agree","plaster",
                "spi","die","conflate","trouble","size","tan","fall","fail","file","happi","ski","enjoy",
                'relate', 'condition', 'rational', 'valence', 'hesitance', 'digitize', 'conformable', 'radic',
                'different', 'vile', 'analogous', 'vietnamize', 'predic', 'operate', 'feudal',
                'decisive', 'hope', 'callous', 'formal', 'sensitive', 'sensible',"geolog",
                'triplic', 'form', 'formal', 'electric', 'electric', 'hope', 'good']

    # test_string = ["radicalli"]
    # correct_stem = ["radical"]

    print(("{:<15} ==> {:<10} {:<10} {:<15}".format("word", "stemed_word", "actual_stem", "match")))
    for i in range(len(test_string)):
        word = test_string[i]
        stemed_word = stemmer.stem(test_string[i])
        actual_stem = correct_stem[i]
        print(("{:<15} ==>     {:<10} {:<10} {:<15}".format(word, stemed_word, actual_stem, stemed_word == actual_stem)))


