
class FormatTransformer:

    def tokenListTransf(self, tokenlist):
        res = []
        for i, aa in enumerate(tokenlist):
            if aa[1] != 'ID' and aa[1] != 'CONST':
                    token = (aa[0], aa[1], aa[2].upper())
                    res.append(token)
            else:
                res.append(aa)
        return res