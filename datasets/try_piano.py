import musicalbeeps

'''
player = musicalbeeps.Player(volume = 0.3,
                            mute_output = False)

# Examples:

# To play an A on default octave n°4 for 0.2 seconds
player.play_note("c", 2.5)

# To play a G flat on octave n°3 for 2.5 seconds
player.play_note("G3b", 2.5)

# To play a F sharp on octave n°5 for the default duration of 0.5 seconds
player.play_note("F5#")

# To pause the player for 3.5 seconds
player.play_note("pause", 3.5)

'''
import musicalbeeps

# Define the musical notes and their durations for the Pink Panther theme
song = [
    ("E", 0.5),
    ("D", 0.5),
    ("A", 0.5),
    ("B", 1),
    ("A", 0.5),
    ("E", 0.5),
    ("D", 0.5),
    ("A", 1),
    ("B", 0.5),
    ("E", 0.5),
    ("D", 0.5),
    ("A", 1),
    ("B", 0.5),
    ("E", 0.5),
    ("D", 0.5),
    ("A", 1),
    ("E", 0.5),
    ("D", 0.5),
    ("A", 0.5),
    ("B", 1),
    ("A", 0.5),
    ("E", 0.5),
    ("D", 0.5),
    ("A", 1),
    ("B", 0.5),
    ("E", 0.5),
    ("D", 0.5),
    ("A", 1),
    ("B", 0.5),
    ("E", 0.5),
    ("D", 0.5),
    ("A", 1),
    ("E", 0.5),
    ("D", 0.5),
    ("A", 0.5),
    ("B", 1),
    ("A", 0.5),
    ("E", 0.5),
    ("D", 0.5),
    ("A", 1),
]

# Initialize the player
player = musicalbeeps.Player(volume=0.5, mute_output=False)

# Play the Pink Panther theme
for note, duration in song:
    player.play_note(note, duration)