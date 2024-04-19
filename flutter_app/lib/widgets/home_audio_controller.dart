import 'package:flutter/material.dart';
import 'package:flutter_app/widgets/audio_controller.dart';
import 'package:flutter_app/states/recording_state.dart';
import 'package:flutter_app/states/generation_state.dart';
import 'package:just_audio/just_audio.dart';
import 'package:provider/provider.dart';

class HomeAudioController extends AudioController {
  HomeAudioController({super.key, required super.filePath, bool? canPlay})
      : super(canPlay: true /*this=poopoo*/, onAudioPlayerCreated: (AudioPlayer audioPlayer) {});
  
  @override
  State<HomeAudioController> createState() => _HomeAudioControllerState();
}

class _HomeAudioControllerState extends State<HomeAudioController> {
  late AudioPlayer _audioPlayer;
  bool _audioPlayerCreated = false;

  @override
  void initState() {
    super.initState();
  }

  bool canPlay(bool isRecording, bool isGenerating) {
    return !(isRecording || isGenerating);
  }

  @override
  Widget build(BuildContext context) {
    return Consumer2<RecordingState, GenerationState>(
      builder: (context, recordingState, generationState, child) {
        if (!generationState.getHaveReloadedAudioplayer && _audioPlayerCreated) {
          generationState.setHaveReloadedAudioplayer(true);
          _audioPlayer.load();
        }
        return AudioController(
          filePath: widget.filePath,
          canPlay: canPlay(recordingState.getIsRecording, generationState.getGenerating),
          onAudioPlayerCreated: (audioPlayer) {
            _audioPlayer = audioPlayer;
            _audioPlayerCreated = true; // Set the flag to true after the audio player is created
          },
        );
      },
    );
  }
}