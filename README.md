# Music Scale Ranger 🎵

A Python-based music theory exploration tool built with [music21](https://www.music21.org/).

Music Scale Ranger allows users to explore musical scales, find scales compatible with a collection of notes, inspect scale notes, and generate traditional diatonic harmonic fields.

It also includes a custom implementation of the Blues Scale.

## Features

* Find scales containing a given collection of notes
* Handle enharmonic equivalents such as `C#` and `Db`
* Display the notes of a selected scale
* Generate diatonic triads
* Generate diatonic seventh chords
* Support major, minor, modal, harmonic minor, melodic minor and blues scales
* Custom `BluesScale` implementation compatible with `music21`
* Validate whether a scale is suitable for traditional seven-degree harmonic-field generation

## Example

Given the notes:

```text
C E G
```

the analyzer searches the available scales and possible tonics for compatible combinations.

The tool can also display a scale:

```text
C Major

C - D - E - F - G - A - B - C
```

and generate its harmonic field:

```text
I     C major
ii    D minor
iii   E minor
IV    F major
V     G major
vi    A minor
vii°  B diminished
```

## Blues Scale

The project includes a custom Blues Scale implementation.

Its interval formula is:

```text
1 - ♭3 - 4 - ♭5 - 5 - ♭7
```

For C:

```text
C - Eb - F - Gb - G - Bb
```

The custom scale is implemented as a subclass of `music21.scale.Scale`, allowing it to participate in the same scale-analysis workflow as the other scales.

## Scale Search

The scale search compares pitch classes when determining whether notes belong to a scale.

For example:

```text
C# == Db
F# == Gb
A# == Bb
```

The spelling of the note is therefore ignored when determining pitch-class membership.

### Important limitation

The scale finder does **not** currently determine the most likely key or tonal center.

Instead, it answers:

> "Which scales contain all of these notes?"

A set of notes can therefore produce multiple possible scales.

## Harmonic Field

The harmonic-field generator constructs chords by stacking thirds from the scale.

For example, in C major:

```text
C E G
D F A
E G B
F A C
G B D
A C E
B D F
```

For seventh chords, the seventh scale degree is added to each structure.

Traditional harmonic-field generation is currently restricted to **seven-note scales**.

This prevents non-heptatonic scales, such as the six-note Blues Scale, from being interpreted as conventional seven-degree diatonic systems.

## Project Structure

```text
music_scale_ranger/
│
├── music_scale_ranger.py
├── tests/
│   ├── __init__.py
│   └── test_music_scale_ranger.py
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
└── .git/
```

The `.git/` directory is created automatically by Git and is not uploaded as part of the project files.

## Installation

Clone the repository:

```bash
git clone https://github.com/ZeroNipher/music_scale_ranger.git
cd music_scale_ranger
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

### Windows

```bash
.venv\Scripts\activate
```

### macOS / Linux

```bash
source .venv/bin/activate
```

Install the dependency:

```bash
pip install -r requirements.txt
```

## Usage

Run the program:

```bash
python music_scale_ranger.py
```

The interactive menu provides:

```text
========================================
       MÓDULO DE ANÁLISE MUSICAL
========================================
1. Descobrir escalas a partir de notas
2. Ver notas de uma escala específica
3. Ver campo harmônico (tríades/tétrades)
4. Sair
========================================
```

## Tests

The project uses Python's built-in `unittest` framework.

Run the test suite from the project root:

```bash
python -m unittest discover
```

The current test suite covers:

* Major scale note generation
* Blues Scale note generation
* Diatonic triad generation
* Diatonic seventh-chord generation
* Scale identification from a collection of notes

## Requirements

The project currently depends on:

* Python
* [music21](https://www.music21.org/)

The required dependency is listed in `requirements.txt`.

## Technologies

* Python
* [music21](https://www.music21.org/)
* `unittest`

## Future Improvements

Possible future features include:

* Roman numeral analysis
* Chord progression analysis
* Key detection
* Chord-to-scale recommendations
* Additional custom scales
* MIDI input and output
* MIDI playback
* Command-line arguments
* Graphical user interface
* Web interface

## Motivation

This project started as an exploration of the `music21` library and its representation of pitches, intervals, scales and chords.

The goal is to combine programming with music theory and gradually develop the project into a reusable tool for musical analysis.
