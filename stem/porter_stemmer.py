class porter_stem

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
            if self.is_vowel(word,i):
                pattern += 'V'
            else:
                pattern += 'C'
        return pattern


    def m_count(self,word):
        """finds the value of m in form [C](VC){m}[V]"""

        cv_format = self._cv_form(word)
        count = cv_format.count('VC')
        return (count)



    def _step1a(self,word)

    """*********NOT COMPLETED*********"""

        return word


    def _step1b(self,word)

    """*********NOT COMPLETED*********"""
    
        return word



    def _step1c(self,word)

    """*********NOT COMPLETED*********"""
    
        return word


    def _step2(self,word)

    """*********NOT COMPLETED*********"""
    
        return word


    def _step3(self,word)

    """*********NOT COMPLETED*********"""
    
        return word


    def _step4(self,word)

    """*********NOT COMPLETED*********"""
    
        return word


    def _step5a(self,word)

    """*********NOT COMPLETED*********"""
    
        return word


    def _step5b(self,word)

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