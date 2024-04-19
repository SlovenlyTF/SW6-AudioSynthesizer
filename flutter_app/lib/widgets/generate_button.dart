import 'package:flutter/material.dart';
import 'package:flutter_app/states/generation_option_state.dart';
import 'package:flutter_app/states/generation_state.dart';
import 'package:flutter_app/states/recording_state.dart';
import 'package:provider/provider.dart';
import 'package:flutter_app/states/audio_saved_state.dart';

class GenerateButton extends StatefulWidget {
  const GenerateButton({super.key, this.size = 75});

  final double size;

  @override
  State<GenerateButton> createState() => _GenerateButtonState();
}

class _GenerateButtonState extends State<GenerateButton> {

  bool generating = false;

  bool canGenerate(bool isRecording) {
    // TODO: Check if audio recording exists
    return !isRecording;
  }

  @override
  Widget build(BuildContext context) {
    // Perhaps we can use Provider.of for the generating state?
    return Consumer4<RecordingState,GenerationState,GenerationOptionState,AudioSavedState>(
      builder: (context, recordingState, generationState, generationOptions, audioSavedState, child) {
        return ElevatedButton(
          // onPressed is null if generation is not allowed to disable the button
          onPressed: !canGenerate(recordingState.getIsRecording) ? null : () {
            generationState.generateAudio(generationOptions, audioSavedState);
          },
          style: ElevatedButton.styleFrom(
            shape: const CircleBorder(),
            minimumSize: Size(widget.size, widget.size),
            backgroundColor: generationState.getGenerating ? Colors.cyan[200] : Colors.cyan[300],
          ),
          child: const Icon(Icons.multitrack_audio_rounded, color: Colors.white, size: 30),
        );
      }
    );
  }
}