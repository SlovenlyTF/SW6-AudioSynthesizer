import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_app/states/audio_saved_state.dart';
import 'package:flutter_app/states/generation_state.dart';
import 'package:flutter_app/utilities/notifications.dart';
import 'package:name_plus/name_plus.dart';
import 'package:provider/provider.dart';
import 'package:flutter_app/utilities/file_system.dart';

class SaveButton extends StatefulWidget {
  const SaveButton({super.key, this.size = 75});

  final double size;

  @override
  State<SaveButton> createState() => _SaveButtonState();
}

class _SaveButtonState extends State<SaveButton> {
  bool _isSaving = false;

  @override
  Widget build(BuildContext context) {
    return Consumer2<GenerationState, AudioSavedState>(
      builder: (context, generationState, audioSavedState, child) {
        return ElevatedButton(
          // onPressed is null if recording is not allowed to disable the button
          onPressed: !canSave(generationState, audioSavedState) ? null : () async {
            if(await save()) await audioSavedState.setIsAudioSaved(true);
          },
          style: ElevatedButton.styleFrom(
            shape: const CircleBorder(),
            minimumSize: Size(widget.size, widget.size),
            backgroundColor: _isSaving ? Colors.blue[100] : Colors.blue[600],
          ),
          child: const Icon(Icons.save, color: Colors.white, size: 30),
        );
      }
    );
  }

  bool canSave(GenerationState generationState, AudioSavedState audioSavedState) {
    // TODO: Check: record.hasPermission()
    if(generationState.getGenerating) return false;
    if(audioSavedState.getIsAudioSaved) return false;
    if(!generationState.getFileExists) return false;
    if(_isSaving) return false;
    return true;
  }

  Future<bool> save() async {
    setState(() {
      _isSaving = true;
    });

    // Get file and copy it to archive
    String generatedFilePath = await getTempGeneratedPath();
    String saveFilePath = await getSaveFilePath();
    
    // showDebugToast('Saving audio to $saveFilePath');

    try {
      var file = await copyFile(generatedFilePath, saveFilePath);
      return file.existsSync();
    } catch(error) {
      showDebugToast('Failed to save audio', Colors.red);
      return false;
    } finally {
      setState(() {
        _isSaving = false;
      });
    }
  }

  Future<File> copyFile(String source, String destination) async {
    var sourceFile = File(source);
    return sourceFile.copy(destination);
  }

  Future<String> getSaveFilePath() async {
    return (await File(await getArchivePath()).namePlus(
      'audio.wav',
      space: false,
      format: '_d',
    )).path;
  }
}
