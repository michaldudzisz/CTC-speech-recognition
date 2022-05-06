from word_spotting.distance61 import distance_ratio61

def test_should_compute_ratio():
    # given
    model_phones = ['sil', 'b','aa','sil','p','ey','sil','p','er','dx','ow','v','er','sil','d','ah','l','ih','l','ih','ng','m','ih','l','z','sil']
    word_phones = ['p', 'ey', 'p', 'axr', 'd']
    distance = 3
    ratio = 1 - (distance / (len(word_phones))) # 0.4

    # expect
    assert distance_ratio61(model_phones, word_phones) == ratio

