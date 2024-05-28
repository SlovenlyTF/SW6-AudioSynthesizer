import 'package:flutter/material.dart';
import 'package:flutter_app/states/generation_state.dart';
import 'package:flutter_app/states/recording_state.dart';
import 'package:provider/provider.dart';

class RecordButton extends StatefulWidget {
  const RecordButton({super.key, this.size = 75});

  final double size;

  @override
  State<RecordButton> createState() => _RecordButtonState();
}

class _RecordButtonState extends State<RecordButton> {
  @override
  Widget build(BuildContext context) {
    // Perhaps we can use Provider.of for the recording state?
    return Consumer2<RecordingState,GenerationState>(
      builder: (context, recordingState, generationState, child) {
        return ElevatedButton(
          // onPressed is null if recording is not allowed to disable the button
          onPressed: !canStartRecording(generationState.getGenerating) ? null : () {
            if(recordingState.getIsRecording) {
              return recordingState.stopRecording();
            }
            recordingState.startRecording();
          },
          style: ElevatedButton.styleFrom(
            shape: const CircleBorder(),
            minimumSize: Size(widget.size, widget.size),
            backgroundColor: recordingState.getIsRecording ? Colors.red : Colors.blue[600],
          ),
          child: recordingState.getIsRecording ?
            const Icon(Icons.square, color: Colors.white, size: 30) :
            const Icon(Icons.mic, color: Colors.white, size: 30),
        );
      }
    );
  }

  bool canStartRecording(bool isGenerating) {
    // TODO: Check: record.hasPermission()
    return !isGenerating;
  }
}
