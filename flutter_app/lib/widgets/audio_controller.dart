import 'dart:math';

import 'package:flutter/material.dart';
import 'package:just_audio/just_audio.dart';
import 'dart:io';
import 'package:path_provider/path_provider.dart';

class AudioController extends StatefulWidget {
  const AudioController({super.key});

  @override
  State<AudioController> createState() => _AudioControllerState();
}

class _AudioControllerState extends State<AudioController> {
  late AudioPlayer _audioPlayer;
  double _sliderValue = 0.0;
  bool _isPlaying = false;

  @override
  void initState() {
      super.initState();
      instantiateAudioPlayer();
  }

  void instantiateAudioPlayer() async {
    // TODO: Move this thing somewhere else man
    Directory appDocumentsDirectory = await getApplicationDocumentsDirectory();
    String filePath = '${appDocumentsDirectory.path}/test.wav';

    _audioPlayer = AudioPlayer();
    _audioPlayer.setUrl(filePath);
    _audioPlayer.positionStream.listen((position) {
      setState(() {
        _sliderValue = position.inMilliseconds.toDouble();
      });
    });
    _audioPlayer.playerStateStream.listen((playerState) {
      setState(() {
        _isPlaying = playerState.playing;
        if (playerState.processingState == ProcessingState.completed) {
            _isPlaying = false;
        }
      });
    });
  }

  @override
  void dispose() {
    _audioPlayer.dispose();
    super.dispose();
  }

  void _playPause() {
    if (_isPlaying) {
      _audioPlayer.pause();
    } else {
      _audioPlayer.play();
    }
  }

  void _seek(double ms) {
    int targetTime = ms < 0 ? 0 : ms.toInt();
    targetTime = min(targetTime, _audioPlayer.duration?.inMilliseconds ?? 0);
    _audioPlayer.seek(Duration(milliseconds: targetTime));
  }

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Padding(
        // DOG SHIT HARDCODED VALUE STRAIGHT FROM ASS
        padding: const EdgeInsets.only(right: 32),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
        
            // PLAY / PAUSE BUTTON
            Expanded(
              flex: 1,
              child: IconButton(
                icon: Icon(_isPlaying ? Icons.pause : Icons.play_arrow, size: 20.0, color: Colors.white),
                onPressed: _playPause,
              ),
            ),
        
            // SLIDER
            Expanded(
              flex: 3,
              child: Column(
                children: <Widget>[
                  // SLIDER BAR
                  SliderTheme(
                    data: const SliderThemeData(
                      trackShape: CustomSliderTrackShape(),
                      thumbShape: RoundSliderThumbShape(
                        enabledThumbRadius: 5,
                        disabledThumbRadius: 0,
                      ),
                    ),
                    child: Slider(
                      value: _sliderValue,
                      min: 0.0,
                      max: (_audioPlayer.duration?.inMilliseconds.toDouble() ?? 0.0)+100.0,
                      onChanged: _seek,
                    ),
                  ),
                  // SLIDER LABELS
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(_msToTimeString(_sliderValue), style: TextStyle(color: Colors.white)),
                      Text(_msToTimeString(_audioPlayer.duration?.inMilliseconds.toDouble()), style: TextStyle(color: Colors.white)),
                    ],
                  ),
                ],
              ),
            ),
          ],
        ),
      )
    );
  }

  // Return a time string in the format mm:ss
  String _msToTimeString(double? ms) {
    if (ms == null) return '00:00';

    int minutes = ((ms/60000) % 60).toInt();
    int seconds = ((ms/1000) % 60).toInt();

    // Return a time string in the format 12:34
    return '${minutes.toString().padLeft(2, '0')}:${seconds.toString().padLeft(2, '0')}';
  }
}

class CustomSliderTrackShape extends RoundedRectSliderTrackShape {
  const CustomSliderTrackShape();
  @override
  Rect getPreferredRect({
    required RenderBox parentBox,
    Offset offset = Offset.zero,
    required SliderThemeData sliderTheme,
    bool isEnabled = false,
    bool isDiscrete = false,
  }) {
    final trackHeight = sliderTheme.trackHeight;
    final trackLeft = 0.0;
    final trackTop = offset.dy + (parentBox.size.height - trackHeight!) / 2;
    final trackWidth = parentBox.size.width;
    return Rect.fromLTWH(trackLeft, trackTop, trackWidth, trackHeight);
  }
}
