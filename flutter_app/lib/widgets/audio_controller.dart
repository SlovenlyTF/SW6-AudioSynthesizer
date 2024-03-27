import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter_app/states/generation_state.dart';
import 'package:flutter_app/states/recording_state.dart';
import 'package:just_audio/just_audio.dart';
import 'package:provider/provider.dart';

class AudioController extends StatefulWidget {
  const AudioController({super.key, required this.filePath});

  // Using a future value for now, perhaps move the waiting to a more appropriate location
  final Future<String> filePath;

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
    _audioPlayer = AudioPlayer();
    // TODO: Hardcoding file path for now, receive as parameter instead
    _audioPlayer.setUrl(await widget.filePath);
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
      // Restart if at the end
      if (_audioPlayer.position >= (_audioPlayer.duration ?? Duration.zero)) {
        _audioPlayer.seek(Duration.zero);
      }
      _audioPlayer.play();
    }
  }

  void _seek(double ms) {
    int targetTime = ms < 0 ? 0 : ms.toInt();
    targetTime = min(targetTime, _audioPlayer.duration?.inMilliseconds ?? 0);
    _audioPlayer.seek(Duration(milliseconds: targetTime));
  }

  bool canPlay(bool isRecording, bool isGenerating) {
    return !(isRecording || isGenerating);
  }

  @override
  Widget build(BuildContext context) {
    return Consumer2<RecordingState,GenerationState>(
      builder: (context, recordingState, generationState, child) {
        // Straight from ass, + lots of reloading
        if(!generationState.getHaveReloadedAudioplayer){
          generationState.setHaveReloadedAudioplayer(true);
          _audioPlayer.load();
        }
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
                    onPressed: !canPlay(recordingState.getIsRecording, generationState.getGenerating) ? null : _playPause,
                  ),
                ),
            
                // SLIDER
                Expanded(
                  flex: 3,
                  child: Column(
                    children: <Widget>[
                      // SLIDER BAR
                      SliderTheme(
                        data: SliderThemeData(
                          activeTrackColor: Colors.cyan[300],
                          thumbColor: Colors.cyan[100],
                          trackShape: const CustomSliderTrackShape(),
                          thumbShape: const RoundSliderThumbShape(
                            enabledThumbRadius: 5,
                            disabledThumbRadius: 0,
                          ),
                        ),
                        child: Slider(
                          value: _sliderValue,
                          min: 0.0,
                          max: (_audioPlayer.duration?.inMilliseconds.toDouble() ?? 0.0)+50.0, // Add padding to avoid overflowing, this fix is hot garbage <3
                          onChanged: !canPlay(recordingState.getIsRecording, generationState.getGenerating) ? null : _seek,
                        ),
                      ),
                      // SLIDER LABELS
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text(_msToTimeString(_sliderValue), style: const TextStyle(color: Colors.white)),
                          Text(_msToTimeString(_audioPlayer.duration?.inMilliseconds.toDouble()), style: const TextStyle(color: Colors.white)),
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
    );
  }

  // Return a time string in the format mm:ss
  String _msToTimeString(double? ms) {
    if (ms == null) return '00:00';

    int minutes = ((ms/60000) % 60).toInt();
    int seconds = ((ms/1000) % 60).toInt();

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
