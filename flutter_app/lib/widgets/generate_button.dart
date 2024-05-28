import 'package:flutter/material.dart';
import 'package:flutter_app/states/generation_option_state.dart';
import 'package:flutter_app/states/generation_state.dart';
import 'package:flutter_app/states/last_generation.dart';
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

  bool canGenerate(RecordingState recordingState, String previousOperation, String selectedOperation) {
    bool isRecording = recordingState.getIsRecording;
    bool recordingExists = recordingState.getRecordingExists;
    bool newRecording = recordingState.getNewRecording;
    return !isRecording && recordingExists && (newRecording || (previousOperation != selectedOperation));
  }

  @override
  Widget build(BuildContext context) {
    // Perhaps we can use Provider.of for the generating state?
    return Consumer5<RecordingState,GenerationState,GenerationOptionState,AudioSavedState,LastGeneration>(
      builder: (context, recordingState, generationState, generationOptions, audioSavedState, lastGeneration, child) {
        return Column(
          children: [
            ElevatedButton(
              // onPressed is null if generation is not allowed to disable the button
              onPressed: !canGenerate(recordingState, lastGeneration.getPreviousOperation, generationOptions.getOperation.label) ? null : () {
                generationState.generateAudio(generationOptions, audioSavedState, generationOptions, recordingState, lastGeneration);
              },
              style: ElevatedButton.styleFrom(
                shape: const CircleBorder(),
                minimumSize: Size(widget.size, widget.size),
                backgroundColor: generationState.getGenerating ? Colors.cyan[200] : Colors.cyan[300],
              ),
              child: const Icon(Icons.multitrack_audio_rounded, color: Colors.white, size: 30),
            ),
            const Text(
              "Generate",
              style: TextStyle(
                color: Colors.white,
                fontSize: 14,
              ),
            ),
          ],
        );
      }
    );
  }
}