from random import randrange


'''
The idea here is to test repetition in long sequences to see how the solver performs
'''


tubthumping = 'I get knocked down, but I get up again You are never gonna keep me down I get knocked down, but I get up again You are never gonna keep me down I get knocked down, but I get up again You are never gonna keep me down I get knocked down, but I get up again You are never gonna keep me down He drinks a Whiskey drink, he drinks a Vodka drink He drinks a Lager drink, he drinks a Cider drink He sings the songs that remind him of the good times He sings the songs that remind him of the best times (Oh Danny Boy, Danny Boy, Danny Boy) I get knocked down, but I get up again You are never gonna keep me down I get knocked down, but I get up again You are never gonna keep me down I get knocked down, but I get up again You are never gonna keep me down I get knocked down, but I get up again You are never gonna keep me down He drinks a Whiskey drink, he drinks a Vodka drink He drinks a Lager drink, he drinks a Cider drink He sings the songs that remind him of the good times He sings the songs that remind him of the best times (Dont cry for me, next door neighbour) I get knocked down, but I get up again You are never gonna keep me down I get knocked down, but I get up again You are never gonna keep me down I get knocked down, but I get up again You are never gonna keep me down I get knocked down, but I get up again You are never gonna keep me down I get knocked down, (well be singing) but I get up again You are never gonna keep me down (when were winning) I get knocked down, (well be singing) but I get up again You are never gonna keep me down (ooh) I get knocked down, (well be singing) but I get up again You are never gonna keep me down (when were winning) I get knocked down, (well be singing) but I get up again You are never gonna keep me down (ooh) I get knocked down, (well be singing) But I get up again (pissing the night away) You are never gonna keep me down (when were winning) I get knocked down, (well be singing) But I get up again (pissing the night away) You are never gonna keep me down (ooh) I get knocked down, (well be singing) But I get up again (pissing the night away) You are never gonna keep me down (when were winning) I get knocked down, (well be singing) But I get up again (pissing the night away) You are never gonna keep me down (ooh) I get knocked down, (well be singing) But I get up again (pissing the night away) You are never gonna keep me down (when were winning) I get knocked down, (well be singing) But I get up again (pissing the night away) You are never gonna keep me down (ooh) I get knocked down, (well be singing) But I get up again (pissing the night away) You are never gonna keep me down (when were winning) I get knocked down, (well be singing) But I get up again (pissing the night away) You are never gonna keep me down (ooh) I get knocked down, (well be singing) But I get up again (pissing the night away) You are never gonna keep me down (when were winning) I get knocked down, (well be singing) But I get up again (pissing the night away) You are never gonna keep me down (ooh) I get knocked down, (well be singing) But I get up again (pissing the night away) You are never gonna keep me down (when were winning)'
tubthumping = tubthumping.replace(' ', '_')

N = 1000
min_length = 25
max_length = 75


def get_reads(number_reads=1000, min_length=25, max_length=75):
    reads = []
    for x in xrange(number_reads):
        l = randrange(len(tubthumping))
        u = l + randrange(min_length, max_length)
        reads.append(tubthumping[l:u])
    return reads
