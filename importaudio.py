from pydub import AudioSegment
from pydub.playback import play


class processAudio(object):

    def __init__(self, filename):
        """Return a Customer object whose name is *name* and starting
        balance is *balance*."""
        self.name = filename

    def playaudio(self):
        # convert audio to datasegment
        # the file type out of the phone is .aac.
        # we need to play it as mp4
        sound = AudioSegment.from_file(self.name, "mp4")
        play(sound)  # play sound

    def printFileName(self):
        print 'filename = ', self.name

# if __name__ == '__main__':
    # filename = '15_01_2018_17_36_40.mp4'
    # newob = processAudio(filename)
    # newob.printFileName()
    # newob.playaudio()
