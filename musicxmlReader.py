import xml.etree.ElementTree as ETree
from fractions import Fraction


note_value = {
    'A0': 21, '#A0': 22, 'B0': 23, 'C1': 24, '#C1': 25, 'D1': 26, '#D1': 27, 'E1': 28, 'F1': 29, '#F1': 30,
    'G1': 31, '#G1': 32, 'A1': 33, '#A1': 34, 'B1': 35, 'C2': 36, '#C2': 37, 'D2': 38, '#D2': 39, 'E2': 40,
    'F2': 41, '#F2': 42, 'G2': 43, '#G2': 44, 'A2': 45, '#A2': 46, 'B2': 47, 'C3': 48, '#C3': 49, 'D3': 50,
    '#D3': 51, 'E3': 52, 'F3': 53, '#F3': 54, 'G3': 55, '#G3': 56, 'A3': 57, '#A3': 58, 'B3': 59, 'C4': 60,
    '#C4': 61, 'D4': 62, '#D4': 63, 'E4': 64, 'F4': 65, '#F4': 66, 'G4': 67, '#G4': 68, 'A4': 69, '#A4': 70,
    'B4': 71, 'C5': 72, '#C5': 73, 'D5': 74, '#D5': 75, 'E5': 76, 'F5': 77, '#F5': 78, 'G5': 79, '#G5': 80,
    'A5': 81, '#A5': 82, 'B5': 83, 'C6': 84, '#C6': 85, 'D6': 86, '#D6': 87, 'E6': 88, 'F6': 89, '#F6': 90,
    'G6': 91, '#G6': 92, 'A6': 93, '#A6': 94, 'B6': 95, 'C7': 108, '#C7': 97, 'D7': 98, '#D7': 99, 'E7': 100,
    'F7': 101, '#F7': 102, 'G7': 103, '#G7': 104, 'A7': 105, '#A7': 106, 'B7': 107, 'C8': 108
}


class MusicxmlReader:
    def __init__(self, filepath):
        # Load the musicxml file
        tree = ETree.parse(filepath)
        root = tree.getroot()

        # # Print the score metadata
        # title = root.find('.//work/work-title').text
        # composer = root.find('.//creator').text
        # print(title)
        # print(composer)
        div = int(root.find(".//attributes/divisions").text)

        # Iterate over the notes in the score
        for note in root.findall('.//note'):
            try:
                pitch = note_value[
                            note.find('.//pitch/step').text + note.find('.//pitch/octave').text
                        ]+int(note.find('.//pitch/alter').text)
                duration = float(note.find('.//duration').text)
                print(pitch, str(Fraction(duration/div)))
            except AttributeError:
                try:
                    pitch = note_value[note.find('.//pitch/step').text + note.find('.//pitch/octave').text]
                    duration = float(note.find('.//duration').text)
                    print(pitch, str(Fraction(duration/div)))
                except AttributeError:
                    pass


