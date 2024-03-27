import 'package:flutter/material.dart';
import 'package:flutter_app/states/generation_option_state.dart';
import 'package:flutter_app/states/generation_state.dart';
import 'package:flutter_app/states/recording_state.dart';
import 'package:provider/provider.dart';

class GenerateButton extends StatefulWidget {
  const GenerateButton({super.key});

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
    return Consumer3<RecordingState,GenerationState,GenerationOptionState>(
      builder: (context, recordingState, generationState, generationOptions, child) {
        return ElevatedButton(
          // onPressed is null if generation is not allowed to disable the button
          onPressed: !canGenerate(recordingState.getIsRecording) ? null : () {
            generationState.generateAudio(generationOptions);
          },
          style: ElevatedButton.styleFrom(
            shape: const CircleBorder(),
            minimumSize: const Size(75, 75),
            backgroundColor: generationState.getGenerating ? Colors.cyan[200] : Colors.cyan[300],
          ),
          child: const Icon(Icons.multitrack_audio_rounded, color: Colors.white, size: 30),
        );
      }
    );
  }
}